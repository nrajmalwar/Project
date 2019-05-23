# Architectural Basics

## Understanding Data

Before we start  building our model, it is very important that we understand our data. Without any knowledge on how our data looks like, it is pointless to think about what layers we should add. 

Firstly, we display a random batch of images from our dataset. We look at images from all the classes to get an idea of what kind of images each class contains and understand the details of the object (type, variations, size etc.). Then we do **image normalization [10]** in order to bring all the pixel values between 0 and 1. This is important because there could be some images where the pixel values are very skewed (for eg. some images can have 90% pixel values close to 255). We do not want our model to be biased towards any image based on shear intensity of the pixel.

## Building Basic Model Architecture - First Model

When we first start building our model, we use only the basic functions and build a vanilla model. We also overlook on some of the constraints we might have like number of parameters, training time, target validation accuracy etc. The aim of this simple model is to act as a good baseline to build a more complex model that solves our model.

We start by deciding the **number of layers [1]** our model will have based on the **Receptive Field [5]** of the object in our images. We start by adding **3x3 Convolution [4]** layers in the sequence of increasing channels and calculate the output size and receptive field alongside. Once the low level features are obtained (like edges, gradients or textures) we merge the channels of our kernels using a  **MaxPooling [2]** layers followed by a **1x1 Convolution [3]** to reduce the number of channels. This together is known as a Convolution Block and a Transition Block. We add several of these blocks till we reach an output image size of 9x9 or 7x7. After this point, adding a Convolution layer would convolve more number of times on the central pixels as compared to the boundary pixels. This is when we **stop Convolution and go ahead with a larger kernel or some other alternative [19].** 

We bring down the number of channels to the output number of classes using a 1x1 Convolution. We flatten this result and feed it to a **Softmax [6]** activation. Softmax creates a large separation between the final predictions which can be used by Backpropagation to learn faster. However, the results of a softmax function are only probability like and may not be suitable in some critical cases (like medical data). 

We compile the model and then **add validation checks [22]** while fitting the model. The validation checks are crucial and required to be added from the beginning because our model can behave very differently on the training and the test data. It can start overfitting from the very beginnning in some cases. We check the first two epochs of our model and **know whether the network is going well very early [20]**. The value of training/validation accuracy and also the gap between gives a fair idea of how this model is going to behave eventually. A network which starts with a low accuracy cannot be expected to pick up and have a higher accuracy than a network which has a higher accuracy to begin with.

## Overcome Parameter Contraints and Improve Architecture - Second Model