from enum import Enum
from ucl.enums import Mode
from ucl.common import float_to_hex

class cartesian:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

class bmsState:
    def __init__(self, version_h, version_l, bms_status, SOC, current, cycle, BQ_NTC, MCU_NTC, cell_vol):
        self.version_h = version_h
        self.version_l = version_l
        self.bms_status = bms_status
        self.SOC = SOC                      # SOC 0-100%
        self.current = current              # mA
        self.cycle = cycle
        self.BQ_NTC = BQ_NTC                # x1 degrees centigrade
        self.MCU_NTC = MCU_NTC              # x1 degrees centigrade
        self.cell_vol = cell_vol            # cell voltage mV
    
class bmsCmd:
    def __init__(self, off, reserve):
        self.off = off
        self.reserve = reserve

    def getBytes(self):
        return (self.off).to_bytes(1, byteorder='little') + self.reserve[0].to_bytes(1, byteorder='little') + self.reserve[1].to_bytes(1, byteorder='little') + self.reserve[2].to_bytes(1, byteorder='little')

class led:                                  # foot led brightness: 0~255
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def getBytes(self):
        return (self.r).to_bytes(1, byteorder='little') + (self.g).to_bytes(1, byteorder='little') + (self.b).to_bytes(1, byteorder='little') + bytes(1)

class motorState:                               # motor feedback
    def __init__(self, mode, q, dq, ddq, tauEst, q_raw, dq_raw, ddq_raw, temperature, reserve):
        self.mode = mode                        # motor working mode
        self.q = q                              # current angle (unit: radian)
        self.dq = dq                            # current velocity (unit: radian/second)
        self.ddq = ddq                          # current acc (unit: radian/second*second)
        self.tauEst = tauEst                    # current estimated output torque (unit: N.m)
        self.q_raw = q_raw                      # current angle (unit: radian)
        self.dq_raw = dq_raw                    # current velocity (unit: radian/second)
        self.ddq_raw = ddq_raw
        self.temperature = temperature          # current temperature (temperature conduction is slow that leads to lag)
        self.reserve = reserve

class imu:                                      # when under accelerated motion, the attitude of the robot calculated by IMU will drift.
    def __init__(self, quaternion, gyroscope, accelerometer, rpy, temperature):
        self.quaternion = quaternion            # quaternion, normalized, (w,x,y,z)
        self.gyroscope = gyroscope              # angular velocity （unit: rad/s)    (raw data)
        self.accelerometer = accelerometer      # m/(s2)                             (raw data)
        self.rpy = rpy                          # euler angle（unit: rad)
        self.temperature = temperature

class motorCmd:
    def __init__(self, mode=0, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0]):
        self.mode = mode             # desired working mode
        self.q = q                   # desired angle (unit: radian)
        self.dq = dq                 # desired velocity (unit: radian/second)
        self.tau = tau               # desired output torque (unit: N.m)
        self.Kp = Kp                 # desired position stiffness (unit: N.m/rad )
        self.Kd = Kd                 # desired velocity stiffness (unit: N.m/(rad/s) )
        self.reserve = reserve

    def getBytes(self):
        if isinstance(self.mode, Enum):
            self.mode = self.mode.value

        return (self.mode).to_bytes(1, byteorder='little') + float_to_hex(self.q) + float_to_hex(self.dq) + float_to_hex(self.tau) + float_to_hex(self.Kp) + float_to_hex(self.Kd) + self.reserve[0].to_bytes(2, byteorder='little') + self.reserve[1].to_bytes(2, byteorder='little') + self.reserve[2].to_bytes(2, byteorder='little')


class motorCmdArray:
    def __init__(self):
        #JOINTS
        self.FR_0 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])
        self.FR_1 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])
        self.FR_2 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])

        self.FL_0 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])
        self.FL_1 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])
        self.FL_2 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])

        self.RR_0 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])
        self.RR_1 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])
        self.RR_2 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])

        self.RL_0 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])
        self.RL_1 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])
        self.RL_2 = motorCmd(mode=Mode.IDLE, q=0, dq=0, tau=0, Kp=0, Kd=0, reserve=[0,0,0])

    def setMotorCmd(self, motorIndex, motorCmd):
        if motorIndex == 'FR_0' or motorIndex == 0:
            self.FR_0 = motorCmd
        if motorIndex == 'FR_1' or motorIndex == 1:
            self.FR_1 = motorCmd
        if motorIndex == 'FR_2' or motorIndex == 2:
            self.FR_2 = motorCmd

        if motorIndex == 'FL_0' or motorIndex == 3:
            self.FL_0 = motorCmd
        if motorIndex == 'FL_1' or motorIndex == 4:
            self.FL_1 = motorCmd
        if motorIndex == 'FL_2' or motorIndex == 5:
            self.FL_2 = motorCmd

        if motorIndex == 'RR_0' or motorIndex == 6:
            self.RR_0 = motorCmd
        if motorIndex == 'RR_1' or motorIndex == 7:
            self.RR_1 = motorCmd
        if motorIndex == 'RR_2' or motorIndex == 8:
            self.RR_2 = motorCmd

        if motorIndex == 'RL_0' or motorIndex == 9:
            self.RL_0 = motorCmd
        if motorIndex == 'RL_1' or motorIndex == 10:
            self.RL_1 = motorCmd
        if motorIndex == 'RL_2' or motorIndex == 11:
            self.RL_2 = motorCmd

    def getBytes(self):
        return self.FR_0.getBytes() + self.FR_1.getBytes() + self.FR_2.getBytes() + self.FL_0.getBytes() + self.FL_1.getBytes() + self.FL_2.getBytes() + self.RR_0.getBytes() + self.RR_1.getBytes() + self.RR_2.getBytes() + self.RL_0.getBytes() + self.RL_1.getBytes() + self.RL_2.getBytes()
