from ucl.enums import Mode, GaitType, SpeedLevel
from enum import Enum
from ucl.common import float_to_hex, encryptCrc, genCrc
from ucl.complex import led, bms, imu, motorSate

class highState:
    def __init__(self): #highState len == 1087 / lowState len == 807
        self.head = bytearray(2)
        self.levelFlag = 0
        self.frameReserve = 0
        self.SN = bytearray(8)
        self.version = bytearray(8)
        self.bandWidth = bytearray(4)
        self.imu = imu()
        self.motorstate = motorState()
        self.bms = bmsState()
        self.footForce = None
        self.footForceEst = None
        self.mode = Mode.IDLE
        self.progress = 0.0
        self.gaitType = GaitType.IDLE
        self.footRaiseHeight = 0.0
        self.position = [0.0, 0.0]
        self.bodyHeight = 0.0
        self.velocity = [0.0, 0.0]
        self.yawSpeed = 0.0
        self.rangeObstacle = None
        self.footPosition2Body = None
        self.footSpeed2Body = None
        self.speedLevel = SpeedLevel.LOW_SPEED
        self.wirelessRemote = bytearray(40)
        self.reserve = bytearray(4)
