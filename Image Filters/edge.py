import numpy as np
import pyopencl as cl
from PIL import Image
from time import time

def getKernel(krnl):
    kernel = open(krnl).read() #Create kernel object
    return kernel 


def findedges(p,d,image): #Edge detection function

    data = np.asarray(image).astype(np.uint32) #Read image as numpy array
    #Setup OpenCL device on Host
    platform = cl.get_platforms()[p] 
    device = platform.get_devices()[d]
    cntx = cl.Context([device])
    queue = cl.CommandQueue(cntx)
    #Create memory buffers
    mf = cl.mem_flags
    im = cl.Buffer(cntx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
    out = cl.Buffer(cntx,mf.WRITE_ONLY,data.nbytes)
    #Create Kernel
    prgm = cl.Program(cntx,getKernel('edge.c')%(data.shape[1],data.shape[0])).build()

    prgm.detectedge(queue,data.shape,None,im,out)

    result = np.empty_like(data)
    #Move result to output queue
    cl.enqueue_copy(queue,result,out)
    result = result.astype(np.uint8)
    print(result)

    img = Image.fromarray(result)
    #Save filtered image
    img.save('img.png')


if __name__ == '__main__':
    image = Image.open('img2.png')
    #(1,0) for GPU  
    #(0,0) for intel processor 
    findedges(0,0,image) #choose device to be intel processor
 
