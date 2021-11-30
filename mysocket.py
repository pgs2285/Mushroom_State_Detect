import socket
import cv2
import pickle
import struct
import threading
import os 
import serial
import time
import cv2
from tensorflow.keras.models import load_model
import sqlite3
from datetime import datetime

conne = sqlite3.connect("humidyAndTemperature2.db", isolation_level=None, check_same_thread=False)
model = load_model('./model.hdf5')

ser = serial.Serial('COM4', 9600) # 1번카메라
ser2 = serial.Serial('COM8', 9600) # 3번카메라
ser3 = serial.Serial('COM9', 9600) # 2번카메라


ser.timeout = 1
ser2.timeout = 1
ser3.timeout =1



def run(conn, addr):
    data = b"" # 수신한 데이터를 넣을 변수
    idx = 0
    cnt = 0
    if os.path.exists(f"./img{addr[0]}") == False:
        os.mkdir(f"./img{addr[0]}")
    value = ['핀 발생기','생장기','수확기','과습']
    while True:
        data += conn.recv(4096)
        packet_size = struct.unpack(">L", data[:4])[0]
        while len(data) < packet_size:
            data += conn.recv(4096)

        img_size = struct.unpack(">L", data[4:8])[0]
        frame_data = data[8: 8+img_size]

        # 역직렬화(de-serialization) : 직렬화된 파일이나 바이트를 원래의 객체로 복원하는 것
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes") # 직렬화되어 있는 binary file로 부터 객체로 역직렬화
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR) # 프레임 디코딩
        try:
            cnt+=1
            humid, temp = struct.unpack(">LL", data[8 + img_size:packet_size + 4])
            if cnt % 50 == 0:
                finame = f"./img{addr[0]}/" + str(addr) + "_" + str(cnt) + ".jpg"
                cv2.imwrite(finame, frame)
                iframe = cv2.imread(finame)    
                    
                dst = cv2.resize(iframe, dsize=(150, 150))
                dst = dst.reshape(-1, 150, 150, 3)
                y_pred = model.predict(dst)
                pred = [y_pred[0][0], y_pred[0][1], y_pred[0][2]] 
                idx = str(pred.index(max(pred)))
                if addr[0] == '172.30.1.37' and iframe.mean() >= 120:
                    print("172.30.1.37 : 과습")
                    idx = '3'
                if addr[0] == '172.30.1.14':
                    c = conne.cursor()    
                    c.execute("CREATE TABLE IF NOT EXISTS boundary1 \
                        (idx int auto_increament, humid int, temperature int)")
                    state = idx.encode('utf-8')
                    ser.write(state)
                    if ser.readable():
                        sensor = ser.readline().decode()
                        dataS = sensor.split()
                        dt = datetime.now()
                        now_time = dt.strftime("%Y-%m-%d-%H-%M-%S")
                        c.execute(f"INSERT INTO boundary1 \
                        VALUES({now_time}, {dataS[0]}, {dataS[1]})")
                    
                elif addr[0] == '172.30.1.54':
                    c2 = conne.cursor() 
                    c2.execute("CREATE TABLE IF NOT EXISTS boundary2 \
                    (idx int auto_increament, humid int, temperature int)") 
                    state = idx.encode('utf-8')
                    ser3.write(state)
                    if ser3.readable():
                        sensor = ser3.readline().decode()
                        dataS = sensor.split()
                        dt = datetime.now()
                        now_time = dt.strftime("%Y-%m-%d-%H-%M-%S")
                        c2.execute(f"INSERT INTO boundary2 \
                        VALUES({now_time}, {dataS[0]}, {dataS[1]})")

                elif addr[0] == '172.30.1.37':
                    c3 = conne.cursor()
                    c3.execute("CREATE TABLE IF NOT EXISTS boundary3 \
                    (idx int auto_increament varchar, humid int, temperature int)") 
                    state = idx.encode('utf-8')
                    ser2.write(state)
                    if ser2.readable():
                        sensor = ser2.readline().decode()
                        dataS = sensor.split()
                        dt = datetime.now()
                        now_time = dt.strftime("%Y-%m-%d-%H-%M-%S")
                        c3.execute(f"INSERT INTO boundary3 \
                        VALUES({now_time}, {dataS[0]}, {dataS[1]})")
                        
                print(addr[0],':',value[int(idx)])

        
            data = data[packet_size+4:]
            idx = int(idx)
            idx+=1

        except:
            print('pass')
            pass
        

ip = '172.30.1.40' # ip 주소
port = 8080 # port 번호

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # 소켓 객체를 생성
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((ip, port)) # 바인드(bind) : 소켓에 주소, 프로토콜, 포트를 할당
s.listen(10) # 연결 수신 대기 상태(리스닝 수(동시 접속) 설정)
print('클라이언트 연결 대기')

while True:
    conn, addr = s.accept()
    print("클라이언트 접속 완료")
    t = threading.Thread(target=run, args=(conn, addr))
    t.start()