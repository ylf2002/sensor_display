with open("gps0.txt", "r") as f:  # 打开文件
    lines = f.readlines()  # 读取文件
    for line in lines:
        if line.startswith('$GNGGA'):
            line = str(line).split(',')
            print(line)
            print("时：",line[1][:2], "分：", line[1][2:4],"秒：", line[1][4:6])
            jing = float(line[4][:3]) + float(line[4][3:])/60
            wei = float(line[2][:2]) + float(line[2][2:])/60
            print("维度:",wei,line[3])
            print("经度:",jing,line[5])
            if line[6]=='1':
                print("GPS状态非差分定位")
            print("使用卫星数量：", line[7])
            print("HDOP水平精度因子", line[8])
            print("海拔高度:", line[9])
            print("地球椭球面相对大地水准面的高度:", line[10])
            print("差分时间:", line[11])
            print("差分站ID号:", line[12])
            print("校验值:", line[13])
        
        elif line.startswith('$GPGSV'):
            line = str(line).split(',')
            print(line)
            print("卫星编号:", line[4])
            print("卫星仰角:", line[5])
            print("卫星方位角:", line[6])
            print("讯号噪声比:", line[7])