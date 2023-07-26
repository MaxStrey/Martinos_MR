# This document is for description for each phantom file

## Main files are phantom_3, phantom_6, phantom_7, and phantom_9


### phantom_1 and phantom_2 

Prehistoric tests from a time before knowledge and history, maybe even before life itself... Soon to be removed. Don't bother looking at them.

### phantom_3

This iteration generates a 1D phantom, a 1D kspace and encoding matrix using discrete fourier transforms equations. There are three phantom options which are commented so you can pick and choose which phantom you want to use. 

There are two ways that the image is reconstructed. 

1. The first method is done by multiplying the inverse fourier of the encoding matrix with the kspace to produce our 1D image. This method will produce some gibbs ringing in the recontructed image. 

2. The second method for reconstruction is done by inputing the kspace vector and the encoding matrix into the lsqr function which will output the reconstructed 1D image. 

### phantom_4 

This is a test recon file for understanding what the 1D kspace looks like by using a numpy fft function.

### phantom_5

Relic of a bygone era... Doesn't officially exist... Soon to be removed. Don't look at it

### phantom_6

A 2D version of phantom 3. We input a 2D shepp-logan array as our phantom which is resized to match the

### phantom_7

Description soon to be added

### phantom_8

Description soon to be added

### phantom_9

Description soon to be added

### phantom_10

Description soon to be added
