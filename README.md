# Mushroom_State_Detect
clients.py: 라즈베리파이에 부착된 웹캠을 통해 이미지데이터를 main pc로 보내주는 코드 
mysocket.py : 1.main pc에서 socket통신을 받기위해 사용. 2.모델 판단하고 아두이노에 값을 보내줌  
sketch_oct25a.ino : 아두이노에 탑재된 하드웨어 제어 코드. mysocket.py에서 값을 받아서 처리함
stream.py   :  스트림릿 웹페이지 
