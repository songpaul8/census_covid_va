
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import datapane as dp

db = 'covid-19.db'
dp.login(token = '')  # enter a datapane token here, otherwise app link is provided at bottom of py file.

#### sql functions
def query(prompt):
    with sqlite3.connect(db) as conn:
        return pd.read_sql(prompt, conn)

def command(c):
    with sqlite3.connect(db) as conn:
        conn.isolation_level = None
        conn.execute(c)

####  sqlite prompt
# this prompt selects covid case counts on the last recorded day (04/27) to visualize cumulative cases
# this cuts the dataset down to just one observation per FIPS code.
# new variables added are: black_african_american_pop_percent, hispanic_pop_percent, asian_pop_percent, minority_pop_percent, 
# covid_rate, minority_density and group_pop_percent
p1 = '''
SELECT *, black_african_american/total_population as 'black_african_american_pop_percent', hispanic_latino/total_population as 'hispanic_pop_percent',
asian/total_population as 'asian_pop_percent', (total_population - white)/total_population as 'minority_pop_percent',
num_cases/total_population as 'covid_rate', group_quarters_population/total_population as 'group_pop_percent',
CASE
WHEN (total_population - white)/total_population <= .20 THEN 'low'
WHEN (total_population - white)/total_population >= .20 AND (total_population - white)/total_population <= .5 THEN 'med'
ELSE 'high'
END as 'minority_density'
FROM census natural join locations natural join covid_cases
WHERE case_date == '2022-12-24 00:00:00'
'''


#### creating a dataframe from our SQL db
df = query(p1)

df_density = pd.DataFrame({'minority_density':['low', 'med', 'high']})
df_density['density_dummy'] = df_density.index
df = pd.merge(df, df_density, on = 'minority_density', how = 'left')

#### additional feature transformation
# adding the difference from the mean covid_rate for each county
df['covid_rate_diff'] = df['covid_rate'] - df['covid_rate'].mean()


#### parallel coordinate plot to map total covid cases to different minority densities
dimensions = list([dict(range = [df['covid_rate'].min(), df['covid_rate'].max()],
                        label = 'COVID Infection Rate', values = df['covid_rate']),
                   dict(range = [df['num_cases'].min(), df['num_cases'].max()],
                        label = 'Total Cases', values = df['num_cases']),
                   dict(range = [df['black_african_american_pop_percent'].min(), df['black_african_american_pop_percent'].max()],
                        label = 'Black or African American Population', values = df['black_african_american_pop_percent']),
                   dict(range = [df['hispanic_pop_percent'].min(), df['hispanic_pop_percent'].max()],
                        label = 'Hispanic Population', values = df['hispanic_pop_percent']),
                   dict(range = [df['minority_pop_percent'].min(), df['minority_pop_percent'].max()],
                        label = 'Minority Population', values = df['minority_pop_percent']),
                   dict(range = [0, 2], label = 'Minority Density', values = df['density_dummy'],
                        tickvals = [0, 1, 2], ticktext = ['low', 'med', 'high'])
                   ])
fig1 = go.Figure(data =
                 go.Parcoords(
                     line = dict(color = df['density_dummy'],
                                 colorscale = [[0, 'lightseagreen'],[0.5, 'lightgoldenrodyellow'],[1, 'indianred']]),
                     dimensions = dimensions))

#### computing averages
# avg covid rates for high/med/low minority populations
high_minority_cr = round(df.loc[df['minority_pop_percent'] > 0.5]['covid_rate'].mean(), 3)
med_minority_cr = round(df.loc[(df['minority_pop_percent'] > 0.2) & (df['minority_pop_percent'] <= 0.5)]['covid_rate'].mean(), 3)
low_minority_cr = round(df.loc[df['minority_pop_percent'] <= 0.2]['covid_rate'].mean(), 3)

# avg distance from mean covid rate for high/med/low minority populations
b_high = df.loc[df['black_african_american_pop_percent'] > 0.5]['covid_rate_diff'].mean()
b_med = df.loc[(df['black_african_american_pop_percent'] > 0.2) & (df['black_african_american_pop_percent'] <= 0.5)]['covid_rate_diff'].mean()
b_low = df.loc[df['black_african_american_pop_percent'] <= 0.2]['covid_rate_diff'].mean()

h_high = df.loc[df['hispanic_pop_percent'] > 0.5]['covid_rate_diff'].mean()
h_med = df.loc[(df['hispanic_pop_percent'] > 0.2) & (df['hispanic_pop_percent'] <= 0.5)]['covid_rate_diff'].mean()
h_low= df.loc[df['hispanic_pop_percent'] <= 0.2]['covid_rate_diff'].mean()

#### bar plot displaying the difference of COVID rates from the mean for counties with different minority makeups
fig2 = px.bar(
    x = ['Low (<20%)', 'Medium (20-50%)', 'High (>50%)'],
    y = [b_low, b_med, b_high],
    color_discrete_sequence = ['darkolivegreen'],
    title = 'Black/African American Population vs Difference from mean COVID rate',
    labels = {'x':'Black/African American Population', 'y':'Difference from Mean'}
    )

fig3 = px.bar(
    x = ['Low (<20%)', 'Medium (20-50%)', 'High (>50%)'],
    y = [b_low, b_med, b_high],
    color_discrete_sequence = ['darkslateblue'],
    title = 'Hispanic Population vs Difference from mean COVID rate',
    labels = {'x':'Hispanic Population', 'y':''}
    )

#### analyzing group quarters population vs covid rates
fig4 = px.scatter(
    df,
    x = 'group_pop_percent',
    y = 'covid_rate',
    color_discrete_sequence = ['lightsalmon'],
    trendline = 'ols',
    trendline_color_override = 'maroon',
    title = 'Group Housing Population vs COVID rate',
    labels = {'group_pop_percent':'Group Housing Population %', 'covid_rate':'COVID Infection Rate'}
    )

#### 3D heatmap to visualize how group quarters and minority population density may be effecting COVID rates

fig5 = go.Figure(
    data = go.Contour(
        z = df['covid_rate'],
        x = df['black_african_american_pop_percent'],
        y = df['group_pop_percent'],
        contours = dict(showlabels = True, labelfont = dict(size = 12, color = 'white')),
        colorbar = dict(title = 'Covid Rate', titleside = 'top'),
        colorscale = 'viridis',
        hovertemplate = "covid rate: %{z}<br>group housing pop: %{y}<br>african american pop: %{x}<extra></extra>",
        )
    )
fig5.update_layout(
    xaxis_title = 'Black/African American Population',
    yaxis_title = 'Group Housing Population',
    title = {'text':'Black/African American + Group Housing Population vs COVID rate', 'xanchor':'center', 'yanchor':'top', 'x':0.5}
    )

fig6 = go.Figure(
    data = go.Contour(
        z = df['covid_rate'],
        x = df['hispanic_pop_percent'],
        y = df['group_pop_percent'],
        contours = dict(showlabels = True, labelfont = dict(size = 12, color = 'white')),
        colorbar = dict(title = 'Covid Rate', titleside = 'top'),
        colorscale = 'viridis',
        hovertemplate = "covid rate: %{z}<br>group housing pop: %{y}<br>hispanic pop: %{x}<extra></extra>",
        )
    )
fig6.update_layout(
    xaxis_title = 'Hispanic Population',
    yaxis_title = 'Group Housing Population',
    title = {'text':'Hispanic + Group Housing Population vs COVID rate', 'xanchor':'center', 'yanchor':'top', 'x':0.5}
    )


#### pushing all objects to our datapane
dp.Report(
    dp.Group(
        dp.BigNumber(heading = 'VA Counties/GEOIDs', value = len(df)),
        dp.BigNumber(heading = 'COVID tracking start date', value = '01/22/2020'),
        dp.BigNumber(heading = 'COVID tracking end date', value = '12/24/2022'),
        dp.BigNumber(heading = 'Average rate of COVID', value = round(df['covid_rate'].mean(), 3)),
        columns = 4
        ),
    dp.Group(
        dp.BigNumber(heading = 'High Minority Population(>50% of total population) COVID rate', value = high_minority_cr),
        dp.BigNumber(heading = 'Med Minority Population(20-50% of total population) COVID rate', value = med_minority_cr),
        dp.BigNumber(heading = 'Low Minority Population(<20% of total population) COVID rate', value = low_minority_cr),
        ),
    dp.Plot(fig1),
    dp.Group(
        dp.Plot(fig2),
        dp.Plot(fig3),
        columns = 2,
        ),
    dp.Plot(fig4),
    dp.Text(text = '## Group Housing + Minority Population Density vs COVID-19 infection rate'),
    dp.Plot(fig5),
    dp.Plot(fig6),
    dp.DataTable(df)
).upload(name='VA Covid-19 and Census DB')

#### datapane URL: https://cloud.datapane.com/apps/mA26ZjA/va-covid-19-and-census-db/
    
