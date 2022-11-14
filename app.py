import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

import fastf1 as ff1
from fastf1 import plotting
plotting.setup_mpl()

from draw_visuals import draw_boxplot, draw_minisector

st.set_page_config(layout='wide')

df_race = pd.read_csv("2022_race.csv")
df_qualification = pd.read_csv("2022_qualification.csv")

f1_cal = ['BAHRAIN GP',
            'SAUDI ARABIAN GRAND PRIX',
            'AUSTRALIAN GP',
            'EMILIA ROMAGNA GRAND PRIX',
            'MIAMI GRAND PRIX',
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
            'MEXICAN GP',
            'BRAZILIAN GP']

sidebar = st.sidebar
raceweek_selector = sidebar.selectbox(
    "Select Race Week",
    f1_cal
)

st.markdown(f'## F1 2022 - {raceweek_selector}')

show_data = sidebar.checkbox("Show Data")
if show_data:
    st.dataframe(df_race[df_race['Raceweek']==raceweek_selector])

#boxplot = draw_boxplot(df[df['Raceweek']==raceweek_selector], raceweek_selector)
#st.plotly_chart(boxplot)

pace_analysis = draw_boxplot(df_race, raceweek_selector)
st.pyplot(pace_analysis)

draw_minisector(df_qualification, raceweek_selector, 'VER', 'HAM')