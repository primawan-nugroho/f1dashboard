import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

import fastf1 as ff1
from fastf1 import plotting
plotting.setup_mpl()

from draw_visuals import draw_boxplot, draw_minisector, draw_stint, draw_boxplot_plotly

st.set_page_config(page_title="F1 Dashboard",
                    layout='wide',
                    page_icon=":racing_car:")

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

st.markdown(f'## BALAPAN F1 2022 nich - {raceweek_selector}')

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

boxplot = draw_boxplot_plotly(df_race, raceweek_selector)
boxplot.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(boxplot)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)