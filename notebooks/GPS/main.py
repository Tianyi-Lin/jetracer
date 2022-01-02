import L76X
import time
import math
import pymysql


# update_pos和insert_pos切换
key = 1
# 0——update，1——insert
# 位置更新频率
f = 0.4


def update_pos(Lon, Lat):
    db = pymysql.connect(host="123.56.147.189", port=3306, user='raspberry', passwd='ty111111', db='raspberry', charset='utf8')
    print ('login in db successfully!') 
    cursor = db.cursor()
    update = "UPDATE GPS_DATA SET longtitude ='" + str(Lon) + "', latitude ='" + str(Lat) + "' WHERE id = 0"
    try:
        cursor.execute(update)
        db.commit()
        print ('db update successfully')
    except:
        db.rollback()
        print ('db update fail')
    db.close()
    

def insert_pos(Lon, Lat, tag):
    db = pymysql.connect(host="123.56.147.189", port=3306, user='raspberry', passwd='ty111111', db='raspberry', charset='utf8')
    print ('login in db successfully!') 
    cursor = db.cursor()
    # INSERT INTO `GPS_DATA`(`longtitude`, `latitude`, `id`) VALUES (lon,la,tag)
    insert = "INSERT INTO GPS_DATA (longtitude, latitude, id) VALUES (%s, %s, %s)"
    try:
        cursor.execute(insert,(Lon,Lat,tag))
        db.commit()
        print ('db insert successfully')
    except:
        db.rollback()
        print ('db insert fail')
    db.close()
    
    
def db_init(Lon_init, Lat_init):
    db = pymysql.connect(host="123.56.147.189", port=3306, user='raspberry', passwd='ty111111', db='raspberry', charset='utf8')
    print ('login in db successfully!') 
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS GPS_DATA")
    print ('db DROP TABLE!')
    sql1 = '''CREATE TABLE GPS_DATA (longtitude varchar(10), latitude varchar(10), id int(10))'''
    # id号字符长度为10,预留足够长度给insert插入时的时间戳
    cursor.execute(sql1)
    print ('db CREATE TABLE ok')
    sql2 = "INSERT INTO GPS_DATA (longtitude, latitude, id) VALUES (%s, %s, %s)"
    print ("INSERT INTO GPS_DATA (longtitude, latitude, id) VALUES", (Lon_init, Lat_init, 0))
    cursor.execute(sql2, (Lon_init, Lat_init, 0))
    db.commit()
    print ('db init ok')

# try:
x = L76X.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)

x.L76X_Send_Command(x.SET_POS_FIX_400MS)

# Set output message
x.L76X_Send_Command(x.SET_NMEA_OUTPUT)


x.L76X_Exit_BackupMode()


# ---------------------------------
# database init 初始化
x.L76X_Gat_GNRMC()
print (x.Lon,x.Lat)
db_init(x.Lon,x.Lat)
# ---------------------------------


# h = 0
# m = 0
# s = 0
# h1 = 0
# m1 = 0
# s1 = 0

# m1 = math.floor(time.time())/60 % 60
# h1 = math.floor(time.time())/3600 % 60
# s1 = math.floor(time.time()) % 60

# if m1 >= 59:
#     h1 = h1 + 1
#     m1 = m1 + 1 - 60
# m1 = m1 + 1


# tag时间戳，从1开始，id=0预留给初始化
tag = 1

while 1:
    x.L76X_Gat_GNRMC()
    if x.Status == 1:
        print('Already positioned')
    else:
        print('No positioning')
    print('Time %d:'%x.Time_H, end='')
    print('%d:'%x.Time_M, end='')
    print('%d'%x.Time_S)

    print('Lon = %f'%x.Lon, end='')
    print(' Lat = %f'%x.Lat)
    
    # --------------------------------------
    if(key == 0):
        update_pos(x.Lon, x.Lat)
    if(key == 1):
        insert_pos(x.Lon, x.Lat, tag)
    
    tag = tag + 1
    print("当前时间戳：", tag)
    # ---------------------------------------
    
    x.L76X_Baidu_Coordinates(x.Lat, x.Lon)
    print('Baidu coordinate %f'%x.Lat_Baidu, end='')
    print(',%f'%x.Lon_Baidu)
    
    time.sleep(f)
    
#     m = math.floor(time.time())/60 % 60
#     h = math.floor(time.time())/3600 % 60
#     s = math.floor(time.time()) % 60
#     if h >= h1 and m >= m1 and s >= s1:
#         print("Enter backup mode \r\n")
#         x.L76X_Send_Command(x.SET_PERPETUAL_BACKUP_MODE)
#         input("Please enter any character to exit backup mode\r\n")
#         print("Exit backup mode \r\n")
#         x.L76X_Exit_BackupMode()
#         m1 = math.floor(time.time())/60 % 60
#         h1 = math.floor(time.time())/3600 % 60
#         m1 = m1 + 1
#         if m1 >= 59:
#             h1 = h1 + 1
#             m1 = m1 + 1 - 60
        
# except:
    # GPIO.cleanup()
    # print "\nProgram end"
    # exit()
