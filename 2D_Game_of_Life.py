import numpy as np
import matplotlib.pyplot as plt


def initLattice(m,n):
    return np.random.randint(0,2,(m,n)) 


def periodicLat(lat):
    m = lat.shape[0]
    n = lat.shape[1]
    first_row = np.copy(lat[0,:]).reshape(1,n)
    last_row = np.copy(lat[m-1,:]).reshape(1,n)
    lat2 = np.concatenate((last_row, lat, first_row), axis = 0)
    m2 = lat2.shape[0]
    n2 = lat2.shape[1]
    first_col = np.copy(lat2[:,0]).reshape(m2, 1)
    last_col = np.copy(lat2[:, n2-1]).reshape(m2, 1)
    periodic_lat = np.concatenate((last_col, lat2, first_col), axis = 1)
    return periodic_lat


def transitionRule(site, E, W, N, NE, NW, S, SE, SW):
    neighbors = [E, W, N, NE, NW, S, SE, SW]
    if site == 1:
        if sum(neighbors) > 3 or sum(neighbors)<2:
            site = 0
    if site == 0:
        if sum(neighbors) == 3:
            site = 1
    return site


def applyRule(barExt):
    for i in range(1, m+1):
        for j in range(1, n+1):
            site = barExt[i,j]
            E = barExt[i,j+1]
            W = barExt[i, j-1]
            N = barExt[i-1, j]
            NW = barExt[i-1, j-1]
            NE = barExt[i-1, j+1]
            S = barExt[i+1, j]
            SW = barExt[i+1, j-1]
            SE = barExt[i+1, j+1]
            new_site = transitionRule(site, E, W, N, NE, NW, S, SE, SW)
            barExt[i,j] = new_site
    new_bar = barExt[1:m+1, 1:n+1]
    return new_bar


def gameOfLife(m,n,nstep):
    bar = initLattice(m,n)
    grid = [bar]
    for i in range(nstep):
        bar_ext = periodicLat(bar)
        bar = applyRule(bar_ext)
        grid.append(bar)  
    return grid

m = 10
n = 10
nstep = 12
grid = gameOfLife(m,n, nstep)
fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12)) \
    = plt.subplots(3, 4, sharex=True, sharey = True, figsize = (12,6))
axs = [ax1,ax2,ax3,ax4,ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12]

#PLOTTING
for i in range(nstep):
    lat = grid[i]
    axs[i].imshow(lat, cmap='Greys', interpolation = 'nearest')
    axs[i].set_title('Grid at t={}'.format(i), fontsize = 8)

plt.savefig('gameOfLife.png')

    