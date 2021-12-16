# IOT_Final_Project: Smart Personalized Window - Based on voiceprint recognition

Description：
---
The smart window uses voiceprint recognition to identify the users when sighed in, and automatically adjusts the window open/close status depending on the user preferences to the inside and outside weather conditions. The weather information containing temperature, humidity and wind speed is detected by the sensors. This data and window status is monitored in real time and displayed on out webapp.

Motivation:
---
1. Smart homes that include smart windows which are combined for security and comfort<br>
2. Adjust the indoor surroundings according to both indoor and outdoor weather<br>
3. Monitor and adjust the window while we are not home<br>
4. Incorporate personalization in the design of the smart windows</p>

Fetures:
---
● Use voiceprint recognition to identify the user <br>
● Set personal preference and user authentication for unique user <br>
● Adjust window open-close degree according to factors such as<br>
- Temperature<br> 
- Humidity<br> 
- Wind speed<br>

● Display real time monitoring data on the designed web-app</p>

Components：
---
<h4>Hardware<br></h4>
<p align="left">
● RaspberryPi<br>
● Feather Huzzah ESP8266<br>
● Sensors (dht11 humidity) (ds18b20 temperature) (Rev. P6 wind speed)<br>
● Motor (servo motor SG90)<br>
<br></p>
<h4>Software<br></h4>
<p align="left">
● Server mongoDB<br>
● Django (webpage layout, user authentication system, data visualization, front end and backend integration)<br>
● Voice print recognition<br>
● Socket Communication</p>

Results:
---
https://youtu.be/WjF8oAkQ9ns

Directory：
---
```./
├── raspberry pi
├── README.md
├── esp
└── webapp
