import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

import fastf1 as ff1
from fastf1 import plotting
plotting.setup_mpl()

from draw_visuals import get_ranks, draw_boxplot

st.set_page_config(layout='wide')

df = pd.read_csv("2022_race.csv")

f1_cal = ['BAHRAIN GP',
            'SAUDI ARABIAN GRAND PRIX',
            'AUSTRALIAN GP',
            'EMILIA ROMAGNA GRAND PRIX',
            'MIMI GRAND PRIX',
            'SPANISH GP',
            'MONACO GP',
            'AZERBAIJAN GP',
            'CANADIAN GP',
            'BRITISH GP',
            'AUSTRIAN GP',
            'FRENCH GRAND PRIX',
            'HUNGARIAN GP',
            'BELGIAN GP',
            'DUTCH GRAND PRIX',
            'ITALIAN GP',
            'SINGAPORE GP',
            'JAPANESE GP',
            'UNITED STATES GP',
            'MEXICAN GP']
#color scheme
fer = ff1.plotting.team_color('ferrari')
rbr = ff1.plotting.team_color('RBR')
mer = ff1.plotting.team_color('mercedes')
alf = ff1.plotting.team_color('alfa romeo')
ast = ff1.plotting.team_color('aston martin')
mcl = ff1.plotting.team_color('mclaren')
alt = ff1.plotting.team_color('alphatauri')
wil = ff1.plotting.team_color('williams')
alp = ff1.plotting.team_color('alpine')
has = '#adadad' #has putih, ga keliatan, dibikin agak abu biar keliaan

sidebar = st.sidebar
raceweek_selector = sidebar.selectbox(
    "Select Race Week",
    f1_cal
)

st.markdown(f'## F1 2022 - {raceweek_selector}')

show_data = sidebar.checkbox("Show Data")
if show_data:
    st.dataframe(df[df['Raceweek']==raceweek_selector])

boxplot = draw_boxplot(df[df['Raceweek']==raceweek_selector], raceweek_selector)
st.plotly_chart(boxplot)

sns.axes_style('whitegrid')
box_plt, ax = plt.subplots()
ax = sns.boxplot(data=df[df['Raceweek']==raceweek_selector], x='Driver', y='LapTime_seconds')
st.pyplot(box_plt)