from ucl.enums import MotorModeHigh, GaitType, SpeedLevel
from enum import Enum
from ucl.common import float_to_hex, encryptCrc, genCrc, byte_print
from ucl.complex import led, bmsCmd

class highCmd:
    def __init__(self):
        self.head = bytes.fromhex('FEEF')
        self.levelFlag = 0x00
        self.frameReserve = 0
        self.SN = bytearray(8)
        self.version = bytearray(8)
        self.bandWidth = bytearray(2)
        self.mode = MotorModeHigh.IDLE
        self.gaitType = GaitType.IDLE
        self.speedLevel = SpeedLevel.LOW_SPEED
        self.footRaiseHeight = 0.0
        self.bodyHeight = 0.0
        self.position = [0.0, 0.0]
        self.euler = [0.0, 0.0, 0.0]
        self.velocity = [0.0, 0.0]
        self.yawSpeed = 0.0
        self.bms = bmsCmd(0,[0,0,0])
        self.led = led(0,0,0)
        self.wirelessRemote = bytearray(40)
        self.reserve = bytearray(4)
        self.crc = None
        self.encrypt = False

    def buildCmd(self, debug=False):
        cmd = bytearray(129)
        cmd[0:2] = self.head
        cmd[2] = self.levelFlag
        cmd[3] = self.frameReserve
        cmd[4:12] = self.SN
        cmd[12:20] = self.version
        cmd[20:22] = self.bandWidth

        if isinstance(self.mode, Enum):
            cmd[22] = self.mode.value
        else:
            cmd[22] = self.mode
        if isinstance(self.gaitType, Enum):
            cmd[23] = self.gaitType.value
        else:
            cmd[23] = self.gaitType
        if isinstance(self.speedLevel, Enum):
            cmd[24] = self.speedLevel.value
        else:
            cmd[24] = self.speedLevel
        cmd[25:29] = float_to_hex(self.footRaiseHeight)
        cmd[29:33] = float_to_hex(self.bodyHeight)

        cmd[33:37] = float_to_hex(self.position[0])
        cmd[37:41] = float_to_hex(self.position[1])

        cmd[41:45] = float_to_hex(self.euler[0])
        cmd[45:49] = float_to_hex(self.euler[1])
        cmd[49:53] = float_to_hex(self.euler[2])

        cmd[53:57] = float_to_hex(self.velocity[0])
        cmd[57:61] = float_to_hex(self.velocity[1])

        cmd[61:65] = float_to_hex(self.yawSpeed)
        cmd[65:69] = self.bms.getBytes()
        cmd[69:73] = self.led.getBytes()
        cmd[73:113] = self.wirelessRemote
        cmd[113:117] = self.reserve
        if self.encrypt:
            cmd[-4:] = encryptCrc(genCrc(cmd[:-5]))
        else:
            cmd[-4:] = genCrc(cmd[:-5])
        if debug:
            print(f'Send Data ({len(cmd)}): {byte_print(cmd)}')
        return cmd
