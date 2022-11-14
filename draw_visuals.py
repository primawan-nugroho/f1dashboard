import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import fastf1 as ff1

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

def draw_minisector(df, raceweek_selector, driver1, driver2):
    df_raceweek = df[df['Raceweek']==raceweek_selector]
    laps_driver1 = df_raceweek[df_raceweek['Driver']==driver1]
    laps_driver2 = df_raceweek[df_raceweek['Driver']==driver2]

    fastest_driver1 = laps_driver1.pick_fastest().get_telemetry().add_distance()
    fastest_driver2 = laps_driver2.pick_fastest().get_telemetry().add_distance()
    print(fastest_driver1)
    #return plt