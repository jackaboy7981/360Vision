import json
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['axes.grid'] = True

_config = None

def _load_config():
    """Load the configuration from the JSON file."""
    global _config
    if _config is None:
        with open("config.json", "r") as file:
            _config = json.load(file)
    return _config

def visualizeFrame(objects):
    '''Visualizing the 3d object position of surrounding objects along with the Main object [xCord, yCord, lenght, width, height, angle, category]'''
    if objects.shape[1] != 7:
        raise ValueError("Expected objects parameter dimension is [x,7]")
    if "Main" in objects[:,6]:
        raise ValueError("Category cannot be Main")
    config = _load_config()
    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")
    ax.set_xlim(config['X-Axis'][0], config['X-Axis'][1])
    ax.set_ylim(config['Y-Axis'][0], config['Y-Axis'][1])
    ax.set_zlim(config['Z-Axis'][0], config['Z-Axis'][1])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    drawBox(ax, 0,0, 4, 4, 2, 0, 'Main') #sensor car box
    for xCord, yCord, lenght, width, height, angle, category in objects:
        drawBox(ax, xCord, yCord, lenght, width, height, angle, category)
    plt.show()

def drawBox(ax, xCord, yCord, lenght, width, height, angle, category, debugging = False):
    '''the boxes are drawn such that they rest on the x,y plain. 
        Angle:radiance'''
    config = _load_config()
    halflength, halfwidth = lenght/2, width/2
    baseCord = np.array([[halfwidth, -halfwidth, -halfwidth, halfwidth],
                        [halflength, halflength, -halflength, -halflength]]) #[x,y]
    sine , cosine = np.sin(angle), np.cos(angle)
    rotationMatrix = [[cosine, -sine],[sine, cosine]]
    roatatedCordinates = np.dot(rotationMatrix, baseCord)
    translatedBaseCordinates = np.concatenate((np.array([roatatedCordinates[0] + xCord, roatatedCordinates[1] + yCord, np.zeros(roatatedCordinates[1].shape[0])]), np.array([roatatedCordinates[0] + xCord, roatatedCordinates[1] + yCord, np.full(roatatedCordinates[1].shape[0],height)])), axis=1)
    #translatedBaseCordinates has the base 4 cordinates and then the top 4 cordinates in the same order
    #setting the ploting path
    plotingPath = np.concatenate((translatedBaseCordinates[:,:4],translatedBaseCordinates[:,:1],translatedBaseCordinates[:,4:],translatedBaseCordinates[:,4:6],translatedBaseCordinates[:,1:3],translatedBaseCordinates[:,6:8],translatedBaseCordinates[:,3:4]), axis=1)
    
    ax.plot(plotingPath[0], plotingPath[1], plotingPath[2], color = config['CategoryColors'][category])
    #ploting x for front side
    crossline1 = np.concatenate((translatedBaseCordinates[:,:1],translatedBaseCordinates[:,5:6]),axis=1)
    crossline2 = np.concatenate((translatedBaseCordinates[:,1:2],translatedBaseCordinates[:,4:5]),axis=1)

    ax.plot(crossline1[0], crossline1[1], crossline1[2], color = "Black")
    ax.plot(crossline2[0], crossline2[1], crossline2[2], color = "Black")

    if debugging:
        colors = ['red', 'blue', 'green', 'yellow']
        fig = plt.figure()
        ax = fig.add_subplot(311, aspect='equal')
        ax.set_xlim(config['X-Axis'][0], config['X-Axis'][1])
        ax.set_ylim(config['Y-Axis'][0], config['Y-Axis'][1])
        for x,c in zip(baseCord.T, colors):
            ax.scatter(x[0],x[1],color=c)

        ay = fig.add_subplot(312, aspect='equal')
        ay.set_xlim(config['X-Axis'][0], config['X-Axis'][1])
        ay.set_ylim(config['Y-Axis'][0], config['Y-Axis'][1])
        for x,c in zip(roatatedCordinates.T, colors):
            ay.scatter(x[0],x[1], color=c)
        
        az = fig.add_subplot(313, aspect='equal')
        az.set_xlim(config['X-Axis'][0], config['X-Axis'][1])
        az.set_ylim(config['Y-Axis'][0], config['Y-Axis'][1])
        for x,c in zip(translatedBaseCordinates.T, colors):
            az.scatter(x[0],x[1],color=c)
        plt.show()
        print("Base Cordinates :",baseCord)
        print("Rotated Base Cordinates", roatatedCordinates)
        print("Translated Base Cordinates", translatedBaseCordinates)

#visualizeFrame(np.array([[5,7, 4, 4, 2, -np.pi/4, 'Car'],[-5,-7, 4, 7, 2, np.pi/4, 'Car']], dtype=object))
#drawBox( -4, -4, 4, 4 , 2, np.pi/4, False)