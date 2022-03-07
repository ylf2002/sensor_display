import serial

try:
    serial = serial.Serial("/dev/ttyS0", 9600)
    if serial.isOpen():
        print('串口打开成功！\n')
        f = open('./test.txt','w') 
        #pass
    else:
        print('串口打开失败！\n')

    while 1:
        data = serial.readline()
        if data.startswith('$GNGGA'):
            line = str(data).split(',')
            print(line)
            print("时：",line[1][:2], "分：", line[1][2:4],"秒：", line[1][4:6])
            jing = float(line[4][:3]) + float(line[4][3:])/60
            wei = float(line[2][:2]) + float(line[2][2:])/60
            print("维度:",wei,line[3])
            print("经度:",jing,line[5])
           
except KeyboardInterrupt:
    print('error')