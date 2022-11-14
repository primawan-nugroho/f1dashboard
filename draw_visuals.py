import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

import fastf1 as ff1

from matplotlib.collections import LineCollection
import matplotlib.colors

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

def get_ranks(df):
    ranks = pd.DataFrame(df.groupby("Driver")["LapTime_seconds"].mean().fillna(0).sort_values(ascending=False)[::-1])
    ranks.reset_index(inplace=True)
    ranks = ranks.to_dict('list')
    return ranks

def draw_boxplot_plotly(df, raceweek_selector):
    boxplot = px.box(df[df['Raceweek']==raceweek_selector],
            x='Driver',
            y='LapTime_seconds',
            category_orders=get_ranks(df[df['Raceweek']==raceweek_selector]),
            title='Race Pace Analysis')
    return boxplot

def draw_boxplot(df, raceweek_selector):
    df_raceweek = df[df['Raceweek']==raceweek_selector]
    df_raceweek.groupby("Driver")["LapTime_seconds"].median().sort_values()
    
    # buang data yg IsAccurate == False
    df_raceweek = df_raceweek.drop(df_raceweek[df_raceweek.IsAccurate == False].index)

    # fine tuning, buang outlier yg ga logis
    #df_raceweek = df_raceweek.drop(df_raceweek[df_raceweek.LapTime_seconds > LIMIT_OUTLIER].index)
    
    # ranking untuk masing-masing Driver dari nilai median() LapTime_seconds
    ranks = df_raceweek.groupby("Driver")["LapTime_seconds"].median().fillna(0).sort_values(ascending=False)[::-1].index

    # set palette dengan dictionary berdasarkan driver dan color scheme dari ff1
    my_palette ={'SAI':fer,
    'PER':rbr,
    'HAM':mer,
    'LEC':fer,
    'ALO':alp,
    'NOR':mcl,
    'VER':rbr,
    'MSC':has,
    'VET':ast,
    'MAG':has,
    'STR':ast,
    'LAT':wil,
    'RIC':mcl,
    'TSU':alt,
    'OCO':alp,
    'GAS':alt,
    'BOT':alf,
    'RUS':mer,
    'ZHO':alf,
    'ALB':wil,
    'HUL':ast,
    'DEV':wil}

    sns.set_style('white')
    plt.figure(figsize=(16,8))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    ax = sns.boxplot(data=df_raceweek, x='Driver', y='LapTime_seconds', order=ranks, palette=my_palette)

    #ax.set_title(f"Race Pace - F1 {RACE} GP {YEAR}")
    ax.set_ylabel('Lap Time (seconds)', fontsize=14)
    ax.set_xlabel('Driver', fontsize=14)
    ax.xaxis.set_label_coords(.5, -.15)

    medians = df_raceweek.groupby("Driver")["LapTime_seconds"].median().sort_values()

    # label median LapTime
    ax.text(-2.4, df_raceweek.LapTime_seconds.min()-1.2, "Lap Time Median")
    for xtick in ax.get_xticks():
        ax.text(xtick,
            df_raceweek.LapTime_seconds.min()-1.2, #adjust y value offset disini
            round(medians[xtick], 3),
            horizontalalignment = 'center',
            size = 11,
            color = 'black')

    # Label median LapTime gap to leader
    leader_median = medians[0]
    ax.text(-2.4, df_raceweek.LapTime_seconds.min()-1.45, "Gap to Leader")
    for xtick in ax.get_xticks():
        ax.text(xtick,
            df_raceweek.LapTime_seconds.min()-1.45, #adjust y value offset disini
            "+" + str(round(medians[xtick] - leader_median, 3)),
            horizontalalignment = 'center',
            size = 11,
            color = 'black')

    ax.text(0.9, 0.1,'@primawanugroho', ha='center', va='center', transform=ax.transAxes)

    return plt

def switch(driver):
    if driver=='VER' or driver=='PER': return rbr
    elif driver=='HAM' or driver=='RUS': return mer
    elif driver=='NOR' or driver=='RIC': return mcl
    elif driver=='LEC' or driver=='SAI': return fer
    elif driver=='VET' or driver=='STR' or driver=='HUL': return ast
    elif driver=='BOT' or driver=='ZHO': return alf
    elif driver=='TSU' or driver=='GAS': return alt
    elif driver=='MSC' or driver=='MAG': return has
    elif driver=='LAT' or driver=='ALB' or driver=='DEV': return wil
    elif driver=='ALO' or driver=='OCO': return alp

def draw_minisector(df, raceweek_selector):
    telemetry = df[df['Raceweek']==raceweek_selector]

    num_minisectors = 50   
    # Grab the maximum value of distance that is known in the telemetry
    total_distance = max(telemetry['Distance'])
    # Generate equally sized mini-sectors 
    minisector_length = total_distance / num_minisectors
    # Initiate minisector variable, with 0 (meters) as a starting point.
    minisectors = [0]
    # Add multiples of minisector_length to the minisectors
    for i in range(0, (num_minisectors - 1)):
        minisectors.append(minisector_length * (i + 1))

    telemetry['Minisector'] = telemetry['Distance'].apply(
        lambda dist: (
            int((dist // minisector_length) + 1)
        )
    )   
    # Calculate avg. speed per driver per mini sector
    average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()
    # Select the driver with the highest average speed
    fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]
    # Get rid of the speed column and rename the driver column
    fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

    # Join the fastest driver per minisector with the full telemetry
    telemetry = telemetry.merge(fastest_driver, on=['Minisector'])

    # Order the data by distance to make matploblib does not get confused
    telemetry = telemetry.sort_values(by=['Distance'])

    # Convert driver name to integer
    telemetry.loc[telemetry['Fastest_driver'] == telemetry['Driver'].unique()[0], 'Fastest_driver_int'] = 1
    telemetry.loc[telemetry['Fastest_driver'] == telemetry['Driver'].unique()[1], 'Fastest_driver_int'] = 2

    sns.set_style('white')
    
    x = np.array(telemetry['X'].values)
    y = np.array(telemetry['Y'].values)
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)

    cmap = matplotlib.colors.ListedColormap([switch(telemetry['Driver'].unique()[0]), switch(telemetry['Driver'].unique()[1])], name='from_list', N=None)
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
    lc_comp.set_array(fastest_driver_array)
    lc_comp.set_linewidth(5)
    
    plt.rcParams['figure.figsize'] = [18, 10]
    
    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
    
    #plt.title(f'FASTEST MINI SECTOR QUALIFICATION - F1 {raceweek_selector} GP 2022')
    
    cbar = plt.colorbar(mappable=lc_comp)#, boundaries=np.arange(1,5))

    return plt

def draw_stint(df, raceweek_selector):
    stint = df[df['Raceweek']==raceweek_selector]
    # bikin pivot pake groupby
    driver_stints = stint[['Driver', 'Stint', 'Compound', 'LapNumber']].groupby(
        ['Driver', 'Stint', 'Compound']).count().reset_index()
    driver_stints = driver_stints.rename(columns={'LapNumber': 'StintLength'})
    driver_stints = driver_stints.sort_values(by=['Stint'])
    compound_colors = {
        'SOFT': '#FF3333',
        'MEDIUM': '#FFF200',
        'HARD': '#EBEBEB',
        'INTERMEDIATE': '#39B54A',
        'WET': '#00AEEF',
    }
    fig, ax = plt.subplots()

    # loop setiap driver buat create stacked graph
    for driver in stint['Driver']:
        stints = driver_stints.loc[driver_stints['Driver'] == driver]

        previous_stint_end = 0
        for x, stint in stints.iterrows():
            plt.barh(
                [driver], 
                stint['StintLength'], 
                left=previous_stint_end, 
                color=compound_colors[stint['Compound']], 
                edgecolor = "black",
                linewidth=1
            )

            previous_stint_end = previous_stint_end + stint['StintLength']

    plt.title(f'Stint Strategy - {raceweek_selector} 2022')
    plt.xlabel('Lap')
    plt.gca().invert_yaxis()

    return fig