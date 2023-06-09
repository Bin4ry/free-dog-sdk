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

PosStopF  = math.pow(10,9)
VelStopF  = 16000.0
LOWLEVEL  = 0xff
sin_mid_q = [0.0, 1.2, -2.0]
dt = 0.002
qInit = [0, 0, 0]
qDes = [0, 0, 0]
sin_count = 0
rate_count = 0
Kp = [0, 0, 0]
Kd = [0, 0, 0]

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
    print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')
    lstate.parseData(paket)
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
    print(f'MotorState FR_0 MODE:\t\t{lstate.motorState[d["FR_0"]].mode}')
    print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')

motiontime = 0

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
            print(f'MotorState FR_0 MODE:\t\t{lstate.motorState[d["FR_0"]].mode}')
            print(f'MotorState FR_0 q:\t\t{lstate.motorState[d["FR_0"]].q}')
            print(f'MotorState FR_0 dq:\t\t{lstate.motorState[d["FR_0"]].dq}')
            print('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=')

    if( motiontime >= 0):

        # first, get record initial position
        if( motiontime >= 0 and motiontime < 10):
            qInit[0] = lstate.motorState[d['FR_0']].q
            qInit[1] = lstate.motorState[d['FR_1']].q
            qInit[2] = lstate.motorState[d['FR_2']].q

        # second, move to the origin point of a sine movement with Kp Kd
        if( motiontime >= 10 and motiontime < 400):
            rate_count += 1
            rate = rate_count/200.0                       # needs count to 200
            Kp = [5, 5, 5]
            Kd = [1, 1, 1]
            # Kp = [20, 20, 20]
            # Kd = [2, 2, 2]

            qDes[0] = jointLinearInterpolation(qInit[0], sin_mid_q[0], rate)
            qDes[1] = jointLinearInterpolation(qInit[1], sin_mid_q[1], rate)
            qDes[2] = jointLinearInterpolation(qInit[2], sin_mid_q[2], rate)

        # last, do sine wave
        freq_Hz = 1
        # freq_Hz = 5
        freq_rad = freq_Hz * 2* math.pi
        t = dt*sin_count
        if( motiontime >= 400):
            sin_count += 1
            # sin_joint1 = 0.6 * sin(3*M_PI*sin_count/1000.0)
            # sin_joint2 = -0.9 * sin(3*M_PI*sin_count/1000.0)
            sin_joint1 = 0.6 * math.sin(t*freq_rad)
            sin_joint2 = -0.9 * math.sin(t*freq_rad)
            qDes[0] = sin_mid_q[0]
            qDes[1] = sin_mid_q[1] + sin_joint1
            qDes[2] = sin_mid_q[2] + sin_joint2


        mCmdArr.setMotorCmd('FR_0',  motorCmd(mode=MotorModeLow.Servo, q=qDes[0], dq = 0, Kp = Kp[0], Kd = Kd[0], tau = -0.65))
        mCmdArr.setMotorCmd('FR_1',  motorCmd(mode=MotorModeLow.Servo, q=qDes[1], dq = 0, Kp = Kp[1], Kd = Kd[1], tau = 0.0))
        mCmdArr.setMotorCmd('FR_2',  motorCmd(mode=MotorModeLow.Servo, q=qDes[2], dq = 0, Kp = Kp[2], Kd = Kd[2], tau = 0.0))
        lcmd.motorCmd = mCmdArr

        cmd_bytes = lcmd.buildCmd(debug=False)
        conn.send(cmd_bytes)
