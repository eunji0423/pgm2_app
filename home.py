from altair import Key
import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import matplotlib.font_manager as fm
from dotenv import load_dotenv
import os

key=st.secrets['key']


st.header('첫 페이지')
url='http://api.sexoffender.go.kr/openapi/SOCitysStats/'
params={
    'serviceKey': Key
}

# api 호출
response=requests.get(url, params=params)
print(response.status_code)

if response.status_code==200:
    root=ET.fromstring(response.content)
    data=[]
    for city in root.findall('.//City'):
        data.append(
            {
                'city_name': city.find('city-name').text,
                'city_count': city.find('city-count').text
            }
        )
    df=pd.DataFrame(data)
    st.dataframe(df)
else:
    st.error('Failed to fetch data: [response.status_code]')

df['city_count']=df['city_count'].astype(int)
df_sorted=df.sort_values('city_count', ascending=False).head(10)
st.dataframe(df_sorted)

# 시각화
mpl.rcParams['font.family']='Malgun Gothic'
mpl.rcParams['font.size']=11
mpl.rcParams['axes.unicode_minus']=False

fig=plt.figure(figsize=(12, 6))
sns.barplot(x='city_name', y='city_count', data=df_sorted)
plt.xticks(rotation=45)
plt.title('지역별 성범죄 통계')
st.pyplot(fig)