# OTA-PVR_Alexa
This is an Alexa skill to communicate with my USB TV tuner card connected to my PC. It allows me to send voice commands to Alexa to record TV broadcasts.

I currently am running Windows 10 Professional with a Hauppauge WINTV-HVR-995Q USB TV tuner. I wanted to create an Amazon Alexa skill that would communicate with the TV tuner card and schedule to record shows at certain times. Currently, the lambda_function.py is the lambda function that I have running on Amazon AWS and connected to my Alexa skill. Alexa will recgonize my record intent when I specify what channel I want to record on, the date, the time, and the duration (in seconds). This information is send to the other python program which is running as a server on the Windows machine with the TV tuner card. It schedules calling the WinTVRec.exe (program came with the tuner card) with the appropriate parameters. The TV channel number is that specified by the tuner card and doesn't correspond to the virtual channel number. 

In order to use this Alexa skill:
1. The user must first run the python server on the computer with TV tuner card and have the software installed that came with the Hauppage card (WINTV). The installed files must be in the default path. 
2. Next the user must configure his or her router to set up port forwarding to have TCP packets arriving on port 9998 to go to port 9998 on the local machine hosting the python server with the TV tuner card. Please consult your router's manual if you don't know how to do this.
3. You must then tell the Alexa skill your public IP address by something like "Alexa, tell TV recorder my internet protocol address is zero dot zero dot zero dot zero."
4. Now you can tell Alexa what you want to record by stating the channel, time, date, and duration. If you don't specify all of these parameters at once, Alexa will walk you through a conversation which will prompt you for all of the information that she needs. For example, you can say, "Alexa record channel 1101." Alexa will then respond something similar to, "At what should I record?"

TODO:
I would like to create the program so that Alexa doesn't need to know the IP address of the local server. I would also like to translate the channel numbers specified by the tuner card into the virtual channel numbers.
