Computer Vision Pipeline for Precision Agriculture 

A robust computer vision module designed for intelligent pesticide application. This pipeline processes visual data to identify target zones (such as weeds or diseased crops) in real-time, acting as the primary perception system for an autonomous agricultural rover.

Overview
This repository contains the standalone vision subsystem for the agricultural sprayer project. Developed and tested in a Windows environment, the model utilizes OpenCV and YOLOv8 (via PyTorch) to achieve high-accuracy, real-time inference. The system is engineered to eventually output target coordinates that will guide a 6-DOF robotic manipulator mounted on a differential-drive rover.

Tech Stack
* Language:Python 3.x
* Computer Vision: OpenCV
* Deep Learning Framework: PyTorch, YOLOv8
* Development Environment: Windows 10/11

Installation & Setup (Windows)

1. Clone the repository:
   Open your Command Prompt or PowerShell and run:
   ```cmd
   git clone [https://github.com/yourusername/agri-sprayer-vision.git](https://github.com/yourusername/agri-sprayer-vision.git)
   cd agri-sprayer-vision
2. Create a virtual environment:
  It is highly recommended to use a virtual environment to manage dependencies.

    ```terminal
    python -m venv venv

3. Activate the virtual environment:

    ```terminal
    venv\Scripts\activate
4. Install dependencies:
  Ensure your virtual environment is active, then install the required packages:

    ```terminal
    pip install -r requirements.txt
5.To run the web-based inference script:

  ```terminal
  python web_inference.py
