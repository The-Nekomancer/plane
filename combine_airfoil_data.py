import pandas as pd


# function to combine airfoil data
def combine_airfoil_data(performance_csv, geometry_txt, output_csv):
    """
    performance_data(CSV): "naca4412.csv", "naca2412.csv" ( Alpha, CL, CD, CDp, CM, Top_Xtr -> X, Bot_Xtr -> Y)
    geometry_data(TXT): "naca 4412.txt", "NACA 2412.txt" (x, y, z coordinates)
    output_csv: "naca4412_combined.csv", "naca2412_combined.csv"
    """

    # Load performance csv file
    performance_df = pd.read_csv(performance_csv)

     # Check for columns that Xtr and Ytr are in the dataframe
    cols = performance_df.columns
    if "Top_Xtr" in cols and "Bot_Xtr" in cols:
        # Rename Top_Xtr and Bot_Xtr to X and Y
        performance_df.rename(columns={"Top_Xtr": "X", "Bot_Xtr": "Y"}, inplace=True)

    # Add Block Type Column
    performance_df['Block_Type'] = 'Performance'

    # Ad Geometry Columns
    performance_df['x_coord'] = None
    performance_df['y_coord'] = None
    performance_df['z_coord'] = None


    # 10 column schema
    performance_df = performance_df[['Block_Type', 'Alpha', 'CL', 'CD', 'CDp', 'CM', 'X', 'Y', 'x_coord', 'y_coord', 'z_coord']]

    # Load geometry txt file -> parse as CSV with delimeter space
    geometry_df = pd.read_csv(geometry_txt, delim_whitespace=True, header=None)

    # If no Z column, assign to 0
    if geometry_df.shape[1] == 2:
        geometry_df[2] = 0
    
    # Get x, y, z coordinates and name them -> x_coord, y_coord, z_coord
    geometry_df.columns = ['og_x', 'og_y', 'og_z']

    # Create geometry columns (x_coord, y_coord, z_coord)
    geometry_df['x_coord'] = geometry_df['og_x']
    geometry_df['y_coord'] = geometry_df['og_y']
    geometry_df['z_coord'] = geometry_df['og_z']

    #Fill performance values with None
    geometry_df['Block_Type'] = 'Geometry'
    geometry_df['Alpha'] = None
    geometry_df['CL'] = None
    geometry_df['CD'] = None
    geometry_df['CDp'] = None
    geometry_df['CM'] = None
    geometry_df['X'] = None
    geometry_df['Y'] = None

    # 10 column schema
    geometry_df = geometry_df[['Block_Type', 'Alpha', 'CL', 'CD', 'CDp', 'CM', 'X', 'Y', 'x_coord', 'y_coord', 'z_coord']]

    # Combine the two dataframes
    combined_df = pd.concat([performance_df, geometry_df], ignore_index=True)

    #Output to CSV
    combined_df.to_csv(output_csv, index=False)
    print(f"Created merged CSV -> {output_csv}, with 10 columns") 


if __name__ == '__main__':
    combine_airfoil_data("naca4412.csv", "naca 4412.txt", "naca4412_combined.csv")
    combine_airfoil_data("naca2412.csv", "NACA 2412.txt", "naca2412_combined.csv")
    print("Combined data successfully written to CSV files!")
