# This document is for description for each phantom file

## Main files are phantom_3, phantom_6, phantom_7, and phantom_9


### phantom_3

This iteration generates a 1D phantom, a 1D kspace and encoding matrix using discrete fourier transforms equations. There are three phantom options which are commented so you can pick and choose which phantom you want to use. 

There are two ways that the image is reconstructed. 

1. The first method is done by multiplying the inverse fourier of the encoding matrix with the kspace to produce our 1D image. This method will produce some gibbs ringing in the recontructed image. 

2. The second method for reconstruction is done by inputing the kspace vector and the encoding matrix into the lsqr function which will output the reconstructed 1D image. 

### phantom_4 

This is a test recon file for understanding what the 1D kspace looks like by using a numpy fft function.

### phantom_6

A 2D version of phantom 3. We input a 2D shepp-logan array as our phantom, generates a 2D kspace, and finally recontructs the image using fourier and lsqr techniques. Specially for the LSQR, we make project the 4D tensor onto a 2D matrix and plug that in the LSQR library with the kspace vector which is created by stacking the columns of the matrix.

### phantom_7

Same as phantom 6, we create a 2D shepp-logan array but also load a B0 field map. We create a kspace and reconstruct the image using fourier methods. We can see distortion from the B0 inhomogineities. 

### phantom_8

Testing out 3D phantom... Not working on it until I finish the 2D version first

### phantom_9

Redefining how I make the kspace and replacing the time length which a metric based on the size of kspace in that particular direction. This allows for under and over sampling.

### phantom_10

Description soon to be added
