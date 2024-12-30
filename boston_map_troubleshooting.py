import altair as alt
import pandas as pd

boston_git = "https://raw.githubusercontent.com/emeliaaaa/Project-2-INFO-Viz/refs/heads/main/Boston_boundaries.geojson"
geodata_boston = alt.Data(url=boston_git, format=alt.DataFormat(property="features", type="json"))


boston_land = alt.Chart(geodata_boston).mark_geoshape(
    fill = 'lightgray',
    stroke = 'white'

).encode(
    # alt.Tooltip(['properties.CRA_NAM:N'])
    # bc in the geojson, name is in the the "properties" dict. cra_nam variable, nominal
).properties(
    width = 350,
    height = 600
).project(
    type='identity'
)


boston_land


# Load the GeoJSON data
geodata_boston = alt.Data(url=boston_git, format=alt.DataFormat(property="features", type="json"))

# Create the Altair chart with a standard projection (no flipping)
chart = alt.Chart(geodata_boston).mark_geoshape().encode(
    # Add encoding if needed
).project(
    type='identity'  # 'mercator' projection without flipping
).properties(
    width=500,
    height=500
)

chart

# !pip install geopandas shapely

import geopandas as gpd
from shapely.affinity import scale

# Load the original GeoJSON file from GitHub
url = "https://raw.githubusercontent.com/emeliaaaa/Project-2-INFO-Viz/refs/heads/main/Boston_boundaries.geojson"
gdf = gpd.read_file(url)

# Flip the y-axis (latitude) by multiplying it by -1 using shapely's scale function
gdf['geometry'] = gdf['geometry'].apply(lambda geom: scale(geom, xfact=1, yfact=-1, origin=(0, 0)))

# Save the new GeoJSON file locally
gdf.to_file("Boston_boundaries_flipped.geojson", driver="GeoJSON")

print("File saved as Boston_boundaries_flipped.geojson")

import altair as alt
import json

# Load the Boston GeoJSON file
with open('Boston_boundaries_flipped.geojson') as f:
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