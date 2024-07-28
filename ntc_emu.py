import hid
import time
from ctypes import *
from modbus_crc import crc16
import os
import sys
import argparse

def calc_crc16(dat, data_len):
    calc_data = dat[0:data_len];
    return crc16(calc_data)

def Func_Modbus_Send_10(reg,  length, val, buffer):
    buffer[0] = 0x01;
    buffer[1] = 0x10;
    buffer[2] = (int)(0xff & (reg >> 8));
    buffer[3] = (int)(0xff & (reg));
    buffer[4] = 0x00;
    buffer[5] = 0x02;
    buffer[6] = 0x04;
    buffer[7] = (int)(0xFF & (val >> 24));
    buffer[8] = (int)(0xFF & (val >> 16));
    buffer[9] = (int)(0xFF & (val >> 8));
    buffer[10]= (int)(0xFF & (val));
    crc1 = calc_crc16(buffer,  11);
    buffer[11] = crc1[0]
    buffer[12] = crc1[1]

def write_ntc_to_dev(ntc_value):
    buffer = [0]*64
    Func_Modbus_Send_10(91*2, 0x02, ntc_value, buffer);
    try:
        print("Opening the device")

        h = hid.device()
        h.open(0x0483, 0x572B)  # TREZOR VendorID/ProductID

        print("Manufacturer: %s" % h.get_manufacturer_string())
        print("Product: %s" % h.get_product_string())
        print("Serial No: %s" % h.get_serial_number_string())

        # enable non-blocking mode
        h.set_nonblocking(1)

        # write some data to the device
        print("Write ntc value to device, value=%d" % ntc_value)

        buffer_hw = [0x06] + buffer
        h.write(buffer_hw)
        print('hw array length=%#x'%len(buffer_hw))
        # wait
        time.sleep(0.2)

        # read back the answer
        print("Read the data from device")
        while True:
            d = h.read(65)
            if d:
                print(d)
            else:
                break

        print("Closing the device")
        h.close()

    except IOError as ex:
        print(ex)
        print("You probably don't have the hard-coded device.")
        print("Update the h.open() line in this script with the one")
        print("from the enumeration list output above and try again.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='这是一个解析命令行参数示例')
    parser.add_argument('--value', type=int, help='位置参数1')
    args = parser.parse_args()
    if None == args.value:
        ntc_value = 10000
    else:
        ntc_value = args.value
    write_ntc_to_dev(ntc_value);
    print("Done")
