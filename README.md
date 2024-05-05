# MTJ
Team-working on AIoT Software Development Project

## Domain: Automatic Park Lighting 
## Stakeholder
1.  Park management staff

## Hardware
1. LILYGO T-SIMCAM ESP32-S3
2. ESP WROOM-32
3. LDR Light-Sensor Module
4. 5mm LED
   
   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/22e59ff4-84b8-48f0-b5d1-8182098f0f84)


## Overview

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/98aab676-9f42-4344-a8dc-64c4f8c607e8)


We combined different devices to develop an integrated system that combines smart lighting and crowd management functionalities in the park. This system utilizes camera and light-related sensors to achieve its objectives.The crowd management component involves the deployment of an AI model, which is uploaded to the camera board (ESP32-S3) for crowd detection both during the day and at night.
Simultaneously, the smart lighting system leverages LDR sensors and LED lights. It works in tandem with the crowd detection system on the cameras to dynamically adjust lighting levels in the park. During periods of increased crowd activity, particularly at night, the system enhances lighting to ensure better visibility and safety.

   
## User Stories

- As a park staff, I want to automate the park's lighting system to optimize energy consumption based on daylight conditions.

AC #1: I want the system to autonomously adjust the brightness of park lights or control their on/off status based on readings from specialised sensors that measure the current ambient light conditions.

AC #2: I want the system to accumulate and store historical data regarding light levels, and operational functionality.

AC #3: I want to utilize this information for park management to study system usage, identify improvement opportunities, and establish more efficient lighting schedules.

AC #4: I want to be notified the moment an issue arises in the lighting system, minimizing downtime and ensuring fast resolution.

- As a park staff, I want to monitor crowd situations so that I can identify popular spots.

AC #1: I want to monitor crowd density in real-time.

AC #2: I want to identify popular areas within the park during specific times. Use this information to suggest optimal locations and timings for events and activities.

AC #3: I want to modify the lighting intensity during nighttime when there is an increased crowd density, with the primary goal of ensuring safety.


## System Architecture

- Flowchart
  
   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/3b3c5f75-3d79-40e5-8893-2ca0cb19aba4)


- Sequence diagram

   ![image](https://github.com/CHIMAI-A/MTJ/assets/64695311/abd5858f-9554-40e8-b7db-47d11825e389)

- Data flow

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/d9ca2f64-d08f-4a67-8715-e5fd4dc98f28)


- Data modeling class diagram

   ![Lec 05](https://github.com/CHIMAI-A/MTJ/assets/64695311/0abe512b-a569-4724-96e0-c271781d8026)

## Camera - AI Model Development

   ![image](https://github.com/CHIMAI-A/MTJ/assets/146721485/44266252-82f3-4558-834c-a6e03456be87)


# Members
Miss Thi Chi Mai Le 6622040290

Mr.  Than Zaw Win 6622040654

Miss Joanna Sophie Abraham 6614552643
