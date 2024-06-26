# SEGNet
### Automated Bone Segmenting and Rendering Application
![](https://img.shields.io/github/issues/saivishwak/SEGNet)
![](https://img.shields.io/github/forks/saivishwak/SEGNet)
![](https://img.shields.io/github/stars/saivishwak/SEGNet)
![](https://img.shields.io/badge/Python-3-blue)
![](https://img.shields.io/github/license/saivishwak/SEGNet)
![](https://img.shields.io/github/last-commit/saivishwak/SEGNet)
![](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)


# Introduction
SEGNet is an open-source, multi-platform bone segmentation and Dicom viewer with user-friendly interface. SEGNet provides ease in viewing Dicom data; Mouse integrations will help you to visualize Dicom in a detailed way. SEGNet utilizes combined power of image processing and computer vision for fast segmentation of bone from a CT Dicom data.

![Splash](./Images/splash.png)

# Developments need to be done

- Fullscreen mode for widgets
- Advanced surface properties

# Requirements
- VTK
- Pyqt5
- Opencv
- Numpy

Requirements can be dwonloaded as shown below:
    
    git clone https://github.com/hanaisreal/MedSAM-Dicom.git
    
    cd SEGNet
    
    pip3 install -r requirement.txt (For Linux add sudo)

# Running GUI

    cd SEGNet

    cd src

    python3 Main.py

Tested on Windows and Linux

## User Interface

    Dicom Widget:
    
    mouse_scroll - Change slice
    
    clrt + left_mouse_button - Pan

    clrt + mouse_scroll - Zoom

    mouse_right_button + drag - Contrast/Brightness

    r - Reset view

    3D Renderer:

    All basic mouse movements!

## [MIT License](https://raw.githubusercontent.com/saivishwak/SEGNet/master/LICENSE)
<img src ="https://img.shields.io/badge/Important-notice-red" />
<h4>You can use it absolutely anywhere!</h4>

Feel free to make a pull request if you feel that you have to improve this tool
