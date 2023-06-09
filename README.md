# free dog sdk

This should be a free version of the robodog go1 sdk. I was upset that the original sdk only comes in precompiled libs, so i started to write this. It is far from finished but it can be used to send highLevelCmds and lowLevelCmds to the Unitre** Go1 dogs (maybe other dogs too...).

The intention is to break free of the manufacturers restricitons. This SDK has proven to work on all Models of the Go1 Dog: Air, Pro, Max and Edu
The manufacturer claims that only the Edu dog can be controlled via the SDK, it was shown before that the Highlevel Commands can be used to control the non-Edu models, but with this SDK you can also use Lowlevel commands.

## Support 
Stop by "TheDogPound - Animal control for stray robot dogs" Slack group, and join #faux-level and #unitree for support assistance.
https://join.slack.com/t/robotdogs/shared_invite/zt-1fvixx89u-7T79~VxmDYdFSIoTnSagFQ

## Current State

The SDK is fully useable, however, it does currently not include any Safety features of the original SDK. Please feel free to contribute the Safety restrictions to the project! Also it might still include small bugs, if you see one, please fix it and do a PR ;)

## What do you need?

python3 and some modules, to install them you can use pip from within the project folder
```
pip install -r requirements.txt
```

## Configuration of the dog and the SDK
There are several configurations you can run. You can either run the script from any component inside the dog, or on an connected PC. It doesn't matter really, but you need to make sure to configure you dog accordingly and use the correct connection settings inside the SDK.
In our example we will connect the PC via WiFi to the Dogs Hotspot. Startup the dog and connect to the WiFi, the default Wifi password is of the Hotspot is 00000000

Now your PC should have the IP 192.168.12.14 and you should be able to reach the Dog via ping on 192.168.12.1. To run the Highlevel examples that is all what you need.

#### Configure the connection
Lets first take a look into the examples, they usually start with the imports and then they build an connection object like this:

```
conn = unitreeConnection(HIGH_WIFI_DEFAULTS)
```

The connection object uses either presets or self defined values to create an connection to the dog.
You can browse the preset in the file ucl\unitreeConnection.py:
```
listenPort = 8090
sendPort_low = 8007
sendPort_high = 8082
local_ip_wifi = '192.168.12.14'
local_ip_eth = '192.168.123.14'
addr_wifi = '192.168.12.1'
addr_low = '192.168.123.10'
addr_high = '192.168.123.161'
LOW_WIRED_DEFAULTS = (listenPort, addr_low, sendPort_low, local_ip_eth)
LOW_WIFI_DEFAULTS = (listenPort, addr_low, sendPort_low, local_ip_wifi)
HIGH_WIRED_DEFAULTS = (listenPort, addr_high, sendPort_high, local_ip_eth)
HIGH_WIFI_DEFAULTS = (listenPort, addr_wifi, sendPort_high, local_ip_wifi)
```

As you can see there are 4 presets defined, Low_Wired, Low_WiFi, High_Wired and High_WiFi
The listenPort is currently unused, in the current state the listenport is set automatically, no matter which value you put.
If you run another configuration (maybe inside the dog) you can create an own preset easily, you just need to call the connection Object like this:
```
MY_CUSTOM_SETTINGS = (LISTENPORT, 'IP.TO.SEND.TO', SENDPORT, 'MY.CURRENT.IP.ADDY')
conn = unitreeConnection(MY_CUSTOM_SETTINGS)
```

So if you connected via WiFi like described above, you should be able to use the WIFI_DEFAULTS for either High or Lowlevel (the examples come preconfigured for WiFi!)


### Highlevel Examples
There are three Highlevel examples included:

 - example_pushups(highlevel).py --> This will make the dog do pushups
 - example_rotate(highlevel).py --> This will make the dog rotate 90°
 - example_walk(highlevel).py --> This will run the same walk routing as the original SDK

Lets run one example:

 1. Connect to the dog via WiFi
 2. Make sure you own WiFi IP is 192.168.12.14 (the Dog should assign you this IP automatically!), if not change the connection object accordingly!
 3. Run the pushup example (it's stationary, so it is safest to use!)
```
python3 ./example_pushups(highlevel).py
```
If everything is working correctly you should see the dog doing pushups. Congratulations :)

### Lowlevel Examples
There are three Highlevel examples included:

 - example_position(lowlevel).py -> The dog will do positioning with the front right leg.
 - example_torque(lowlevel).py --> The dog will put a torque to the front right leg, you can try to push against the torque to see it in action. (Don't go too hard!)
 - example_velocity(lowlevel).py--> The dog will control the velocity of the front left leg.

#### Prerequisite to be able to run the Lowlevel commands via WiFi

> Execute the following code on the robot's Raspberry Pi：
```
sudo vi /etc/sysctl.conf
```
Remove the comment in front of net.ipv4.ip_forward=1
```
sudo sysctl -p
sudo iptables -F
sudo iptables -t nat -F
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan1 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan1 -j ACCEPT
```
Do the following on your own laptop：
```
sudo route add default gw 192.168.12.1
```

After that your can run the Lowlevel examples via WiFi!

#### Run the Lowlevel Example
To communicate to the dog via Lowlevel you need to put the dog into Lowlevel mode first. This will make sure the Highlevel functions of the dog will be disabled. To do that you need to use the RC. On the RC to the following sequence:

```
L2 + A
L2 + A
L2 + B
L1 + L2 + START
```

The dog should be lying on the floor now and you should HEAR that the dog is more silent than before.

Now to run the examples you should put your dog on the back and fold in all legs. This is the safest way!
Run the example of your choice like this:

```
example_velocity(lowlevel).py
```

The dog should move now, fully controlled via Lowlevel. Congratulations :)

## Donate
If this helped you to save money feel free to donate to help source more robot dogs :)
https://www.buymeacoffee.com/bin4ry


## Warnings
This is an Opensource project, we are not responsible for any damage done to your dog. Be aware that the project might be incomplete and may allow you to break the dog.

## LICENSE
MIT see LICENSE file
