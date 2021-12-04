# Bayer Image Viewer

Viewing Bayer format images is a problem with professional photographers and camera engineers face everyday. There are some tools which help solve the issue a bit. However, most of these solutions/tools are designed by the camera manufacturers and only support their own format. Viewing RAW images without header is a bigger issue and there are very few tools which have this feature. 

An inherent problem with header-less RAW images is the fact that there is no information about the width and height. Formats like JPEG, PNG carry this information and thus it is very easy to view these images one after the other. 

This tool was designed to overcome the above problem by asking the user the image dimensions before hand. 

I admit, this tool solves a few problems, not all.

## Setup

- You should have any version of Python3 installed on your system.
- Set up a virtual environment.
'''
python3 -m venv bayer-env
'''
- Install the required libraries
'''
pip install numpy=1.21.1
pip install PyQt5
'''
- 
