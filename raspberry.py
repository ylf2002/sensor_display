from smbus import SMBus
import time
import json
import requests
import datetime
import serial

rqs_headers = {'Content-Type': 'application/json'}
requrl = 'http://192.168.43.95:8888/sensor/sensors_api/'  # 服务器的IP地址

#sudo i2cdetect -y 1查看地址
ACC_ADDRESS = 0x19
ACC_REGISTER_ADDRESS = 0x02
GYR_ADDRESS = 0x69
GYR_REGISTER_ADDRESS = 0x02
MAG_ADDRESS = 0x13
MAG_REGISTER_ADDRESS = 0x42

i2c = SMBus(1)

class ComplexEncoder(json.JSONEncoder):  # 这个是用来把datetime的时间格式化
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def bmx055_setup():
    # --- BMX055ãSetup --- #
    try:
        i2c.write_byte_data(ACC_ADDRESS, 0x0F, 0x03)
        time.sleep(0.1)
        i2c.write_byte_data(ACC_ADDRESS, 0x10, 0x0F)
        time.sleep(0.1)
        i2c.write_byte_data(ACC_ADDRESS, 0x11, 0x00)
        time.sleep(0.1)
    except:
        time.sleep(0.1)
        print("BMX055 Setup Error")
        i2c.write_byte_data(ACC_ADDRESS, 0x0F, 0x03)
        time.sleep(0.1)
        i2c.write_byte_data(ACC_ADDRESS, 0x10, 0x0F)
        time.sleep(0.1)
        i2c.write_byte_data(ACC_ADDRESS, 0x11, 0x00)
        time.sleep(0.1)

    #Initialize GYR
    try:
        i2c.write_byte_data(GYR_ADDRESS, 0x0F, 0x00)
        time.sleep(0.1)
        i2c.write_byte_data(GYR_ADDRESS, 0x10, 0x07)
        time.sleep(0.1)
        i2c.write_byte_data(GYR_ADDRESS, 0x11, 0x00)
        time.sleep(0.1)
    except:
        time.sleep(0.1)
        print("BMX055 Setup Error")
        i2c.write_byte_data(GYR_ADDRESS, 0x0F, 0x00)
        time.sleep(0.1)
        i2c.write_byte_data(GYR_ADDRESS, 0x10, 0x07)
        time.sleep(0.1)
        i2c.write_byte_data(GYR_ADDRESS, 0x11, 0x00)
        time.sleep(0.1)

    #Initialize MAG
    try:
        data = i2c.read_byte_data(MAG_ADDRESS, 0x4B)
        if(data == 0):
            i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x83)
            time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x01)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4C, 0x38)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4E, 0x84)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x51, 0x04)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x52, 0x0F)
        time.sleep(0.1)
    except:
        time.sleep(0.1)
        print("BMX055 Setup Error")
        data = i2c.read_byte_data(MAG_ADDRESS, 0x4B)
        if(data == 0):
            i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x83)
            time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x01)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4C, 0x38)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4E, 0x84)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x51, 0x04)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x52, 0x0F)
        time.sleep(0.1)

def acc_dataRead():
    accData = [0, 0, 0, 0, 0, 0]
    value = [0.0, 0.0, 0.0]
    for i in range(6):
        accData[i] = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+i)


    for i in range(3):
        value[i] = (accData[2*i+1] * 16) + (int(accData[2*i] & 0xF0) / 16)
        value[i] = value[i] if value[i] < 2048 else value[i] - 4096
        value[i] = value[i] * 0.0098 * 1

    return value

def gyr_dataRead():
    gyrData = [0, 0, 0, 0, 0, 0]
    value = [0.0, 0.0, 0.0]
    for i in range(6):
        gyrData[i] = i2c.read_byte_data(GYR_ADDRESS, GYR_REGISTER_ADDRESS+i)


    for i in range(3):
        value[i] = (gyrData[2*i+1] * 256) + gyrData[i]
        value[i] = value[i] - 65536 if value[i] > 32767 else value[i]
        value[i] = value[i] * 0.0038 * 16

    return value

def mag_dataRead():
    magData = [0, 0, 0, 0, 0, 0, 0, 0]
    value = [0.0, 0.0, 0.0]
    for i in range(8):
        magData[i] = i2c.read_byte_data(MAG_ADDRESS, MAG_REGISTER_ADDRESS + i)


    for i in range(3):
        if i != 2:
            value[i] = ((magData[2*i+1] *256) + (magData[2*i] & 0xF8)) / 8
            if value[i] > 4095:
                value[i] = value[i] - 8192
        else:
            value[i] = ((magData[2*i+1] * 256) | (magData[2*i] & 0xF8)) / 2
            if value[i] > 16383:
                value[i] = value[i] - 32768

    return value

def bmx055_read():
    accx, accy, accz = acc_dataRead()
    gyrx, gyry, gyrz = gyr_dataRead()
    magx, magy, magz = mag_dataRead()
    value = [accx, accy, accz, gyrx, gyry, gyrz, magx, magy, magz]

    for i in range(len(value)):
        if value[i] is not None:
            value[i] = round(value[i], 2)

    return value

if __name__ == '__main__':
    try:
        bmx055_setup()
        # time.sleep(0.2)
        serial = serial.Serial("/dev/ttyS0", 9600)
        if serial.isOpen():
            print('串口打开成功！\n')
        else:
            print('串口打开失败！\n')
        while 1:
            data = str(str(serial.readline())[2:])
            if data.startswith('$GNGGA'):
                line = str(data).split(',')
                # print(line)
                # print("时：",line[1][:2], "分：", line[1][2:4],"秒：", line[1][4:6])
                jing = float(line[4][:3]) + float(line[4][3:])/60
                wei = float(line[2][:2]) + float(line[2][2:])/60
                # print("维度:",wei,line[3])
                # print("经度:",jing,line[5])
            bmxData = bmx055_read()
            # print("accx:{} accy:{} accz:{}".format(bmxData[0],bmxData[1],bmxData[2]))
            # print("gyrx:{} gyry:{} gyrz:{}".format(bmxData[3],bmxData[4],bmxData[5]))
            # print("magx:{} magy:{} magz:{}".format(bmxData[6],bmxData[7],bmxData[8]))
            new_data = {
                "captime": datetime.datetime.now(),
                "accx": bmxData[0],
                "accy": bmxData[1],
                "accz": bmxData[2],
                "magx": bmxData[6],
                "magy": bmxData[7],
                "magz": bmxData[8],
                "gyrx": bmxData[3],
                "gyry": bmxData[4],
                "gyrz": bmxData[5],
                "longitude": jing,
                "latitude": wei
            }

            test_data = json.dumps(new_data, cls=ComplexEncoder)
            # print(requrl, rqs_headers, test_data)
            response = requests.post(url=requrl, headers=rqs_headers, data=test_data)
            print(response)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print('error')