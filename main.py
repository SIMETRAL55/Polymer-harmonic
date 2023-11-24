import math
import numpy as np
import matplotlib.pyplot as plt

# Defining some parameters
k = 0.5 # spring const
h = 0.01  # 3 point h
a, b, N = 0.0, 50.0, 1000  # time
h1 = (b - a) / float(N)  # euler
m = 1.0  # massS
    

# Defining potential function note the x is distance between 2 adjacent beads and y is distance from x axis.
def Potential(x, y):
    return 0.5*k*(math.sqrt(x*x + y*y) - 1)**2
    
# Defining force using 3 point midpoint formula. When considering force in x direction we introduce h in only x keeping y constant.
def Force_x(x, y):
    return (Potential(x-h, y) - Potential(x+h, y)) / (2*h)

# When considering force in y direction we introduce h in only y keeping x constant.
def Force_y(x, y):
    return (Potential(x, y-h) - Potential(x, y+h)) / (2*h)
    
# This function will return an array(F_x) which contain the force(x directional force) on each beads
def forceTotal_x(X, Y, F_x):
    global n
    for i in range(n):
        if i == 0:
            if X[1] > X[0]:
                F_x[0] = (-1) * Force_x(X[1] - X[0], Y[1] - Y[0])
            else:
                F_x[0] = Force_x(X[1] - X[0], Y[1] - Y[0])
        elif i == n - 1:
            if X[n - 1] > X[n - 2]:
                F_x[n-1] = Force_x(X[n-1] - X[n-2], Y[n-1] - Y[n-2])
            else:
                F_x[n-1] = (-1) * Force_x(X[n-1] - X[n-2], Y[n-1] - Y[n-2])
        else:
            if X[i] < X[i+1] and X[i-1] < X[i]:
                F_x[i] = Force_x(X[i] - X[i-1], Y[i] - Y[i-1]) - Force_x(X[i+1] - X[i], Y[i+1] - Y[i])
            elif X[i] < X[i + 1] and X[i - 1] > X[i]:
                F_x[i] = (-1) * (Force_x(X[i] - X[i-1], Y[i] - Y[i-1]) + Force_x(X[i+1] - X[i], Y[i+1] - Y[i]))
            elif X[i] > X[i + 1] and X[i - 1] < X[i]:
                F_x[i] = Force_x(X[i] - X[i-1], Y[i] - Y[i-1]) + Force_x(X[i+1] - X[i], Y[i+1] - Y[i])
            else:
                F_x[i] = (-1) * (Force_x(X[i] - X[i-1], Y[i] - Y[i-1]) - Force_x(X[i+1] - X[i], Y[i+1] - Y[i]))
    return F_x

# This function will return an array(F_y) which contain the force(y directional force) on each beads
def forceTotal_y(X, Y, F_y):
    global n
    for i in range(n):
        if i == 0:
            if Y[1] > Y[0]:
                F_y[0] = (-1) * Force_y(X[1] - X[0], Y[1] - Y[0])
            else:
                F_y[0] = Force_y(X[1] - X[0], Y[1] - Y[0])
        elif i == n - 1:
            if Y[n - 1] > Y[n - 2]:
                F_y[n-1] = Force_y(X[n-1] - X[n-2], Y[n-1] - Y[n-2])
            else:
                F_y[n-1] = (-1) * Force_y(X[n-1] - X[n-2], Y[n-1] - Y[n-2])
        else:
            if Y[i] < Y[i+1] and Y[i-1] < Y[i]:
                F_y[i] = Force_y(X[i] - X[i-1], Y[i] - Y[i-1]) - Force_y(X[i+1] - X[i], Y[i+1] - Y[i])
            elif Y[i] < Y[i + 1] and Y[i - 1] > Y[i]:
                F_y[i] = (-1) * (Force_y(X[i] - X[i-1], Y[i] - Y[i-1]) + Force_y(X[i+1] - X[i], Y[i+1] - Y[i]))
            elif Y[i] > Y[i + 1] and Y[i - 1] < Y[i]:
                F_y[i] = Force_y(X[i] - X[i-1], Y[i] - Y[i-1]) + Force_y(X[i+1] - X[i], Y[i+1] - Y[i])
            else:
                F_y[i] = (-1) * (Force_y(X[i] - X[i-1], Y[i] - Y[i-1]) - Force_y(X[i+1] - X[i], Y[i+1] - Y[i]))
    return F_y

# Defining euler method which calculate the velocity and position
def euler(X, Y, Vx, Vy, F_x, F_y):
    global N, m, lengthArray, n, lengthArray, equ
    for t in range(N):
        if t == 0: #for t=0 means at initial time means at starting we know the position and velocity(0 vel) and we just calculate force
            F_x = forceTotal_x(X, Y, F_x)
            F_y = forceTotal_y(X, Y, F_y)
            lengthArray.append(math.sqrt((X[n-1] - X[0])**2 + (Y[n-1] - Y[0])**2))  # Inserting the r = sqrt(x*x + y*y) in lengthArray array
        else: #for other time we calculate both velocity, distance & force
            for i in range(n):
                X[i]=X[i]+(h1*Vx[i])+(((h1*h1)*(F_x[i]/m))/2)
                Vx[i]=Vx[i]+(h1*(F_x[i]/m))
                F_x=forceTotal_x(X,Y,F_x)
                Y[i]=Y[i]+(h1*Vy[i])+(((h1*h1)*(F_y[i]/m))/2)
                Vy[i]=Vy[i]+(h1*(F_y[i]/m))
                F_y=forceTotal_y(X,Y,F_y)
            lengthArray.append(math.sqrt((X[n-1] - X[0])**2 + (Y[n-1] - Y[0])**2))  # Inserting the r = sqrt(x*x + y*y) in lengthArray array
            
nbeads = [5, 10, 20] #Defining the number of beads as given in the question. Question - given that calculate the end to end distance for the 5, 10, & 20 beads.
equ = []  #Defining and equilibrium array which will store the mean of each array (i.e the mean of the lengthArray array for 3 case (5, 10, 20 beads))
for nb in range (3): # Loop to iterate over nbead array which store the number of beads(3 cases) and call the euler function to calculate the lengthArray and then plot the end to end distance (obtained by substracting the extreme index of lengthArray) vs time
    # Defining the required arrays and parameters
    lengthArray = []
    n = nbeads[nb]
    F_x = np.zeros(n, dtype='float32')
    F_y = np.zeros(n, dtype='float32')
    X = np.arange(n, dtype='float32')
    Y = np.zeros(n, dtype='float32')
    Vx = np.zeros(n, dtype='float32')
    Vy = np.zeros(n, dtype='float32')
    hy = 0.1 
    hx = 0.1
    # Introducing the small perturbation(i.e moving the beads from mean positions) in the last bead both in x and y direction
    X[n-1] = X[n-1] + hx
    Y[n-1] = Y[n-1] + hy
    euler(X, Y, Vx, Vy, F_x, F_y) # Calling euler function 
    equ.append(np.mean(lengthArray))
    # Defining the time array, which will store the time unit at which the end to end distance is calculated, for plotting the graph
    time = np.zeros(N, dtype = 'float32')
    for i in range(N):
        time[i] = i*h1
    
    # Plotting the End to End Distance vs Time graph
    plt.plot(time, lengthArray, color = 'green')
    plt.xlabel('Time')
    plt.ylabel('End to End Distance of Polymer')
    plt.title('Number of Beads'+ ' = ' +str(n))
    plt.show()

# Plotting the equilibrium length vs number of beads graph
plt.scatter(equ, nbeads, color = 'green', marker = 'o')
plt.plot(equ, nbeads, color = 'green')
# Below 2 lines of code is responsible for the representation of coordinate on the plot
for i_x, i_y in zip(equ, nbeads): 
    plt.text(i_x, i_y, '({:0.2f}, {})'.format(i_x, i_y))

plt.xlabel('Equilibrium Length')
plt.ylabel('Number of Beads')
plt.title('Equilibrium length vs Number of Beads')
plt.show()
