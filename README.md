# hydroponic control
the following files are used
-	hydro.service  	; configuration file for the damon service, which start the main script
-	main.py  		; main script
-	switches_gpio.py 	; controls the GPIO Output to send den Signals

## Quick test of service
send some signals to test basic function
```
- python3 rpi-rf_send.py -g 17 1377617
- python3 rpi-rf_send.py -g 17 1377620
```
check the damon status and the log of the service (/var/log/syslog)
```
systemctl status hydro.service
```
or check the damon configuration file 'hydro.service' is copied to the following destination
```
/etc/systemd/system/hydro.service
```
## Using 433MHz Transmitter
I'm using the modules from https://www.az-delivery.de/products/433-mhz-modul to controll the irrigation of my hydroponic. It's a simple approach which works fine for me
The modules are controlled via GPIO with the python modul https://pypi.org/project/rpi-rf/

## Coding of the 433MHz signals
The signal consists of 5 digits for the group adress, 5 digits for the switch adress and 2 digits for the action to do. Every digit is expressed as 2bit, therefore it's a 24bit signal
See also https://wiki.fhem.de/wiki/Intertechno_Code_Berechnung#Stellen_10-11_.28Ein.2FAus.29

Examples for different codes send for switch A:
```
- 00000 - 5588305 – 0101 0101 0100 0101 0101 0001
- 10000 - 1394001 – 0001 0101 0100 0101 0101 0001
- 01000 - 4539729 – 0100 0101 0100 0101 0101 0001
- 11000 – 345425  - 0000 0101 0100 0101 0101 0001
- 11111 – 1361    - 0000 0000 0000 0101 0101 0001
```

On/off examples for the group adress: 10001 and different switches:
```
- A: 1377617  - 1377620
- B: 1380689 - 1380692
- C: 1381457 - 1381460
- D: 1381649 – 1381652
```

here some examples decoded
```
- 1377617 - 0001 0101 0000 0101 0101 0001 = Group 10001 Switch A on
- 1377620 - 0001 0101 0000 0101 0101 0100 = Group 10001 Switch A off
- 1380689 - 0001 0101 0001 0001 0101 0001 = Group 10001 Switch B on
- 1380692 - 0001 0101 0001 0001 0101 0100 = Group 10001 Switch B off
```
