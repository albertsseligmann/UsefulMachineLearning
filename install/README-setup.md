
##  WARNING: UNTESTED
---

### -- Instructions for setup of object detection environment --

Installs NVIDIA Driver 418.56 (based on GTX 1080 usage, if another GPU is used -> update install_NVDriver to get recommended driver), NVIDIA CUDA 10.1, NVIDIA cuDNN 7, CMake, OpenCV 3.4.5 and the latest modified darknet version.


---
### -- Requirements --

Ubuntu 16.04 LTS
NVIDIA GPU with Compute Capability greater than 3.0 (Google it)


---
### -- Installation (should probably be tested and updates :-) ) --

Do the following **IN-ORDER**
1. Move install_\*, cuda-repo-\*, libcudnn7_\* and libcudnn7-dev_\* to the Home folder (~), and open a terminal
2. `cd`
3. `sudo sh ./install_NVDriver`
4. Reboot (`sudo reboot`)
5. `sudo sh ./install_CUDA`
6. Reboot (`sudo reboot`)
7. `sudo sh ./install_cuDNN`
8. `sudo sh ./install_cURL`
9. `sudo sh ./install_CMake` or `sudo sh ./install_CMake_test`
10. `sudo sh ./install_OpenCV`
11. `sh ./install_darknet`
12. `cd ../darknet/`
13. `cmake . && make`


(Old: 
- Change line `if (i >= (iter_save + 1000) || i % 1000 == 0)` to `if (i >= (iter_save + 100) || i % 100 == 0)` in file `darknet/src/detector.c` (Probably line 271)
- Consider changing `draw_detections_v3` (probably line 339) and `get_label_v3` function in file `darknet/src/image.c` (probably line 123), to alter bounding box and label size on prediction image. For video consider changing `draw_detections_cv_v3` (width = 2; on line 884 and comment out lines 973-977) function in file `darknet/src/image_opencv.cpp`, to alter bounding box and label size on prediction image.
- `nano Makefile`
- Set `GPU=1`, `CUDNN=1`, `OPENCV=1` and `OPENMP=1`)

In Makefile set: 
```
GPU=1
CUDNN=1
CUDNN_HALF=0
OPENCV=1
AVX=1
OPENMP=1
LIBSO=1
ZED_CAMERA=0 # ZED SDK 3.0 and above
ZED_CAMERA_v2_8=0 # ZED SDK 2.X

# set GPU=1 and CUDNN=1 to speedup on GPU
# set CUDNN_HALF=1 to further speedup 3 x times (Mixed-precision on Tensor Cores) GPU: Volta, Xavier, Turing and higher
# set AVX=1 and OPENMP=1 to speedup on CPU (if error occurs then set AVX=0)

USE_CPP=0
DEBUG=0

ARCH= -gencode arch=compute_30,code=sm_30 \
      -gencode arch=compute_35,code=sm_35 \
      -gencode arch=compute_50,code=[sm_50,compute_50] \
      -gencode arch=compute_52,code=[sm_52,compute_52] \
	  -gencode arch=compute_61,code=[sm_61,compute_61]

OS := $(shell uname)

# Tesla V100
# ARCH= -gencode arch=compute_70,code=[sm_70,compute_70]

# GeForce RTX 2080 Ti, RTX 2080, RTX 2070, Quadro RTX 8000, Quadro RTX 6000, Quadro RTX 5000, Tesla T4, XNOR Tensor Cores
# ARCH= -gencode arch=compute_75,code=[sm_75,compute_75]

# Jetson XAVIER
# ARCH= -gencode arch=compute_72,code=[sm_72,compute_72]

# GTX 1080, GTX 1070, GTX 1060, GTX 1050, GTX 1030, Titan Xp, Tesla P40, Tesla P4
ARCH= -gencode arch=compute_61,code=sm_61 -gencode arch=compute_61,code=compute_61

# GP100/Tesla P100 - DGX-1
# ARCH= -gencode arch=compute_60,code=sm_60

# For Jetson TX1, Tegra X1, DRIVE CX, DRIVE PX - uncomment:
# ARCH= -gencode arch=compute_53,code=[sm_53,compute_53]

# For Jetson Tx2 or Drive-PX2 uncomment:
# ARCH= -gencode arch=compute_62,code=[sm_62,compute_62]
```
