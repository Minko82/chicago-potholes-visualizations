import altair as alt
import pandas as pd

# Load Chicago geojson spatial data

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

# Chicago Community Vulnerability Index Data
# https://drive.google.com/file/d/1cVe4eGdQxnwrdEjB7QW6l0DZASZDXpZU/view?usp=sharing

ccvi = pd.read_csv("https://drive.google.com/uc?id=1cVe4eGdQxnwrdEjB7QW6l0DZASZDXpZU")
ccvi.head()

#Change the column name 'Community Area or ZIP Code' to 'zip' so we can merge the GeoJSON and CSV

ccvi = ccvi.rename(columns={'Community Area or ZIP Code' : 'zip'})
ccvi.head()

choropleth = alt.Chart(geodata_chicago).mark_geoshape(
    stroke = 'white'
).transform_lookup(
    lookup='properties.zip',
    from_=alt.LookupData(data=ccvi, key='zip', fields=['CCVI Score', 'CCVI Category'])
).encode(
    alt.Color('CCVI Score:Q', scale=alt.Scale(scheme='viridis', reverse=True), legend=alt.Legend(title="Community Vulnerability Index", orient="bottom")),
    alt.Tooltip(['properties.zip:N', 'CCVI Score:Q', 'CCVI Category:N'])
).properties(
    width=400,
    height=600
).project(
    type='mercator'
)

choropleth

# Chicago Pothole Complaint Data
# https://drive.google.com/file/d/1r-6Cg7drGM_q3hAeqAJDTP7OMqXxj-gK/view?usp=sharing

potholes = pd.read_csv("https://drive.google.com/uc?id=1r-6Cg7drGM_q3hAeqAJDTP7OMqXxj-gK")
potholes.head()

# Filter for pothole complaints created in 2024
potholes['CREATED_DATE'] = pd.to_datetime(potholes['CREATED_DATE'], format='%m/%d/%Y %I:%M:%S %p')
potholes2024 = potholes[potholes['CREATED_DATE'].dt.year == 2024]

# Delete rows with NaN in 'ZIP_CODE' and 'STATUS' columns
potholes2024 = potholes2024.dropna(subset=['ZIP_CODE', 'STATUS'])

# Delete rows with "Canceled" in 'STATUS' column
potholes2024 = potholes2024[potholes2024['STATUS'] != 'Canceled']

# Create a new dataframe with only the columns we'll be using
potholes2024_filtered = potholes2024[['ZIP_CODE', 'STATUS','LATITUDE','LONGITUDE']].copy()
potholes2024_filtered['ZIP_CODE'] = potholes2024_filtered['ZIP_CODE'].apply(lambda x: str(int(x)))

# Rename 'ZIP_CODE' column to 'zip' to merge with GeoJSON
potholes2024_filtered = potholes2024_filtered.rename(columns={'ZIP_CODE': 'zip'})

potholes2024_filtered.head()

# Group by ZIP_CODE and count Completed and Open complaints, without lat/lon
pothole_counts = potholes2024_filtered.groupby('zip').agg(
    Completed=('STATUS', lambda x: (x == 'Completed').sum()),  # Count Completed complaints
    Open=('STATUS', lambda x: (x == 'Open').sum())  # Count Open complaints
).reset_index()

pothole_counts.head()

# For the points, keep lat/lon and complaint status counts
pothole_counts_points = potholes2024_filtered.groupby('zip').agg(
    LATITUDE=('LATITUDE', 'mean'),  # Mean latitude for each ZIP_CODE
    LONGITUDE=('LONGITUDE', 'mean'),  # Mean longitude for each ZIP_CODE
    Completed=('STATUS', lambda x: (x == 'Completed').sum()),  # Count Completed complaints
    Open=('STATUS', lambda x: (x == 'Open').sum())  # Count Open complaints
).reset_index()

# Now we have the points data for plotting

# Plot the Completed complaints as orange points
points_completed = alt.Chart(pothole_counts_points).mark_circle(opacity=0.7).encode(
    alt.Latitude('LATITUDE:Q'),
    alt.Longitude('LONGITUDE:Q'),
    alt.Size('Completed:Q', scale=alt.Scale(range=[10, 100]), legend=alt.Legend(title='Completed Complaints', orient="left")),
    alt.Color(value='blue'),  # High-contrast orange color for Completed complaints
    alt.Tooltip(['zip:N', 'Completed:Q', 'Open:Q'])
).properties(
    width=400,
    height=600
)

# Offset the Open complaints' longitude slightly and plot them as teal points
points_open = alt.Chart(pothole_counts_points).mark_circle(opacity=0.7).encode(
    alt.Latitude('LATITUDE:Q'),
    alt.Longitude('LONGITUDE:Q'),  # Slight longitude offset to separate points
    alt.Size('Open:Q', scale=alt.Scale(range=[10, 100]), legend=alt.Legend(title='Open Complaints', orient="right")),
    alt.Color(value='red'),  # High-contrast teal color for Open complaints
    alt.Tooltip(['zip:N', 'Completed:Q', 'Open:Q'])
).properties(
    width=400,
    height=600
)

completed_with_legend = choropleth + points_completed
open_with_legend = choropleth + points_open

final_chart = alt.hconcat(
    completed_with_legend,
    open_with_legend
).resolve_scale(
    size='shared'  # Shared scale for size encoding to compare open vs closed complaints
)

final_chart









pothole2ksamp = potholes2024.sample(1000)

pothole2ksamp

# Create a scatter plot of pothole locations
pothole_plot = alt.Chart(pothole2ksamp).mark_circle().encode(
    longitude='LONGITUDE:Q',
    latitude='LATITUDE:Q',
    color=alt.condition(alt.datum.STATUS == 'Completed',
                       alt.value('green'),
                       alt.value('red')),
    tooltip=['STATUS', 'CREATED_DATE', 'ZIP_CODE']
).properties(
    width=350,
    height=600
).project(
    type='mercator'
)

# Layer the pothole plot on top of the chloropleth
layered_chart = choropleth + pothole_plot

# Display the layered chart
layered_chart