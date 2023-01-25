from ucl.enums import Mode, GaitType, SpeedLevel
from enum import Enum
from ucl.common import float_to_hex, hex_to_float, encryptCrc, genCrc, byte_print
from ucl.complex import cartesian, led, bmsState, imu, motorState
import struct

class highState:
    def __init__(self): #highState len == 1087 / lowState len == 807
        self.head = bytearray(2)
        self.levelFlag = 0
        self.frameReserve = 0
        self.SN = bytearray(8)
        self.version = bytearray(8)
        self.bandWidth = bytearray(4)
        self.imu = imu([0.0,0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],0)
        self.motorstate = [motorState(0,0,0,0,0,0,0,0,0,0)]*20
        self.bms = bmsState(0,0,0,0,0,0,0,0,0)
        self.footForce = [bytes.fromhex('0000')]*4
        self.footForceEst = [bytes.fromhex('0000')]*4
        self.mode = Mode.IDLE
        self.progress = 0.0
        self.gaitType = GaitType.IDLE
        self.footRaiseHeight = 0.0
        self.position = [0.0, 0.0]
        self.bodyHeight = 0.0
        self.velocity = [0.0, 0.0]
        self.yawSpeed = 0.0
        self.rangeObstacle = bytearray(16)
        self.footPosition2Body = bytearray(48)
        self.footSpeed2Body = bytearray(48)
        self.speedLevel = SpeedLevel.LOW_SPEED
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
        cell_vol = [int.from_bytes(data[13:15], byteorder='little'), int.from_bytes(data[15:17], byteorder='little'), int.from_bytes(data[17:19], byteorder='little'), int.from_bytes(data[19:21], byteorder='little'), int.from_bytes(data[21:23], byteorder='little'),
                    int.from_bytes(data[23:25], byteorder='little'), int.from_bytes(data[25:27], byteorder='little'), int.from_bytes(data[27:29], byteorder='little'), int.from_bytes(data[29:31], byteorder='little'), int.from_bytes(data[31:33], byteorder='little')]
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
        ddq = hex_to_float(data[9:13])
        tauEst = hex_to_float(data[13:17])
        q_raw = hex_to_float(data[17:21])
        dq_raw = hex_to_float(data[21:25])
        ddq_raw = hex_to_float(data[25:29])
        temperature = data[29]
        reserve = [int.from_bytes(data[30:34], byteorder='little'), int.from_bytes(data[34:38], byteorder='little')]
        return motorState(mode, q, dq, ddq, tauEst, q_raw, dq_raw, ddq_raw, temperature, reserve)

    def parseData(self, data):
        self.head = hex(int.from_bytes(data[0:2], byteorder='little'))
        self.levelFlag = data[2]
        self.frameReserve = data[3]
        self.SN = data[4:12]
        self.version = data[12:20]
        self.bandWidth = int.from_bytes(data[20:22], byteorder='little')
        self.imu = self.dataToImu(data[22:75])
        self.motorstate=[]
        for i in range(20):
            self.motorstate.append(self.dataToMotorState(data[(i*38)+75:(i*38)+38+75]))
        self.bms=self.dataToBmsState(data[835:869])
        self.footForce = [int.from_bytes(data[869:871], byteorder='little'), int.from_bytes(data[871:873], byteorder='little'), int.from_bytes(data[873:875], byteorder='little'), int.from_bytes(data[875:877], byteorder='little')]
        self.footForceEst = [int.from_bytes(data[877:879], byteorder='little'), int.from_bytes(data[879:881], byteorder='little'), int.from_bytes(data[881:883], byteorder='little'), int.from_bytes(data[883:885], byteorder='little')]
        self.mode = data[885]
        self.progress = hex_to_float(data[886:890])
        self.gaitType = data[890]
        self.footRaiseHeight = hex_to_float(data[891:895])
        self.position = [hex_to_float(data[895:899]), hex_to_float(data[899:903]), hex_to_float(data[903:907])]
        self.bodyHeight = hex_to_float(data[907:911])
        self.velocity = [hex_to_float(data[911:915]), hex_to_float(data[915:919]), hex_to_float(data[919:923])]
        self.yawSpeed = hex_to_float(data[923:927])
        self.rangeObstacle = [hex_to_float(data[927:931]), hex_to_float(data[931:935]), hex_to_float(data[935:939]), hex_to_float(data[939:943])]
        self.footPosition2Body = []
        for i in range(4):
            self.footPosition2Body.append(cartesian(hex_to_float(data[(i*12)+943:(i*12)+947]), hex_to_float(data[(i*12)+947:(i*12)+951]), hex_to_float(data[(i*12)+951:(i*12)+955])))
        self.footSpeed2Body = []
        for i in range(4):
            self.footSpeed2Body.append(cartesian(hex_to_float(data[(i*12)+991:(i*12)+995]), hex_to_float(data[(i*12)+995:(i*12)+999]), hex_to_float(data[(i*12)+999:(i*12)+1003])))
        self.wirelessRemote = data[1039:1079]
        self.reserve = data[1079:1083]
        self.crc = data[1083:1087]


