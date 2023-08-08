from ucl.enums import MotorModeLow, GaitType, SpeedLevel
from enum import Enum
from ucl.common import float_to_hex, hex_to_float, tau_to_hex, hex_to_tau, encryptCrc, genCrc, byte_print
from ucl.complex import cartesian, led, bmsState, imu, motorState
import struct


class lowState:
    def __init__(self): #highState len == 1087 / lowState len == 807
        self.head = bytearray(2)
        self.levelFlag = 0
        self.frameReserve = 0
        self.SN = bytearray(8)
        self.version = bytearray(8)
        self.bandWidth = bytearray(4)
        self.imu = imu([0.0,0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],0)
        self.motorState = [motorState(0,0,0,0,0,0,0,0,0,0)]*20
        self.bms = bmsState(0,0,0,0,0,0,0,0,0)
        self.footForce = [bytes.fromhex('0000')]*4
        self.footForceEst = [bytes.fromhex('0000')]*4
        self.tick = bytearray(4)
        self.wirelessRemote = bytearray(40)
        self.reserve = bytearray(4)

    def dataToBmsState(self,data):
        version_h = data[0]
        version_l = data[1]
        bms_status = data[2]
        SOC = data[3]
        current = int.from_bytes(data[4:8], byteorder='little', signed=True)
        cycle = int.from_bytes(data[8:10], byteorder='little')
        BQ_NTC = [data[10], data[11]]
        MCU_NTC = [data[12], data[13]]
        cell_vol = [data[14] * 32, data[15] * 32, data[16] * 32, data[17] * 32, data[18] * 32, data[19] * 32, data[20] * 32, data[21] * 32, data[22] * 32, data[23] * 32]
        return bmsState(version_h, version_l, bms_status, SOC, current, cycle, BQ_NTC, MCU_NTC, cell_vol)


    def dataToImu(self, data):
        quaternion = [hex_to_float(data[0:4]), hex_to_float(data[4:8]), hex_to_float(data[8:12]), hex_to_float(data[12:16])]
        gyroscope = [hex_to_float(data[16:20]), hex_to_float(data[20:24]), hex_to_float(data[24:28])]
        accelerometer = [hex_to_float(data[28:32]), hex_to_float(data[32:36]), hex_to_float(data[36:40])]
        rpy = [hex_to_float(data[40:44]), hex_to_float(data[44:48]), hex_to_float(data[48:52])]
        temperature = data[52]
        return imu(quaternion, gyroscope, accelerometer, rpy, temperature)

    def dataToMotorState(self, data):
        mode = data[0]
        q = hex_to_float(data[1:5])
        dq = hex_to_float(data[5:9])
        ddq = float(int.from_bytes(data[9:11], byteorder='little', signed=True))
        tauEst = float(int.from_bytes(data[11:13], byteorder='little', signed=True)) * 0.00390625
        q_raw = hex_to_float(data[13:17])
        dq_raw = hex_to_float(data[17:21])
        ddq_raw = float(int.from_bytes(data[21:23], byteorder='little', signed=True))
        temperature = data[24]
        reserve = [int.from_bytes(data[24:28], byteorder='little'), int.from_bytes(data[28:32], byteorder='little')]
        return motorState(mode, q, dq, ddq, tauEst, q_raw, dq_raw, ddq_raw, temperature, reserve)

    def parseData(self, data):
        self.head = hex(int.from_bytes(data[0:2], byteorder='little'))
        self.levelFlag = data[2]
        self.frameReserve = data[3]
        self.SN = data[4:12]
        self.version = data[12:20]
        self.bandWidth = int.from_bytes(data[20:22], byteorder='little')
        self.imu = self.dataToImu(data[22:75])
        self.motorState=[]
        for i in range(20):
            self.motorState.append(self.dataToMotorState(data[(i*32)+75:(i*32)+32+75]))
        self.bms=self.dataToBmsState(data[715:739])
        self.footForce = [int.from_bytes(data[739:741], byteorder='little'), int.from_bytes(data[751:753], byteorder='little'), int.from_bytes(data[753:755], byteorder='little'), int.from_bytes(data[755:757], byteorder='little')]
        self.footForceEst = [int.from_bytes(data[747:749], byteorder='little'), int.from_bytes(data[759:761], byteorder='little'), int.from_bytes(data[761:763], byteorder='little'), int.from_bytes(data[763:765], byteorder='little')]
        self.mode = data[755:759]
        self.wirelessRemote = data[759:799]
        self.reserve = data[799:803]
        self.crc = data[803:807]
        return True
