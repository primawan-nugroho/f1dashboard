# import standard python library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# import f1 library
import fastf1 as ff1
from fastf1 import plotting
plotting.setup_mpl()

ff1.Cache.enable_cache('../F1/cache')

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
            'MEXICAN GP',
            'BRAZILIAN GP']
            #'ABU DHABI GP]'

def get_race(year, race, weekend, LIMIT_OUTLIER = 1000):
    session = ff1.get_session(year, race, weekend)
    session.load()
    SAI = session.laps.pick_driver('SAI')
    PER = session.laps.pick_driver('PER')
    HAM = session.laps.pick_driver('HAM')
    LEC = session.laps.pick_driver('LEC')
    ALO = session.laps.pick_driver('ALO')
    NOR = session.laps.pick_driver('NOR')
    VER = session.laps.pick_driver('VER')
    MSC = session.laps.pick_driver('MSC')
    VET = session.laps.pick_driver('VET')
    MAG = session.laps.pick_driver('MAG')
    STR = session.laps.pick_driver('STR')
    LAT = session.laps.pick_driver('LAT')
    RIC = session.laps.pick_driver('RIC')
    TSU = session.laps.pick_driver('TSU')
    OCO = session.laps.pick_driver('OCO')
    GAS = session.laps.pick_driver('GAS')
    BOT = session.laps.pick_driver('BOT')
    RUS = session.laps.pick_driver('RUS')
    ZHO = session.laps.pick_driver('ZHO')
    ALB = session.laps.pick_driver('ALB')
    DEV = session.laps.pick_driver('DEV')
    HUL = session.laps.pick_driver('HUL')
    
    df_local = pd.concat([SAI, PER, HAM, LEC, ALO, NOR, VER, MSC, VET,MAG,
                STR, LAT, RIC, TSU, OCO, GAS, BOT, RUS, ZHO, ALB, DEV, HUL])
    df_local.reset_index(inplace=True, drop=True)
    
    # convert LapTime in timedelta64 to float in seconds
    df_local['LapTime_seconds'] = df_local['LapTime'].dt.seconds*1000000 + df_local['LapTime'].dt.microseconds
    df_local['LapTime_seconds'] = df_local['LapTime_seconds']/1000000
    
    # buang data yg IsAccurate == False
    df_local = df_local.drop(df_local[df_local.IsAccurate == False].index)

    # fine tuning, buang outlier yg ga logis
    df_local = df_local.drop(df_local[df_local.LapTime_seconds > LIMIT_OUTLIER].index)

    # add column raceweek
    df_local['Raceweek'] = race

    # hitung ranks untuk kebutuhan sorting
    ranks = pd.DataFrame(df_local.groupby("Driver")["LapTime_seconds"].mean().fillna(0).sort_values(ascending=False)[::-1])
    ranks.reset_index(inplace=True)
    ranks = ranks.to_dict('list')

    telemetry = pd.DataFrame()

    if(weekend=='Q'):
        laps = session.load_laps(with_telemetry=True)
        #Select lap for 2 fastest driver
        driver1 = laps[laps['LapTime'] == laps['LapTime'].sort_values().iloc[0]]['Driver'].to_string(index=False, header=False)
        driver2 = laps[laps['LapTime'] == laps['LapTime'].sort_values().iloc[1]]['Driver'].to_string(index=False, header=False)
        
        # Check whether driver1 == driver2, if yes then pick new fastest
        i = 2
        while driver1 == driver2:
            driver2 = laps[laps['LapTime'] == laps['LapTime'].sort_values().iloc[i]]['Driver'].to_string(index=False, header=False)
            i += 1

        laps_driver1 = laps.pick_driver(driver1)
        laps_driver2 = laps.pick_driver(driver2)
    
        # Get the telemetry data from their fastest lap
        fastest_driver1 = laps_driver1.pick_fastest().get_telemetry().add_distance()
        fastest_driver2 = laps_driver2.pick_fastest().get_telemetry().add_distance()

        # Since the telemetry data does not have a variable that indicates the driver, we need to create that column
        fastest_driver1['Driver'] = driver1
        fastest_driver2['Driver'] = driver2

        # Merge both lap telemetries so we have everything in one DataFrame
        telemetry = pd.concat([fastest_driver1, fastest_driver2])

    return df_local, telemetry

df_R = pd.DataFrame()
df_Q = pd.DataFrame()

# get RACE and QUALIFICATION session and export to csv
for raceweek in f1_cal:
    # get RACE data every race week and concat to df_R
    df_R_temp = get_race(2022, raceweek, 'R', 1000)
    df_R = pd.concat([df_R, df_R_temp])
    # get QUALIFICATION data every race week and concat to df_Q
    df_Q_temp = get_race(2022, raceweek, 'Q', 1000)
    df_Q = pd.concat([df_Q, df_Q_temp])
df_R.to_csv("2022_race.csv")
df_Q.to_csv("2022_qualification.csv")
