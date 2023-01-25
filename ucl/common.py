from enum import Enum
import struct

def decode_sn(data):
    type = data[0]
    type_name = 'UNKNOWN'
    if type == 1:
        type_name = 'Laikago'
    elif type == 2:
        type_name = 'Aliengo'
    elif type == 3:
        type_name = 'A1'
    elif type == 4:
        type_name = 'Go1'
    elif type == 4:
        type_name = 'B1'
    model = data[1]
    model_name = 'UNKNOWN'
    if model == 1:
        model_name = 'AIR'
    elif model == 2:
        model_name = 'PRO'
    elif model == 3:
        model_name = 'EDU'
    elif model == 4:
        model_name = 'PC'
    elif model == 4:
        model_name = 'XX'
    product_name = f'{type_name}_{model_name}'
    id = f'{data[2]}-{data[3]}-{data[4]}[{data[5]}]'
    return product_name, id

def decode_version(data):
    hardware_version = f'{data[0]}.{data[1]}.{data[2]}'
    software_version = f'{data[3]}.{data[4]}.{data[5]}'
    return hardware_version, software_version

def getVoltage(cellVoltages):
    return sum(cellVoltages)


def float_to_hex(f):
    return (struct.unpack('<I', struct.pack('<f', f))[0]).to_bytes(4, 'little')

def hex_to_float(h):
    return struct.unpack('<f', h)[0]

def genCrc(i):
    crc = 0xFFFFFFFF
    for j in struct.unpack("<%dI" % (len(i) / 4), i):
        for b in range(32):
            x = (crc >> 31) & 1
            crc <<= 1
            crc &= 0xFFFFFFFF
            if x ^ (1&(j >> (31-b))):
                crc ^= 0x04c11db7
    crc = struct.pack('<I', crc)
    return crc

def encryptCrc(crc_val):
    crc_val = int.from_bytes(crc_val, byteorder='little')
    # Not my idea to call this an encryption, the manufacturer calls it an encryption in the original lib ;)
    xor_val = 0xedcab9de
    val=crc_val ^ xor_val
    data = struct.pack('<I', val)
    # happy byte swapping, sorry for making it ugly ;)
    temp=bytearray(4)
    temp[0] = data[1]
    temp[1] = data[2]
    temp[2] = data[3]
    temp[3] = data[0]
    return temp

def byte_print(bytes):
    a = ''.join('{:02x}'.format(x) for x in bytes)
    return a

def dump_obj(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

def pretty_print_obj(clas, indent=0, border=True):
    if border:
        print('===============================================================================================')
    print(' ' * indent + type(clas).__name__ + ':')
    indent += 4
    for k, v in clas.__dict__.items():
        if '__dict__' in dir(v):
            pretty_print_obj(v, indent, False)
        elif isinstance(v, Enum):
            print(' ' * indent + k + ': ' + str(v.value))
        else:
            print(' ' * indent + k + ': ' + str(v))
    if border:
        print('===============================================================================================')
