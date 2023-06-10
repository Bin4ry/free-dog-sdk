from ucl.common import byte_print, decode_version, decode_sn, getVoltage, pretty_print_obj, lib_version
from ucl.lowState import lowState
from ucl.lowCmd import lowCmd
from ucl.unitreeConnection import unitreeConnection, LOW_WIFI_DEFAULTS, LOW_WIRED_DEFAULTS
from ucl.enums import GaitType, SpeedLevel, MotorModeLow
from ucl.complex import motorCmd, motorCmdArray
import time
import sys
import math
import numpy as np
from pprint import pprint


def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos*(1-rate) + targetPos*rate
    return p

# You can use one of the 3 Presets WIFI_DEFAULTS, LOW_CMD_DEFAULTS or HIGH_CMD_DEFAULTS.
# IF NONE OF THEM ARE WORKING YOU CAN DEFINE A CUSTOM ONE LIKE THIS:
#
# MY_CONNECTION_SETTINGS = (listenPort, addr_wifi, sendPort_high, local_ip_wifi)
# conn = unitreeConnection(MY_CONNECTION_SETTINGS)
d = {'FR_0':0, 'FR_1':1, 'FR_2':2,
     'FL_0':3, 'FL_1':4, 'FL_2':5,
     'RR_0':6, 'RR_1':7, 'RR_2':8,
     'RL_0':9, 'RL_1':10, 'RL_2':11 }


print(f'Running lib version: {lib_version()}')
conn = unitreeConnection(LOW_WIFI_DEFAULTS)
conn.startRecv()
lcmd = lowCmd()
# lcmd.encrypt = True
lstate = lowState()
mCmdArr = motorCmdArray()
# Send empty command to tell the dog the receive port and initialize the connection
cmd_bytes = lcmd.buildCmd(debug=False)
conn.send(cmd_bytes)
data = conn.getData()
for paket in data:
    lstate.parseData(paket)
    print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')
    print(f'SN [{byte_print(lstate.SN)}]:\t{decode_sn(lstate.SN)}')
    print(f'Ver [{byte_print(lstate.version)}]:\t{decode_version(lstate.version)}')
    print(f'SOC:\t\t\t{lstate.bms.SOC} %')
    print(f'Overall Voltage:\t{getVoltage(lstate.bms.cell_vol)} mv') #something is still wrong here ?!
    print(f'Current:\t\t{lstate.bms.current} mA')
    print(f'Cycles:\t\t\t{lstate.bms.cycle}')
    print(f'Temps BQ:\t\t{lstate.bms.BQ_NTC[0]} °C, {lstate.bms.BQ_NTC[1]}°C')
    print(f'Temps MCU:\t\t{lstate.bms.MCU_NTC[0]} °C, {lstate.bms.MCU_NTC[1]}°C')
    print(f'FootForce:\t\t{lstate.footForce}')
    print(f'FootForceEst:\t\t{lstate.footForceEst}')
    print(f'IMU Temp:\t\t{lstate.imu.temperature}')
    print(f'MotorState FL_2 MODE:\t\t{lstate.motorState[d["FL_2"]].mode}')
    print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')

Tpi = 0
motiontime = 0
speed = 0.0
while True:
    time.sleep(0.002)
    motiontime += 1
    data = conn.getData()
    for paket in data:
        lstate.parseData(paket)
        if motiontime % 100 == 0: #Print every 100 cycles
            print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')
            print(f'SN [{byte_print(lstate.SN)}]:\t{decode_sn(lstate.SN)}')
            print(f'Ver [{byte_print(lstate.version)}]:\t{decode_version(lstate.version)}')
            print(f'SOC:\t\t\t{lstate.bms.SOC} %')
            print(f'Overall Voltage:\t{getVoltage(lstate.bms.cell_vol)} mv') #something is still wrong here ?!
            print(f'Current:\t\t{lstate.bms.current} mA')
            print(f'Cycles:\t\t\t{lstate.bms.cycle}')
            print(f'Temps BQ:\t\t{lstate.bms.BQ_NTC[0]} °C, {lstate.bms.BQ_NTC[1]}°C')
            print(f'Temps MCU:\t\t{lstate.bms.MCU_NTC[0]} °C, {lstate.bms.MCU_NTC[1]}°C')
            print(f'FootForce:\t\t{lstate.footForce}')
            print(f'FootForceEst:\t\t{lstate.footForceEst}')
            print(f'IMU Temp:\t\t{lstate.imu.temperature}')
            print(f'MotorState FL_2 MODE:\t\t{lstate.motorState[d["FL_2"]].mode}')
            print(f'MotorState FL_2 q:\t\t{lstate.motorState[d["FL_2"]].q}')
            print(f'MotorState FL_2 dq:\t\t{lstate.motorState[d["FL_2"]].dq}')
            print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')

    if( motiontime >= 500):
        speed = 2 * math.sin(3*math.pi*Tpi/2000.0)
        mCmdArr.setMotorCmd('FL_2',  motorCmd(mode=MotorModeLow.Servo, q=0, dq = speed, Kp = 0, Kd = 4, tau = 0.0))
        lcmd.motorCmd = mCmdArr

        Tpi += 1


    cmd_bytes = lcmd.buildCmd(debug=False)
    conn.send(cmd_bytes)
