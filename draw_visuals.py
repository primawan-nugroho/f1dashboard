import pandas as pd
import plotly.express as px

def get_ranks(df):
    ranks = pd.DataFrame(df.groupby("Driver")["LapTime_seconds"].mean().fillna(0).sort_values(ascending=False)[::-1])
    ranks.reset_index(inplace=True)
    ranks = ranks.to_dict('list')
    return ranks

def draw_boxplot(df, raceweek_selector):
    boxplot = px.box(df[df['Raceweek']==raceweek_selector],
            x='Driver',
            y='LapTime_seconds',
            category_orders=get_ranks(df[df['Raceweek']==raceweek_selector]),
            title='Race Pace Analysis')
    return boxplot

'''def draw_minisector(df, driveer1, driver2):
    minisector = px.
    
    return minisector
'''