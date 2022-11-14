import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

import fastf1 as ff1
from fastf1 import plotting
plotting.setup_mpl()

from draw_visuals import draw_boxplot, draw_minisector, draw_stint

st.set_page_config(layout='wide')

df_race = pd.read_csv("2022_race.csv")
df_qualification = pd.read_csv("2022_qualification.csv")
df_telemetry_fastest_Q = pd.read_csv('2022_telemetry_fastest_Q.csv')

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
if show_data: st.dataframe(df_race[df_race['Raceweek']==raceweek_selector])

show_race_pace = sidebar.checkbox("Race Pace")
if show_race_pace:
    pace_analysis = draw_boxplot(df_race, raceweek_selector)
    st.pyplot(pace_analysis)

show_quali_minisector = sidebar.checkbox("Fastest Mini Sector Qualification")
if show_quali_minisector:
    minisector_analysis = draw_minisector(df_telemetry_fastest_Q, raceweek_selector)
    st.pyplot(minisector_analysis)

show_stint_strategy = sidebar.checkbox("Stint Strategy")
if show_stint_strategy:
    stint_analysis = draw_stint(df_race, raceweek_selector)
    st.pyplot(stint_analysis)

#boxplot = draw_boxplot(df[df['Raceweek']==raceweek_selector], raceweek_selector)
#st.plotly_chart(boxplot)