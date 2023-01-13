import struct
import crcmod
def float_to_hex(f):
    return (struct.unpack('<I', struct.pack('<f', f))[0]).to_bytes(4, 'little')

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
