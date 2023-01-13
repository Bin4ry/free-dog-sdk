from ucl.highCmd import highCmd
from ucl.lowCmd import lowCmd
from ucl.unitreeConnection import unitreeConnection, WIFI_DEFAULTS, LOW_CMD_DEFAULTS, HIGH_CMD_DEFAULTS
from ucl.enums import Mode, GaitType, SpeedLevel
from ucl.complex import motorCmd
import time

conn = unitreeConnection(WIFI_DEFAULTS)
hcmd = highCmd()
hcmd.mode = Mode.VEL_WALK
hcmd.gaitType = GaitType.TROT
hcmd.velocity = [0.04, 0.1]
hcmd.yawSpeed = 2
hcmd.footRaiseHeight = 0.1
cmd_bytes = hcmd.buildCmd(debug=False)
conn.send(cmd_bytes)


# cmd = lowCmd()
# lcmd.levelFlag = 1
# lcmd.frameReserve = 2
# cmd = motorCmd(10, q=2, dq=1, tau=0.1, Kp=3, Kd=4)
# lcmd.motorCmd.setMotorCmd(0, cmd)
# lcmd.motorCmd.setMotorCmd(1, cmd)
# lcmd.motorCmd.setMotorCmd(2, cmd)
# lcmd.motorCmd.setMotorCmd(3, cmd)
# lcmd.motorCmd.setMotorCmd(4, cmd)
# lcmd.motorCmd.setMotorCmd(5, cmd)
# lcmd.motorCmd.setMotorCmd(6, cmd)
# lcmd.motorCmd.setMotorCmd(7, cmd)
# lcmd.motorCmd.setMotorCmd(8, cmd)
# lcmd.motorCmd.setMotorCmd(9, cmd)
# lcmd.motorCmd.setMotorCmd(10, cmd)
# lcmd.motorCmd.setMotorCmd(11, cmd)
# lcmd.buildCmd(debug=True)
