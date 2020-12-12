import numpy as np
import scipy.misc
import matplotlib.pyplot as plt

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def fractal_dimension(Z):
    threshold=np.mean(Z)
    # Only for 2d image
    assert(len(Z.shape) == 2)

    def boxcount(Z, k):
        S = np.add.reduceat(
            np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
                               np.arange(0, Z.shape[1], k), axis=1)

        # We count non-empty (0) and non-full boxes (k*k)
        return len(np.where((S > 0) & (S < k*k))[0])

    # Transform Z into a binary array
    Z = (Z < threshold)

    # Minimal dimension of image
    p = min(Z.shape)

    # Greatest power of 2 less than or equal to p
    n = 2**np.floor(np.log(p)/np.log(2))

    # Extract the exponent
    n = int(np.log(n)/np.log(2))

    # Build successive box sizes (from 2**n down to 2**1)
    sizes = 2**np.arange(n, 1, -1)

    # Actual box counting with decreasing size
    counts = []
    for size in sizes:
        counts.append(boxcount(Z, size))

    # Fit the successive log(sizes) with log (counts)
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)

    fig, ax = plt.subplots(tight_layout=True)
    xs = np.log(sizes) # size of cells (e)
    ys = np.log(counts) # number of cells
    ax.plot(xs, ys, 'o', label='screenshot.jpg')
    xs = xs[1:]
    ys = ys[1:]
    A = np.vstack([xs, np.ones(len(xs))]).T
    m,b = np.linalg.lstsq(A, ys, rcond=None)[0]
    def line(x): return m*x+b
    ys = line(xs)
    ax.plot(xs, ys, label='a*x+b')
    plt.text(0.35, 0.93,'Fractal dimension: ' + str(round(-coeffs[0], 2)), transform=ax.transAxes)
    ax.legend()

    return -coeffs[0]

def show():
    I = rgb2gray(scipy.misc.imread("screenshot.jpg"))
    print("Minkowski dimension(box-counting dimension): ", fractal_dimension(I))
    #plt.show()

if __name__ == '__main__':
    show()
