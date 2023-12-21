import pandas as pd
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Read data from CSV
data = pd.read_csv('data.csv').to_dict('records')

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter([], [], c='blue')  # Set a single color

# Set labels for each axis
ax.set_xlabel('X Axis Label')
ax.set_ylabel('Y Axis Label')
ax.set_zlabel('Z Axis Label')
ax.set_title('3D Animated Scatterplot')

# Update function for animation
def update(frame):
    ax.cla()  # Clear the previous frame
    ax.set_xlabel('X Axis Label')
    ax.set_ylabel('Y Axis Label')
    ax.set_zlabel('Z Axis Label')
    ax.set_title('3D Animated Scatterplot')
    
    # Plot all points up to the current frame
    pos_values = [json.loads(d['pos']) for d in data[:frame + 1]]
    pos_values = list(zip(*pos_values))
    ax.scatter(pos_values[0], pos_values[1], pos_values[2], c='blue')  # Set a single color

# Animate the scatter plot
for frame in range(len(data)):
    update(frame)
    display_speed = 0.125
    plt.pause(display_speed)  # Adjust the pause duration as needed

plt.show()


#import pandas as pd
#import json
#import numpy as np

#data = pd.read_csv('data.csv').to_dict('records')
#print(json.loads(data[0]['pos'])[0])
#print(json.loads(data[0]['pos'])[1])
#print(json.loads(data[0]['pos'])[2])



#df = pd.read_csv('data.csv').sample(20)
#print(df.pos.apply(lambda x: json.loads(x)[1]))
#print('\n')
#print(df.pos.apply(lambda x: np.array(x)[1]))