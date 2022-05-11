import numpy as np
from skimage import io, img_as_ubyte

def combine(a,b,c,d):
    out = np.zeros((a.shape[0],a.shape[1], 4), dtype=np.ubyte)

    out[:,:,0][a[:,:,3] > 0] = a[:,:,0][a[:,:,3] > 0]
    out[:,:,1][b[:,:,3] > 0] = b[:,:,0][b[:,:,3] > 0]
    out[:,:,2][c[:,:,3] > 0] = c[:,:,0][c[:,:,3] > 0]
    out[:,:,3][d[:,:,3] > 0] = d[:,:,0][d[:,:,3] > 0]

    return out

a = img_as_ubyte(io.imread('a.png'))
b = img_as_ubyte(io.imread('b.png'))
c = img_as_ubyte(io.imread('c.png'))
d = img_as_ubyte(io.imread('d.png'))

img = combine(a,b,c,d)

io.imsave('grid.png', img)

# e = img[:,:,0]
# f = img[:,:,1]
# g = img[:,:,2]
# h = img[:,:,3]

# io.imsave('e.png', e)
# io.imsave('f.png', f)
# io.imsave('g.png', g)
# io.imsave('h.png', h)
