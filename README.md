# Temperature

Program for checking temperature of your video adapter. Won't work without config file, which include:
```
[Timing]

maximum_temperature = 64
#Maximum temperature for your rig

Time_to_send = 6
#How often will notifications be sent? (Seconds)

[User]

Mail = xxxxxxx@gmail.com
Password = xxxxxxxxx
#Mail to which notifications will come and from which they will be sent 
Developer_mode = 0
# 0 - off, 1 - on (This mode incrise all limits, but keep in mind, that program can crash with some variables)
```
Status reports are sent to the mail. Implemented control via telegram bot. 
