# MTJ - ICT720 Project
Team-working on AIoT Software Development Project

## Domain: Automatic Park Lighting 
## Stakeholder
1.  Park management staff

## Hardware
1. LILYGO T-SIMCAM ESP32-S3
2. ESP WROOM-32
3. LDR Light-Sensor Module
4. 5mm LED
   
## User Stories and Acceptance Criteria

- As a park staff, I want to automate the park's lighting system to optimize energy consumption based on daylight conditions.

  AC #1: I want the system to autonomously adjust the brightness of park lights or control their on/off status based on readings from specialised sensors that measure the current ambient light conditions.
      
  AC #2: I want the system to accumulate and store historical data regarding light levels, and operational functionality.
      
  AC #3: I want to utilize this information for park management to study system usage, identify improvement opportunities, and establish more efficient lighting schedules.
      
  AC #4: I want to be notified the moment an issue arises in the lighting system, minimizing downtime and ensuring fast resolution.

- As a park staff, I want to monitor crowd situations so that I can identify popular spots.

  AC #1: I want to monitor crowd density in real-time.
      
  AC #2: I want to identify popular areas within the park during specific times. Use this information to suggest optimal locations and timings for events and activities.
      
  AC #3: I want to modify the lighting intensity during nighttime when there is an increased crowd density, with the primary goal of ensuring safety.

## Overview

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/98aab676-9f42-4344-a8dc-64c4f8c607e8)


We combined different devices to develop an integrated system that combines smart lighting and crowd management functionalities in the park. This system utilizes camera and light-related sensors to achieve its objectives.The crowd management component involves the deployment of an AI model, which is uploaded to the camera board (ESP32-S3) for crowd detection both during the day and at night.
Simultaneously, the smart lighting system leverages LDR sensors and LED lights. It works in tandem with the crowd detection system on the cameras to dynamically adjust lighting levels in the park. During periods of increased crowd activity, particularly at night, the system enhances lighting to ensure better visibility and safety.


## System Architecture


## Flowchart
  
  
   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/3b3c5f75-3d79-40e5-8893-2ca0cb19aba4)
   

## Sequence diagram


   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/84bed13c-472d-4afc-832a-75b39fb2ec28)


## Data flow
  

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/d9ca2f64-d08f-4a67-8715-e5fd4dc98f28)
   

## Data modeling class diagram
  

   ![Lec 05](https://github.com/CHIMAI-A/MTJ/assets/64695311/0abe512b-a569-4724-96e0-c271781d8026)


## Camera - AI Model Development

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/44266252-82f3-4558-834c-a6e03456be87)
   
Demonstration #1

https://github.com/CHIMAI-A/MTJ/assets/146721485/bfb0f932-c674-40bb-a74c-2cb126dc07f3

1. Collecting Images
   
In this step, we upload the code and build the code. After success, we Run the Python file and the screen will display the output as shown below including the following contents:
   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/8580a918-6b9d-4c0c-baad-8215121e3b37)

The application should display a list of available serial ports when you run it. Clicking "Connect" should establish a connection to the selected port (assuming the ESP32 camera is connected). Clicking "Grab" will capture an image from the ESP32 camera and display it in the preview label. Clicking and dragging on the preview image will create a bounding box selection around the area you drag over. Clicking "Upload" will send the captured image and bounding box data to your Edge Impulse project for training.

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/59123983-d96f-42a0-9c87-9d7d30a3c509)

Reference Code: https://github.com/vsupacha/ict720-project-2024/tree/main/examples/tgr2023_06_imglabel

Next, we collected images using the ESP32-S3 camera by uploading the code that was provided (please see reference) in class. This code was used to capture images of people in different light conditions and send them to the Edge Impulse dataset by using the API key provided by Edge Impulse. The total number of images that were collected was 126 images.

   ![Automatic_Lighting_System](https://github.com/CHIMAI-A/MTJ/assets/146721485/67474e8e-8608-464c-b022-f4d0641acd6d)

2. Labeling Images

For this step, labeling was done manually on the Edge Impulse website. After labeling the images, the dataset was divided into training and testing data with a ratio of 8:2
   
   ![Label ](https://github.com/CHIMAI-A/MTJ/assets/146721485/c97e7707-e915-4cd4-a49f-6fdb1386567b)

3. Designing Impulse

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/3890bd8d-3d37-453c-a789-4227414ba917)
   


   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/b1e9b5ba-0c6a-4401-b0ca-cd09103020ae)
   


   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/3ecc58ea-c1cb-4395-aeb0-bd52420fff25)


5. Testing Model

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/04624a7e-f843-4fef-9c1c-68f704eecf05)

6. Deploying Model

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/fa9bde5b-7d7e-4334-8e82-04f28e33944a)


   Build camera

https://github.com/CHIMAI-A/MTJ/assets/146721485/75a1c149-d433-472e-85e4-0a519bd32872

   Upload camera

https://github.com/CHIMAI-A/MTJ/assets/146721485/04d46723-8555-4476-95ba-b9bc5027ec7f

   Serial monitor camera

https://github.com/CHIMAI-A/MTJ/assets/146721485/b0c83434-5d29-4afa-9e97-6da709721e3d


## Light System Development 

![image](https://github.com/CHIMAI-A/MTJ/assets/64695311/5b70659b-e8bc-4589-b084-74344eacdd80)

1. Wiring diagram between LDR light-sensor module

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/1b4dbd76-96b0-4f04-b0e7-3c28f0afd3ff)

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/052e62bd-3e14-4e3a-ac7a-1cd2789058fb)

2. MongoDB

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/78de7f32-bf6f-4577-a450-fd84b627a46e)
   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/bc359b7e-e3bd-40c4-a61c-c693df5e2e32)


# Members
   - Miss Thi Chi Mai Le 6622040290

   - Mr.  Than Zaw Win 6622040654

   - Miss Joanna Sophie Abraham 6614552643
