import altair as alt
import json

import json

# Load the GeoJSON file
with open('Boston_boundaries.geojson') as f:
    geojson = json.load(f)

# Check the structure of the file
print(geojson.keys())  # Should contain 'type', 'features', etc.

# Check how many features are present
print(len(geojson['features']))

# Inspect a sample feature
print(geojson['features'][0])

"""## This is graphed upside down. Still keeping it though because it graphed it still."""

import altair as alt
import json

# Load the Boston GeoJSON file
with open('Boston_boundaries.geojson') as f:
    geojson = json.load(f)

# Create a basic map without tooltips to test rendering
boston_land = alt.Chart(alt.Data(values=geojson['features'])).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    type='identity'  # Use 'identity' projection to match lat/lon data
).properties(
    width=600,
    height=400
)

# Display the map
boston_land

"""## Had to invert the coordinates because up here ^ is wrong. I'm not sure if it is how it was loaded but...

"""

import json
import altair as alt

# Load the Boston GeoJSON file
with open('Boston_boundaries.geojson') as f:
    geojson = json.load(f)

# Invert the y-coordinates of the GeoJSON features
def invert_coordinates(coords):
    return [[lon, -lat] for lon, lat in coords]

for feature in geojson['features']:
    if feature['geometry']['type'] == 'Polygon':
        feature['geometry']['coordinates'] = [invert_coordinates(coord_set) for coord_set in feature['geometry']['coordinates']]
    elif feature['geometry']['type'] == 'MultiPolygon':
        feature['geometry']['coordinates'] = [[invert_coordinates(coord_set) for coord_set in polygon] for polygon in feature['geometry']['coordinates']]

# Create the map using the modified GeoJSON
boston_land = alt.Chart(alt.Data(values=geojson['features'])).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    type='identity'  # Use 'identity' projection to match lat/lon data
).properties(
    width=600,
    height=400
)

# Display the map
boston_land

# adding tooltips
boston_land = boston_land.encode(
    alt.Tooltip('properties.neighborhood:N')
)

boston_land


import pandas as pd

# Assuming the CSV file is in the same directory as your notebook
# Replace 'Boston_CPA_Projects_and_Demographics.csv' with the actual file name
boston_cpa_df = pd.read_csv('Boston_CPA_Projects_and_Demographics.csv')

# Print some info to check if it loaded correctly
boston_cpa_df.head()

# pip install geopandas

import geopandas as gpd

# Load the GeoJSON file
geojson_path = "Boston_boundaries.geojson"
gdf = gpd.read_file(geojson_path)

merged = gdf.merge(boston_cpa_df, how="left", left_on="neighborhood", right_on="Name")
merged.head()

import json

# Flatten the GeoJSON features by moving properties to the top-level
for feature in geojson_features:
    feature.update(feature['properties'])  # Move 'properties' to the top level
    del feature['properties']  # Remove the original 'properties' field

# Create a choropleth map of BIPOC percentages with proper handling of missing values
boston_land1 = alt.Chart(alt.Data(values=geojson_features)).mark_geoshape(
    stroke='white'
).encode(
    color=alt.condition(
        alt.datum.percent_bipoc != None,  # Check if percent_bipoc is not NaN
        alt.Color('percent_bipoc:Q', scale=alt.Scale(scheme='blues')),  # Color by BIPOC percentage
        alt.value('lightgray')  # Set missing values to lightgray
    ),
    tooltip=['neighborhood:N', 'percent_bipoc:Q']  # Add tooltips for neighborhood and BIPOC %
).project(
    type='identity'  # Use 'identity' projection to match lat/lon data
).properties(
    width=600,
    height=400,
    title='BIPOC Percentage by Boston Neighborhood'
)

# Display the map
boston_land1

# Check the first few rows of the merged GeoDataFrame
print(merged[['neighborhood', 'percent_bipoc']].head(10))

# Check for missing values
print(merged['percent_bipoc'].isna().sum())  # Count of NaN values

for feature in geojson['features']:
    neighborhood_name = feature['properties']['neighborhood']
    # Find matching row in the CSV
    matching_row = boston_cpa_df[boston_cpa_df['Name'] == neighborhood_name]

    if not matching_row.empty:
        # Add the CSV data to the GeoJSON feature's properties
        feature['properties'].update(matching_row.iloc[0].to_dict())

# Now create the map using the merged GeoJSON data
boston_land1 = alt.Chart(alt.Data(values=geojson['features'])).mark_geoshape(
    fill='lightgray',
    stroke='white'
).encode(
    alt.Tooltip(['properties.name:N', 'properties.COUNT_:Q', 'properties.SUM_awarded_num:Q'])
).properties(
    width=350,
    height=600
).project(
    type='mercator'  # Using Mercator projection for better city mapping
)

# Display the map
boston_land1

# Print out the properties of the first feature to inspect the merge
print(geojson['features'][0]['properties'])

for feature in geojson['features'][:5]:  # Check the first 5 features
    print(feature['properties'])