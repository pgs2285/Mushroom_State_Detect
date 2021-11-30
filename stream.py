import numpy as np
import cv2
import streamlit as st
import time
import pandas as pd
from PIL import Image
from tensorflow.keras.models import load_model
from pandas import Series, DataFrame
from glob import glob
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
import sqlite3
# font_path = "C:/Windows/Fonts/NGULIM.TTF"
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font, size=10)
st.set_page_config(layout="wide")

cam1,cam2,cam3 = st.columns(3)
model = load_model('./model.hdf5')

conn = sqlite3.connect("humidyAndTemperature2.db", isolation_level=None)
c = conn.cursor()
c.execute("SELECT * FROM table1")
st.markdown("""
<style>
.title{
    text-align: center; 
    color: #0B2161;
    margin-bottom: 20px;
}
.header {    
    font-size:28px !important;
    font-weight: bold;
}
.subject {
    font-size:24px !important;
    margin-left: 20px;
    margin-bottom: 20px;
    color: #2E2E2E;
}
.sensor {
    font-size:24px !important;
    color: #045FB4;
}
.result {
    font-size:24px !important;
    color: DodgerBlue;
}
.warning {
    font-size:24px !important;
    color: red;
}
.time {
    font-size:14px !important;
    text-align: right !important;
    margin-right: 5px;
}
.bold {
    font-size:22px !important;
    font-weight: bold;
}
.top{
    margin-top: -90px;
}
table, td, tr, th {
    font-size: 17px;
    margin-top: -60px;
    text-align: center !important;
}
tr...{
    background-color: #bbdefb;
  }
</style>
""", unsafe_allow_html=True)

if __name__ == '__main__':
#     st.title('표고버섯 생육단계 및 과습여부 모니터링 시스템')
    if cam1.button("1번 구역"):
        st.markdown("<h1 class='title'>표고버섯 생육단계 및 과습 모니터링 시스템</h1><br>", unsafe_allow_html=True)

        c.execute("SELECT * FROM table1")

        label_text = np.array(['핀 발생기', '생장기', '수확기'])
        
        col1, col2 = st.columns(2)
        with col1:
            # col1.header("카메라 모니터링")
            st.markdown('<p class="header">카메라 모니터링</p>', unsafe_allow_html=True)
            # col1.image("./mush_normal.jpg", use_column_width=True)
            
        with col2:
            # st.header("현재 생육환경")
            st.markdown('<p class="header">현재 생육환경</p>', unsafe_allow_html=True)

    
        col1, col2, col3, col4 = st.columns([3,2,2,1])

        imgs = glob("./img172.30.1.14/*.jpg")
        length = len(imgs) - 1

        col1.image(imgs[length], use_column_width=True)

        col2.metric("온도")
        col3.metric("습도")
        col2.metric(c.fetchone())
        # col3.markdown('<text class="warning">과습주의!</text>', unsafe_allow_html=True) 
 
        # col4.metric("생육시기", "핀발생기")
        
        col1, col2 = st.columns([1,1])
    
        col1.markdown('<p class="header">AI기반 실시간 생육시기 판별</p>', unsafe_allow_html=True)
        result_code = '''
            <text class="subject">현재 표고버섯의 생육시기는</text>
            &nbsp&nbsp
            <text class="sensor"> "'''
        result = model.predict(imgs[length])
        li = [result[0][0], result[0][1], result[0][2]]
        result_code += label_text[li.index(max(li))]
        result_code += label_text[li]
        result_code += '"</text><text class="subject"> 입니다</text>'
        col1.markdown(result_code, unsafe_allow_html=True)
        
        st.markdown('<br>', unsafe_allow_html=True) 
        col2.markdown('<p class="bold top">생육시기별 최적 온습도</p>', unsafe_allow_html=True)

        env_data = {'col0': ['10~12', '9~11', '9~11'],
                    'col1': [ '80~90', '80~90', '60~70']}

        df = DataFrame(env_data)
        df.columns = [ '온도(℃)', '습도(%)']
        df.index = ['핀발생기', '생장기', '수확기']
        ## 특정 위치의 배경색 바꾸기
        # col2.dataframe(df) 

        col2.table(df)
        
    #     st.error("습도가 너무 높습니다.")
    #     st.success("Success")
    if cam2.button("2번 구역"):
        st.markdown("<h1 class='title'>표고버섯 생육단계 및 과습 모니터링 시스템</h1><br>", unsafe_allow_html=True)

        
        label_text = np.array(['핀 발생기', '생장기', '수확기'])
        
        col1, col2 = st.columns(2)
        with col1:
            # col1.header("카메라 모니터링")
            st.markdown('<p class="header">카메라 모니터링</p>', unsafe_allow_html=True)
            # col1.image("./mush_normal.jpg", use_column_width=True)
            
        with col2:
            # st.header("현재 생육환경")
            st.markdown('<p class="header">현재 생육환경</p>', unsafe_allow_html=True)
    #         temp_code = """
    #             <br>
    #             <text class="subject">현재 온도</text>
    #             &nbsp&nbsp&nbsp&nbsp
    #             <text class="sensor">25℃</text> """
    #         humi_code = """ 
    #             <text class="subject">현재 습도</text>
    #             &nbsp&nbsp&nbsp&nbsp
    #             <text class="sensor">94%</text> 
    #             &nbsp&nbsp&nbsp&nbsp"""
    #         humi_code += '<text class="warning">과습주의!</text>'
    #         st.markdown(temp_code, unsafe_allow_html=True) 
    #         st.markdown(humi_code, unsafe_allow_html=True) 
    #         my_bar = st.progress(0)
    #         my_bar.progress(90)
            
    
        col1, col2, col3, col4 = st.columns([3,1,1,1])

    #     with col1:
    #         now = time.localtime()
    #         now = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            # st.write(now)
            # st.markdown('<text class="time">'+now+'</text>', unsafe_allow_html=True)
        imgs = glob("./img172.30.1.54/*.jpg")
        length = len(imgs) - 1

        col1.image(imgs[length], use_column_width=True)

        col2.metric("온도")
        col3.metric("습도")
        col2.metric(c.fetchone())
        # col3.markdown('<text class="warning">과습주의!</text>', unsafe_allow_html=True) 

        # col4.metric("생육시기", "핀발생기")
        
        col1, col2 = st.columns([1,1])
        
        col1.markdown('<p class="header">AI기반 실시간 생육시기 판별</p>', unsafe_allow_html=True)
        result_code = '''
            <text class="subject">현재 표고버섯의 생육시기는</text>
            &nbsp&nbsp
            <text class="sensor"> "'''
        
        result = model.predict(imgs[length])
        li = [result[0][0], result[0][1], result[0][2]]
        result_code += label_text[li.index(max(li))]
        result_code += '"</text><text class="subject"> 입니다</text>'
        col1.markdown(result_code, unsafe_allow_html=True)
        
        st.markdown('<br>', unsafe_allow_html=True) 
        col2.markdown('<p class="bold top">생육시기별 최적 온습도</p>', unsafe_allow_html=True)

        env_data = {'col0': ['10~12', '9~11', '9~11'],
                    'col1': [ '80~90', '80~90', '60~70']}

        df = DataFrame(env_data)
        df.columns = [ '온도(℃)', '습도(%)']
        df.index = ['핀발생기', '생장기', '수확기']
        ## 특정 위치의 배경색 바꾸기
        # col2.dataframe(df) 

        col2.table(df)
        
    #     st.error("습도가 너무 높습니다.")
    #     st.success("Success")

    if cam3.button("3번 구역"):
        st.markdown("<h1 class='title'>표고버섯 생육단계 및 과습 모니터링 시스템</h1><br>", unsafe_allow_html=True)

        label_text = np.array(['핀 발생기', '생장기', '수확기'])
        
        col1, col2 = st.columns(2)
        with col1:
            # col1.header("카메라 모니터링")
            st.markdown('<p class="header">카메라 모니터링</p>', unsafe_allow_html=True)
            # col1.image("./mush_normal.jpg", use_column_width=True)
            
        with col2:
            # st.header("현재 생육환경")
            st.markdown('<p class="header">현재 생육환경</p>', unsafe_allow_html=True)
    #         temp_code = """
    #             <br>
    #             <text class="subject">현재 온도</text>
    #             &nbsp&nbsp&nbsp&nbsp
    #             <text class="sensor">25℃</text> """
    #         humi_code = """ 
    #             <text class="subject">현재 습도</text>
    #             &nbsp&nbsp&nbsp&nbsp
    #             <text class="sensor">94%</text> 
    #             &nbsp&nbsp&nbsp&nbsp"""
    #         humi_code += '<text class="warning">과습주의!</text>'
    #         st.markdown(temp_code, unsafe_allow_html=True) 
    #         st.markdown(humi_code, unsafe_allow_html=True) 
    #         my_bar = st.progress(0)
    #         my_bar.progress(90)
            
    
        col1, col2, col3, col4 = st.columns([3,1,1,1])

    #     with col1:
    #         now = time.localtime()
    #         now = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            # st.write(now)
            # st.markdown('<text class="time">'+now+'</text>', unsafe_allow_html=True)
        imgs = glob("./img172.30.1.37/*.jpg")
        length = len(imgs) - 1
        col1.image(imgs[length], use_column_width=True)

        col2.metric("온도")
        col3.metric("습도")
        col2.metric(c.fetchone())
        # col3.markdown('<text class="warning">과습주의!</text>', unsafe_allow_html=True) 

        # col4.metric("생육시기", "핀발생기")
        
        col1, col2 = st.columns([1,1])
    
        col1.markdown('<p class="header">AI기반 실시간 생육시기 판별</p>', unsafe_allow_html=True)
        result_code = '''
            <text class="subject">현재 표고버섯의 생육시기는</text>
            &nbsp&nbsp
            <text class="sensor"> "'''
        result = model.predict(imgs[length])    
        li = [result[0][0], result[0][1], result[0][2]]
        result_code += label_text[li.index(max(li))]
        result_code += '"</text><text class="subject"> 입니다</text>'
        col1.markdown(result_code, unsafe_allow_html=True)
        
        st.markdown('<br>', unsafe_allow_html=True) 
        col2.markdown('<p class="bold top">생육시기별 최적 온습도</p>', unsafe_allow_html=True)

        env_data = {'col0': ['10~12', '9~11', '9~11'],
                    'col1': [ '80~90', '80~90', '60~70']}

        df = DataFrame(env_data)
        df.columns = [ '온도(℃)', '습도(%)']
        df.index = ['핀발생기', '생장기', '수확기']
        ## 특정 위치의 배경색 바꾸기
        # col2.dataframe(df) 

        col2.table(df)

