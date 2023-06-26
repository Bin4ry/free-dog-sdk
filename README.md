# Unitree Go1 Free-Dog SDK featuring 'faux-level' support!

[Who let the 'robot dogs' out!?](https://www.youtube.com/watch?v=Qkuu0Lwb5EM)

![Who Let The Dogs Out?](https://github.com/Bin4ry/free-dog-sdk/raw/main/WhoLetDogsOut.gif)
![Who Let The Dogs Out?](https://github.com/Bin4ry/free-dog-sdk/raw/main/DogsGettingOut.gif)

This repo consists of a free, non paywalled, non pay-for-play version of the [Unitree Legged SDK](https://github.com/unitreerobotics/unitree_legged_sdk). Former "DJI Slack OG" [@bin4ry](https://twitter.com/bin4rydigit) was not only upset that the original Unitree SDK only came with precompiled and poorly documented libraries, but also sick of hearing [@d0tslash](https://twitter.com/d0tslash) complain about it on "TheDogPound - Animal control for stray robot dogs" Slack group. 

Through months of dedication the Unitree libraries were reverse engineered, and this git repository was created with a "free" / liberated version of the Unitree library. This work is far from finished, but in current form it can be used to send ```highLevelCmds``` and ```lowLevelCmds``` to the 宇树科技 Yushu Technology (Unitree) Go1 series dogs. Specifically this SDK enables EDU low-level functions on Air, Pro, and MAX dogs, known to the community as "Faux-Level" support. This code should also be cross functional with A1, AlienGo, B1, and others, but will require some work to support their hard coded values. PR's are [welcome](https://github.com/Bin4ry/free-dog-sdk/compare). 

The intention of this repo is to break free of the manufacturers restricitons on which dog's can utilize the full SDK functionality. The Free-Dog SDK has proven to work on all Models of the 宇树科技 Yushu Technology (Unitree) Go1 series including Air, Pro, Max and EDU models. Unitree sales staff, and distributors repeatedly make claims, and assert that only the EDU dog can be controlled via the SDK, as such you must purchase the more expensive dog if you seek to be a developer. The end user population is discuraged from buying the Air, and told it is simply a "toy", that handles like a "remote control" car *only*. The Unitree community however was quick to discover that in fact ```highLevelCmds``` can in fact be used to control non-Edu models. We further built on the community dicovery to prove that in fact you can also use ```lowLevelCmds``` with inexpensive dogs.

## Support
Stop by "TheDogPound - Animal control for stray robot dogs" Slack group, and join #faux-level and #unitree for support assistance. This is a new project, and a fresh group, be patient with your support requests, and needs.
https://join.slack.com/t/robotdogs/shared_invite/zt-1fvixx89u-7T79~VxmDYdFSIoTnSagFQ

## Current State

The SDK is fully useable, however, it does currently not include any Safety features of the original SDK. Please feel free to contribute the Safety restrictions to the project, we do have a base git issue explaining the needed logic if you are interested in contributing! [Detail on replicating Safety functions](https://github.com/Bin4ry/free-dog-sdk/issues/7). As expected this software might still include small bugs, or errata, if you see one, or find some please let us know via git [issue](https://github.com/Bin4ry/free-dog-sdk/issues), or attempt to fix it and submit a [PR](https://github.com/Bin4ry/free-dog-sdk/pulls).

## What do you need?

This repo, python3 and a few prerequisite modules. 

First clone the repo

```
git clone https://github.com/Bin4ry/free-dog-sdk.git
```
then go into the folder and install the requirements (prerequisite modules) 

```
cd free-dog-sdk
pip install -r requirements.txt
```

## Configuration of the dog and the SDK
There are several configurations you can run. You can either run the script from any component inside the dog, either the Jetsons or RasPi. Alternately you can run it from a PC connected to the Dog's network. The location in which the code runs doesn't particiularly matter, but you will need to make sure to configure your dogs network accordingly, and subsequently use the correct connection settings inside the Free-Dog SDK. For our examples we connected a PC to the WiFi using the dogs Hotspot. 

Start the dog up, and connect to the WiFi. The default Wifi password is of the Hotspot is 00000000. Please see Unitree documentation for more detail.

In this case the DHCP service gave us the address IP 192.168.12.14 and we were able to reach the dog which was verified via a ```ping 192.168.12.1``` test. 

This simple connectivity is all that is needed to run the Highlevel examples.

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
This is an Opensource project, we are not responsible for any damage done to your dog. Be aware that the project might be incomplete and may allow you to break the dog. If you are not familiar with Unitree Low level commands, it is highly recommended you first read up on them. Low level commands are not for the light hearted, and as stated multiple times, CAN damage your dog. 

At least one user on our Slack Group blew his MOSFETs with the normal Unitree SDK, expect ours to have the same ability to allow you to create your own failure conditions. 

## LICENSE
MIT see LICENSE file

![Who Let The Dogs Out?](https://github.com/Bin4ry/free-dog-sdk/raw/main/WhoWhoWhoWho.gif)
![Who Let The Dogs Out?](https://github.com/Bin4ry/free-dog-sdk/raw/main/DogsFleeing.gif)

## Birds of a Feather?
Looking for Quadruped friends? Join "The Dog Pound animal control for Stray robot dogs" slack group: <br>
https://join.slack.com/t/robotdogs/shared_invite/zt-1fvixx89u-7T79~VxmDYdFSIoTnSagFQ<br>

Looking for a Unitree Go1 Air, Pro, or MAX bible full of the current community info? Look no further than the [宇树科技 Yushu Technology Unitree go1 development notes repo](https://github.com/MAVProxyUser/YushuTechUnitreeGo1/tree/main)


If you like this repo, fork it... [Click to Fork https://github.com/Bin4ry/free-dog-sdk](https://github.com/Bin4ry/free-dog-sdk/fork)! Make sure you keep your forked copy up to date, lots of changes happen over time. You won't want a stale copy. 
