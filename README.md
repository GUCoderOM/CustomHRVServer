## HRVServer Sensor Tracking System
This repository contains the instructions on how to run the HRVServer Sensor Tracking System.

Requirements
Android Studio
Ticwatch Pro 3 GPS
Anaconda Prompt
Setup
Launch Android Studio and open the SensorTracker project
Connect the Ticwatch Pro 3 GPS to the device which will run the SensorTracker by connecting it to the same WiFi as the device
Run the following command on the Android Studio terminal:

'''
platform-tools/adb.exe connect [watch ip address]:5555
'''

Note: Replace the watch IP address with the IP address of the watch that is displayed in the settings of the watch once the watch is connected to the WiFi.

Locate the MainActivity.kt file and find the URL's apiurl and userurl. They both share the same start : http://192.168.137.1:5555/hrv/
Replace 192.168.137.1 with the IP address of the laptop because the HRVServer is running on the local network.
Launch a command prompt such as Anaconda prompt and open the directory of the HRVServer
Install all the requirements and run the following commands:

'''
python manage.py makemigrations
python manage.py migrate
python populate_HRVServer.py
python manage.py runserver 0.0.0.0:5555
'''

Data should now flow and be saved onto the UserProfile Yousuf that has a password "y" for purposes of simplicity.
