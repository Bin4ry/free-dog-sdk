from enum import Enum
import struct
import binascii

def lib_version():
    return "0.2"

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
    elif type == 5:
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
    elif model == 5:
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
    return (struct.unpack('>I', struct.pack('>f', f))[0]).to_bytes(4, 'little')

def hex_to_float(hex):
    # Convert hex to bytes
    # b = bytes.fromhex(hex_value)

    # Convert bytes to integer with little-endian order
    i = int.from_bytes(hex, 'little')

    # Pack integer to bytes with big-endian order and unpack as float
    return struct.unpack('>f', struct.pack('>I', i))[0]


#Not sure how the original lib handles negative values. we just assume that they use the lower half from 0x00 to 0xff for positive values and teh upper part for negative.
#this is more imporant for the conversion from hex back to dec.

def fraction_to_hex(fraction, neg=False):
    if fraction == 0.0:
        neg = False
    hex_value = int(fraction * 256)
    if neg:
        hex_value = 255 + hex_value + 1
    return hex_value.to_bytes(1, 'little')

def tau_to_hex(tau):
    tau = round(tau,2)
    integer_part = int(tau)
    fractional_part = tau - integer_part
    neg = False
    if tau < 0:
        neg = True
        integer_part = 255 + integer_part
    try:
        return fraction_to_hex(fractional_part, neg) + integer_part.to_bytes(1, 'little')
    except Exception as e:
        print(e)
        print(tau)
        print(integer_part)


def hex_to_fraction(hex_byte, neg=False):
    if neg:
        return -1+round(hex_byte / 256, 2)
    else:
        return round(hex_byte / 256, 2)

def hex_to_tau(hex_bytes):
    ip = hex_bytes[1:]
    int_val = int.from_bytes(ip, 'little')
    neg = False
    # We just assume 126 the tipover point for the negative values
    if int_val > 126:
        neg = True
        int_val = -255 + int_val
    return int_val + hex_to_fraction(hex_bytes[0], neg)


def kp_to_hex(Kp):
    base, frac = divmod(Kp, 1)
    base = int(base)
    frac = int(round(frac,1) * 10)

    val = 0
    if frac < 5:
        val = (base * 32) + frac * 3
    if frac >= 5:
        val = (base * 32) + ((frac - 1) * 3) + 4

    val = f'%04x' % val
    kp = bytearray(bytes.fromhex(val))
    kp.reverse()
    return kp

def hex_to_kp(byte_arr):
    hex_bytes = binascii.hexlify(byte_arr)
    h = bytearray(4) # Yah doing this ugly, need to make it nice later when we know it really works
    h[0] = hex_bytes[2]
    h[1] = hex_bytes[3]
    h[2] = hex_bytes[0]
    h[3] = hex_bytes[1]
    byte_arr = h
    # print(byte_arr)
    val = int(byte_arr, 16)

    base = val // 32
    remainder = val % 32

    if remainder < 15:
        frac = remainder / 3
    else:
        frac = (remainder - 4) / 3 + 1

    return base + round(frac, 1) / 10

def get_hex_frac(frac):
    mapping = {0.0: '0', 0.1: '1', 0.2: '3', 0.3: '4', 0.4: '6', 0.5: '8', 0.6: '9', 0.7: 'b', 0.8: 'c', 0.9: 'e'}
    return mapping.get(frac, '0')

def kd_to_hex(decimal):
    integer_part = int(decimal)
    fractional_part = round(decimal - integer_part,1)
    hex_fractional_part = get_hex_frac(fractional_part)
    hex_integer_part = f'%03x' % integer_part
    kd = bytearray(bytes.fromhex(hex_integer_part + hex_fractional_part))
    kd.reverse()
    return kd

def get_frac_hex(frac):
    mapping = {'0': 0.0, '1': 0.1, '3': 0.2, '4': 0.3, '6':  0.4,'8':  0.5, '9': 0.6,'b':  0.7, 'c': 0.8, 'e': 0.9}
    return mapping.get(frac, 0.0)

def hex_to_kd(hex_bytes):
    hex_bytes = binascii.hexlify(hex_bytes)
    h = bytearray(4) # Yah doing this ugly, need to make it nice later when we know it really works
    h[0] = hex_bytes[2]
    h[1] = hex_bytes[3]
    h[2] = hex_bytes[0]
    h[3] = hex_bytes[1]
    hex_bytes = h
    int_part = int(hex_bytes[:3],16)
    frac_part = get_frac_hex(hex_bytes.hex()[3])
    kd = int_part + frac_part
    return kd

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
    temp=bytearray(4)# Yah doing this ugly, need to make it nice later when we know it really works
    temp[0] = data[1]
    temp[1] = data[2]
    temp[2] = data[3]
    temp[3] = data[0]
    return temp

# Just little helpers to take a look when needed

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
