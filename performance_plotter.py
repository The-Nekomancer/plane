import matplotlib.pyplot as plt

def performance_plotter(CL,CD,LD,Alpha):
    
    '''CL VS Alpha'''
    fig = plt.figure(1)
    plt.plot(Alpha,CL)
    plt.title("CL and Alpha")
    plt.xlabel("Alpha")
    plt.ylabel("CL")
    plt.show()
    
    '''CL VS Alpha'''
    fig = plt.figure(2)
    plt.plot(Alpha,CD)
    plt.title("CD and Alpha")
    plt.xlabel("Alpha")
    plt.ylabel("CD")
    plt.show()
    
    '''CL VS Alpha'''
    fig = plt.figure(3)
    plt.plot(Alpha,LD)
    plt.title("L/D and Alpha")
    plt.xlabel("Alpha")
    plt.ylabel("L/D")
    plt.show()