import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

sns.set(style='dark')



# Menyiapkan sewa berdasarkan cuaca
def create_weather_rent(df):
    df_weather_rent = df.groupby(by='weather_cond').agg({'count': 'sum'}).reset_index()
    return df_weather_rent

#Menyiapkan data sewa berdasarkan jam
def create_hourly_rent(df):
    df_hourly= df.groupby('hour').agg({
        'count': 'sum',
    })
    df_hourly=df_hourly.reset_index()
    return df_hourly

