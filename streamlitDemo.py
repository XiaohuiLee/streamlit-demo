# Title     : streamlitDemo.py
# Objective : 
# Created by: L.X.H.
# Created on: 2020/9/21

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

st.title("streamlit demo")
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    df['date'] = pd.to_datetime(df['transaction_date']).dt.date
    df['price'] = df['price'].str.replace(",",'').astype(float)
    return df

df = load_data("SalesJan2009.csv")
st.table(df.head(5))


# charts
st.title('使用streamlit的api画图')
sub_df = df[['date', 'price']]
sub_df = sub_df.groupby('date').agg(sum)
st.line_chart(sub_df["price"])


st.title('使用plotly的api画图')
fig = ff.create_distplot([sub_df['price']], group_labels = ['price'], bin_size=2500)
st.plotly_chart(fig, use_container_width=True)

st.title('使用Matplotlib的api画图')
fig, ax = plt.subplots()
ax.hist(df['price'], bins=20)
st.pyplot(fig)


# sidebar插件
product_list = df["product"].unique()

product_type = st.sidebar.selectbox(
    "Which kind of event do you want to explore?",
    product_list
)
country_list = df["country"].unique()

country_name = st.sidebar.selectbox(
    "Which Country do you want to explore?",
    country_list
)

part_df = df[(df["product"] == product_type) & (df['country'] == country_name)]
st.write(f"根据你的筛选，数据包含{len(part_df)}行")


# map
st.title('地图的使用')
st.map(part_df)