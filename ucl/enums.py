from enum import Enum

class Mode(Enum):
    IDLE = 0
    FORCE_STAND = 1
    VEL_WALK = 2
    POS_WALK = 3
    PATH = 4
    STAND_DOWN = 5
    STAND_UP = 6
    DAMPING = 7
    RECOVERY = 8
    BACKFLIP = 9
    JUMPYAW = 10
    STRAIGHTHAND = 11
    DANCE1 = 12
    DANCE2 = 13

class GaitType(Enum):
    IDLE = 0
    TROT = 1
    CLIMB_STAIR = 2
    TROT_OBSTACLE = 3

class SpeedLevel(Enum):
    LOW_SPEED = 0
    MEDIUM_SPEED = 1
    HIGH_SPEED = 2
