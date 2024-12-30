import altair as alt
import pandas as pd

#Upload csv data
data = pd.read_csv("https://drive.google.com/uc?id=1r-6Cg7drGM_q3hAeqAJDTP7OMqXxj-gK")
data

data["STATUS"].unique()

#Delete rows with NaN in zip, created_date, closed_date
data = data.dropna(subset=['ZIP_CODE', 'CREATED_DATE', 'CLOSED_DATE'])

#Convert the 'creation_date' column to datetime object
data['CREATED_DATE'] = pd.to_datetime(data['CREATED_DATE'], format='%m/%d/%Y %I:%M:%S %p')

#Convert the 'closed_date' column to datetime object
data['CLOSED_DATE'] = pd.to_datetime(data['CLOSED_DATE'], format='%m/%d/%Y %I:%M:%S %p')

#Calculate time it took to fix potholes
data['FIXED_IN'] = data['CLOSED_DATE'] - data['CREATED_DATE']

#Filter for potholes created in 2023
data_2023 = data[data['CREATED_DATE'].dt.year == 2023]
data_2023

#Change the column name 'ZIP_CODE' to 'zip' so we can merge the GeoJSON and CSV
data_2023 = data_2023.rename(columns={'ZIP_CODE': 'zip'})
data_2023

#Take a random sample of 1000 datapoints because there are too many values to plot
data_2023Sample = data_2023.sample(n=1000, random_state=1)
data_2023Sample

data

data_2023Sample.info()

chicagoZipcodes = data_2023Sample["zip"].unique()

chicagoZipcodes = data_2023Sample["zip"].unique().tolist()
chicagoZipcodes

chicago_git = "https://gist.githubusercontent.com/sage7270/8b901b3ed67315918d4b31444d19248b/raw/38c9c985f7cae9d6893fb4b48da9655557aca78b/Chicago_zipcodes.geojson"
geodata_chicago = alt.Data(url=chicago_git, format=alt.DataFormat(property="features", type="json"))

chicago_land = alt.Chart(geodata_chicago).mark_geoshape(
    fill = 'lightgray',
    stroke = 'white'
).encode(
    alt.Tooltip(['properties.zip:N'])
).properties(
    width = 350,
    height = 600
).project(
    type='mercator'
)

chicago_land

#Convert 'fixed_in' to total seconds to use it as a field
data_2023Sample['FIXED_IN_SECONDS'] = data_2023Sample['FIXED_IN'].dt.total_seconds()

#Convert 'fixed_in' to string to string bc Altair doesn't support original format
data_2023Sample['FIXED_IN_STRING'] = data_2023Sample['FIXED_IN'].astype(str)

#Convert 'fixed_in' to use for tooltip later (maybe?)
data_2023Sample['FIXED_IN'] = data_2023Sample['FIXED_IN'].apply(
    lambda x: (
        f"{int(x.days)} days, " +
        f"{int(x.total_seconds() // 3600 % 24)} hours, " +
        f"{int((x.total_seconds() % 3600) // 60)} minutes, " +
        f"{int(x.total_seconds() % 60)} seconds"
    )
)

choropleth = alt.Chart(geodata_chicago).mark_geoshape(
    #fill = 'lightgray',
    stroke = 'white'
).transform_lookup(
    lookup='properties.zip',
    from_=alt.LookupData(data=data_2023Sample, key='zip', fields=['FIXED_IN_SECONDS'])
).encode(
    alt.Color('FIXED_IN_SECONDS:Q'),
    alt.Tooltip(['properties.zip:N', 'FIXED_IN_SECONDS:Q'])
).properties(
    width = 350,
    height = 600
).project(
    type='mercator'
)

choropleth

circles = alt.Chart(geodata_chicago).mark_circle().transform_lookup(
    lookup='properties.zip',
    from_=alt.LookupData(data=data_2023Sample, key='zip', fields=['FIXED_IN_SECONDS'])
).transform_calculate(centroid = alt.expr.geoCentroid(None, alt.datum)
).encode(
    longitude = 'centroid[0]:Q',
    latitude = 'centroid[1]:Q',
    size = 'FIXED_IN_SECONDS:Q'
).properties(
    width = 350,
    height = 600,
)

chicago_land + circles

import pandas as pd

chicagoPop_git = "https://raw.githubusercontent.com/emeliaaaa/Project-2-INFO-Viz/refs/heads/main/Chicago%20Population%20Counts%202021.csv"

# Load the CSV data into a pandas DataFrame
chicagoPop = pd.read_csv(chicagoPop_git)

chicagoPop = chicagoPop.rename(columns={'Geography': 'zip'})

chicagoPop.head()

new_chicagoPop = chicagoPop[['zip', 'Population - Total', 'Population - Age 0-17', 'Population - Age 70-79', 'Population - Female', 'Population - Male', 'Population - Latinx', 'Population - Asian Non-Latinx', 'Population - Black Non-Latinx', 'Population - White Non-Latinx', 'Population - Other Race Non-Latinx']]

# renaming them for easier reference
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Total': 'Total Population'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Age 0-17': 'Population Age 0-17'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Age 70-79': 'Population - Age 70-79'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Female': 'Female Population'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Male': 'Male Population'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Latinx': 'Latine Population'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Asian Non-Latinx': 'Asian Population'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Black Non-Latinx': 'Black Population'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - White Non-Latinx': 'White Population'})
new_chicagoPop = new_chicagoPop.rename(columns={'Population - Other Race Non-Latinx': 'Other Race Population'})

# creating a new df to make these proportions
proportion_chicagoPop = pd.DataFrame()

# calculating percents/proportions
proportion_chicagoPop['zip'] = new_chicagoPop['zip']
proportion_chicagoPop['Percent Age 0-17'] = (new_chicagoPop['Population Age 0-17'] / new_chicagoPop['Total Population']) * 100
proportion_chicagoPop['Percent Age 70-79'] = (new_chicagoPop['Population - Age 70-79'] / new_chicagoPop['Total Population']) * 100
proportion_chicagoPop['Percent Female'] = (new_chicagoPop['Female Population'] / new_chicagoPop['Total Population']) * 100
proportion_chicagoPop['Percent Male'] = (new_chicagoPop['Male Population'] / new_chicagoPop['Total Population']) * 100
proportion_chicagoPop['Percent Latine'] = (new_chicagoPop['Latine Population'] / new_chicagoPop['Total Population']) * 100
proportion_chicagoPop['Percent Asian'] = (new_chicagoPop['Asian Population'] / new_chicagoPop['Total Population']) * 100
proportion_chicagoPop['Percent Black'] = (new_chicagoPop['Black Population'] / new_chicagoPop['Total Population']) * 100
proportion_chicagoPop['Percent White'] = (new_chicagoPop['White Population'] / new_chicagoPop['Total Population']) * 100
proportion_chicagoPop['Percent Other Race'] = (new_chicagoPop['Other Race Population'] / new_chicagoPop['Total Population']) * 100
# adding a total POC one as well.
proportion_chicagoPop['Percent POC'] = ((new_chicagoPop['Latine Population'] +
                                  new_chicagoPop['Asian Population'] +
                                  new_chicagoPop['Black Population'] +
                                  new_chicagoPop['Other Race Population']) /
                                  new_chicagoPop['Total Population']) * 100

# proportion_chicagoPop.to_csv('proportion_chicagoPop.csv', index=False)

# if u wanted it as a csv file to save ^^

proportion_chicagoPop.head()

data.head()

# plan: group by 2021-2023 so far
# zipcode, so like get sums of all the potholes. and sums for each zipcode
# get proportions.
# merge them by zipcode with race data. then do pairplots

data_2023 = data[data['CREATED_DATE'].dt.year == 2023]
data_2023

# filtering for good range
data_2021_2023 = data[data['CREATED_DATE'].dt.year.isin([2021, 2022, 2023, 2024])]

data_2021_2023


potholes_by_zip = data_2021_2023.groupby('ZIP_CODE')['ZIP_CODE'].count().reset_index(name='pothole_count')
potholes_by_zip


potholes_by_zip = potholes_by_zip[potholes_by_zip['ZIP_CODE'] != 0]

# 2021 - 2023 pothole count
potholes_by_zip

potholeSum202123 = potholes_by_zip["pothole_count"].sum()
potholeSum202123

potholeSumProportions = pd.DataFrame()
potholeSumProportions['ZIP_CODE'] = potholes_by_zip['ZIP_CODE']
potholeSumProportions['Pothole Proportion'] = (potholes_by_zip['pothole_count'] / potholeSum202123) * 100

potholeSumProportions.sort_values(by='Pothole Proportion', ascending=False)

proportion_chicagoPop.head()

potholeSumProportions["ZIP_CODE"].round()

# Convert ZIP_CODE from float to int, then back to string to remove the .0
potholeSumProportions['ZIP_CODE'] = potholeSumProportions['ZIP_CODE'].astype(float).astype(int).astype(str)

# Now merge again
demogsPotholesmerged_df = pd.merge(potholeSumProportions, proportion_chicagoPop, left_on='ZIP_CODE', right_on='zip', how='inner')

# Display the merged dataframe
demogsPotholesmerged_df

potholeSumProportions.head()

proportion_chicagoPop.head()

import altair as alt

# Assuming demogsPotholesmerged_df is your DataFrame
alt.Chart(demogsPotholesmerged_df).mark_circle().encode(
    alt.X(alt.repeat("column"), type='quantitative'),
    alt.Y(alt.repeat("row"), type='quantitative'),
    tooltip=['ZIP_CODE', 'Pothole Proportion', 'Percent Age 0-17', 'Percent Age 70-79', 'Percent Female', 'Percent Male', 'Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race', 'Percent POC']
).properties(
    width=150,
    height=150
).repeat(
    row=['Percent Age 0-17', 'Percent Age 70-79', 'Percent Female', 'Percent Male', 'Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race', 'Percent POC'],
    column=['Pothole Proportion']
)

import altair as alt
import pandas as pd

# Calculate the correlation matrix
correlation_matrix = demogsPotholesmerged_df.corr()

# Reshape the correlation matrix using reset_index to create the desired columns
correlation_df = correlation_matrix.stack().reset_index()
# Rename the columns
correlation_df.columns = ['Variable 1', 'Variable 2', 'Correlation']

# Create a heatmap using Altair
alt.Chart(correlation_df).mark_rect().encode(
    alt.X('Variable 1:N'),
    alt.Y('Variable 2:N'),
    alt.Color('Correlation:Q', scale=alt.Scale(scheme='redblue'))
).properties(
    width=400,
    height=400
)

import pandas as pd

# Assuming demogsPotholesmerged_df is your DataFrame
correlation_matrix = demogsPotholesmerged_df.corr()

# Extract the correlation between 'Pothole Proportion' and 'Percent POC'
r_value = correlation_matrix.loc['Pothole Proportion', 'Percent POC']
r_value

# Assuming 'Number of Potholes' is the column that stores pothole counts
# This will calculate correlations between 'Number of Potholes' and all other numeric columns
correlations = demogsPotholesmerged_df.corr()['Pothole Proportion']

# Display the correlation values
print(correlations)

correlations.sort_values(ascending=False)

# Create a list of the variables you want to plot against Pothole Proportion
variables = ['Percent Latine', 'Percent Age 0-17', 'Percent POC', 'Percent Asian', 'Percent White','Percent Black']

# Create a list to store the charts
charts = []

# Loop through the variables and create a regression plot for each
for variable in variables:
  chart = alt.Chart(demogsPotholesmerged_df).mark_point().encode(
      x=alt.X(variable, type='quantitative'),
      y=alt.Y('Pothole Proportion', type='quantitative'),
      tooltip=['ZIP_CODE', variable, 'Pothole Proportion']
  ).properties(
      width=200,
      height=150
  )

  # Add a regression line
  chart += chart.transform_regression(variable, 'Pothole Proportion').mark_line(color='red')

  charts.append(chart)


# Concatenate the charts into a single chart using alt.vconcat
top_row = alt.hconcat(*charts[:3])
bottom_row = alt.hconcat(*charts[3:])
combined_chart = alt.vconcat(top_row, bottom_row)

combined_chart


"""Zipcode 60629 = Cook County
Zipcode 60632 = Also cook County
"""

# Chicago Community Vulnerability Index Data
# https://drive.google.com/file/d/1cVe4eGdQxnwrdEjB7QW6l0DZASZDXpZU/view?usp=sharing

ccvi = pd.read_csv("https://drive.google.com/uc?id=1cVe4eGdQxnwrdEjB7QW6l0DZASZDXpZU")
ccvi.head()
#Change the column name 'Community Area or ZIP Code' to 'zip' so we can merge the GeoJSON and CSV

ccviZIP = ccvi[ccvi['Geography Type'] == 'ZIP']

ccvi_zip_df = ccviZIP[['zip', 'CCVI Score', 'CCVI Category']].copy()
ccvi_zip_df.head()

# Rename the 'Community Area or ZIP Code' column to 'zip' for merging
ccvi_zip_df = ccvi_zip_df.rename(columns={'Community Area or ZIP Code': 'zip'})

# Convert the 'zip' column to string type in both DataFrames
ccvi_zip_df['zip'] = ccvi_zip_df['zip'].astype(str)
demogsPotholesmerged_df['ZIP_CODE'] = demogsPotholesmerged_df['ZIP_CODE'].astype(str)


# Merge the DataFrames on the 'zip' column
merged_df = pd.merge(demogsPotholesmerged_df, ccvi_zip_df, left_on='ZIP_CODE', right_on='zip', how='inner')

# Display the merged DataFrame
merged_df

merged_df.sort_values(by='CCVI Score', ascending=False).head(10)

top_5_ccvi

# Assuming 'merged_df' is your DataFrame with CCVI Score, Pothole Proportion, and race proportions
top_5_ccvi = merged_df.sort_values('CCVI Score', ascending=False).head(5)

# Create a stacked bar chart
alt.Chart(top_5_ccvi).mark_bar().encode(
    x=alt.X('ZIP_CODE:N', title='Zip Code',
      sort=alt.SortField('CCVI Score', order='descending')),
    y=alt.Y('CCVI Score:Q', title='CCVI Score'),
    color=alt.Color(
        'Race:N',
        title='Race',
        scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race']),
        legend=alt.Legend(orient='bottom')
    )
).transform_fold(
    ['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
    as_=['Race', 'Proportion']
).properties(
    title='Top 5 Zip Codes with Highest CCVI Scores & Pothole Proportion by Race'
)

# Assuming 'merged_df' is your DataFrame with CCVI Score, Pothole Proportion, and race proportions
top_5_ccvi = merged_df.sort_values('CCVI Score', ascending=False).head(5)

# Create a stacked bar chart
alt.Chart(top_5_ccvi).mark_bar().encode(
    x=alt.X('ZIP_CODE:N', title='Zip Code',
            sort=alt.SortField('CCVI Score', order='descending')),  # Sort by CCVI Score
    y=alt.Y('CCVI Score:Q', title='CCVI Score'),
    color=alt.Color(
        'Race:N',
        title='Race',
        scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race']),
        legend=alt.Legend(orient='bottom')
    )
).transform_fold(
    ['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
    as_=['Race', 'Proportion']
).properties(
    title='Top 5 Zip Codes with Highest CCVI Scores & Pothole Proportion by Race'
)

# Assuming 'merged_df' is your DataFrame with CCVI Score and race proportions
top_5_ccvi = merged_df.sort_values('CCVI Score', ascending=False).head(5)

# Bar chart for the CCVI Score
ccvi_chart = alt.Chart(top_5_ccvi).mark_bar(color='lightgray').encode(
    x=alt.X('ZIP_CODE:N', title='Zip Code',
            sort=alt.SortField('CCVI Score', order='descending')),
    y=alt.Y('CCVI Score:Q', title='CCVI Score')
)

# Stacked bar chart for the race proportions
race_proportion_chart = alt.Chart(top_5_ccvi).mark_bar().encode(
    x=alt.X('ZIP_CODE:N', title='Zip Code',
            sort=alt.SortField('CCVI Score', order='descending')),
    y=alt.Y('Proportion:Q', title='Race Proportion', axis=alt.Axis(grid=False)),
    color=alt.Color(
        'Race:N',
        title='Race',
        scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race']),
        legend=alt.Legend(orient='bottom')
    )
).transform_fold(
    ['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
    as_=['Race', 'Proportion']
)

# Combine the two charts by layering them
layered_chart = alt.layer(
    ccvi_chart,
    race_proportion_chart
).resolve_scale(
    y='independent'  # Allow the two charts to have independent y-axes
).properties(
    title='Top 5 Zip Codes with Highest CCVI Scores & Race Proportions'
)

layered_chart

top_5_ccvi

import altair as alt

# Assuming 'top_5_ccvi' is your DataFrame with CCVI Score and race proportions
# Create a base chart for the ZIP codes
base = alt.Chart(top_5_ccvi).encode(
    x=alt.X('ZIP_CODE:N', title='Zip Code', sort=alt.SortField('CCVI Score', order='descending'))
)

# Create a bar chart for CCVI scores
ccvi_bars = base.mark_bar(color='steelblue').encode(
    y=alt.Y('CCVI Score:Q', title='CCVI Score')
)

# Create a bar chart for race proportions (stacked)
race_bars = base.mark_bar().encode(
    y=alt.Y('Proportion:Q', title='Proportion of Race'),
    color=alt.Color(
        'Race:N',
        title='Race',
        scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
                        range=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
    )
).transform_fold(
    ['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
    as_=['Race', 'Proportion']
)

# Combine the charts with a layer
chart = alt.layer(ccvi_bars, race_bars).properties(
    title='Top 5 Zip Codes with Highest CCVI Scores and Race Proportions'
).resolve_scale(
    y='independent'  # Makes the y-axes independent
)

chart

import altair as alt

# Assuming 'top_5_ccvi' is your DataFrame with CCVI Score and race proportions
# Create a base chart for the ZIP codes
base = alt.Chart(top_5_ccvi).encode(
    x=alt.X('ZIP_CODE:N', title='Zip Code', sort=alt.SortField('CCVI Score', order='descending'))
)

# Create a bar chart for CCVI scores
ccvi_bars = base.mark_bar(color='steelblue').encode(
    y=alt.Y('CCVI Score:Q', title='CCVI Score')
)

# Create a bar chart for race proportions (stacked)
race_bars = base.mark_bar().encode(
    y=alt.Y('Proportion:Q', title='Proportion of Race'),
    color=alt.Color(
        'Race:N',
        title='Race',
        scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'])
    )
).transform_fold(
    ['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
    as_=['Race', 'Proportion']
)

# Combine the charts with a layer
chart = alt.layer(ccvi_bars, race_bars).properties(
    title='Top 5 Zip Codes with Highest CCVI Scores and Race Proportions'
).resolve_scale(
    y='independent'  # Makes the y-axes independent
)

chart

import altair as alt

# Assuming 'top_5_ccvi' is your DataFrame with CCVI Score and race proportions
# Create a base chart for the ZIP codes
base = alt.Chart(top_5_ccvi).encode(
    y=alt.Y('ZIP_CODE:N', title='Zip Code', sort=alt.SortField('CCVI Score', order='descending'))  # Flipped to y-axis
)

# Create a bar chart for CCVI scores
ccvi_bars = base.mark_bar(color='steelblue').encode(
    x=alt.X('CCVI Score:Q', title='CCVI Score')  # Flipped to x-axis
)

# Create a bar chart for race proportions (stacked)
race_bars = base.mark_bar().encode(
    x=alt.X('Proportion:Q', title='Proportion of Race'),  # Flipped to x-axis
    color=alt.Color(
        'Race:N',
        title='Race',
        scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'])
    )
).transform_fold(
    ['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
    as_=['Race', 'Proportion']
)

# Combine the charts with a layer
chart = alt.layer(ccvi_bars, race_bars).properties(
    title='Top 5 Zip Codes with Highest CCVI Scores and Race Proportions'
).resolve_scale(
    x='independent'  # Makes the x-axes independent
)

chart

import altair as alt

# Create a base chart for the ZIP codes
base = alt.Chart(top_5_ccvi).encode(
    y=alt.Y('ZIP_CODE:N', title='Zip Code', sort=alt.SortField('CCVI Score', order='descending'))
)

# Create a bar chart for CCVI scores
ccvi_bars = base.mark_bar(color='steelblue').encode(
    x=alt.X('CCVI Score:Q', title='CCVI Score')
)

# Create a bar chart for race proportions (stacked)
race_bars = base.mark_bar().encode(
    x=alt.X('Proportion:Q', title='Proportion of Race'),
    color=alt.Color(
        'Race:N',
        title='Race',
        scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'])
    )
).transform_fold(
    ['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
    as_=['Race', 'Proportion']
)

# Combine the charts with a layer
chart = alt.layer(ccvi_bars, race_bars).properties(
    title='Top 5 Zip Codes with Highest CCVI Scores and Race Proportions'
).resolve_scale(
    x='independent'  # Makes the x-axes independent
)

chart

# Assuming 'top_5_ccvi' is your DataFrame with CCVI Score and race proportions
# Create a base chart for the ZIP codes
base = alt.Chart(top_5_ccvi).encode(
    y=alt.Y('ZIP_CODE:N', title='Zip Code', sort=alt.SortField('CCVI Score', order='descending'))
)

# Create a bar chart for CCVI scores
ccvi_bars = base.mark_bar(color='steelblue').encode(
    x=alt.X('CCVI Score:Q', title='CCVI Score')
)

# Create a bar chart for race proportions (stacked)
race_bars = base.mark_bar().encode(
    x=alt.X('Proportion:Q', title='Proportion of Race'),
    color=alt.Color(
        'Race:N',
        title='Race',
        scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
                        range=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
    )
).transform_fold(
    ['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
    as_=['Race', 'Proportion']
)

# Combine the charts with a layer
chart = alt.layer(ccvi_bars, race_bars).properties(
    title='Top 5 Zip Codes with Highest CCVI Scores and Race Proportions'
).resolve_scale(
    x='independent'  # Makes the x-axes independent
)

chart

import altair as alt
import pandas as pd

# Assuming 'top_5_ccvi' contains the data for the top 5 ZIP codes and their racial proportions
# Prepare the data for the treemap
treemap_data = top_5_ccvi.melt(id_vars='ZIP_CODE',
                                 value_vars=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
                                 var_name='Race',
                                 value_name='Proportion')

# Create the treemap
treemap = alt.Chart(treemap_data).mark_rect().encode(
    x=alt.X('sum(Proportion):Q', stack='zero', title='Proportion'),
    y=alt.Y('ZIP_CODE:N', title='Zip Code'),
    color=alt.Color('Race:N', title='Race', scale=alt.Scale(domain=['Percent Latine', 'Percent Asian', 'Percent Black', 'Percent White', 'Percent Other Race'],
                                                              range=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])),
    tooltip=['ZIP_CODE:N', 'Race:N', 'Proportion:Q']
).properties(
    title='Racial Demographics Treemap for Top 5 Zip Codes by CCVI Scores',
    width=600,
    height=400
).transform_calculate(
    area='datum.Proportion'  # Use the proportion for sizing
).transform_window(
    sort_order='rank()',  # Sort rectangles based on proportions
    frame=[None, None],
    sort=[alt.SortField('area', order='descending')]
)

treemap