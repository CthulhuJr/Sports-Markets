from pathlib import Path
from importlib import import_module
from typing import Optional

import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pylance as pl



def load_data(csv_path: Optional[str] = None) -> pd.DataFrame:
    default_csv = Path(__file__).with_name("us-sports-teams-evvytools.csv")
    csv_file = Path(csv_path) if csv_path else default_csv

    if csv_file.exists():
        df = pd.read_csv(csv_file)
    else:
        sample_data = {
            "City": ["New York", "Los Angeles", "Chicago", "Houston", "Miami"],
            "Latitude": [40.7128, 34.0522, 41.8781, 29.7604, 25.7617],
            "Longitude": [-74.0060, -118.2437, -87.6298, -95.3698, -80.1918],
        }
        df = pd.DataFrame(sample_data)

    required_columns = {"City", "Latitude", "Longitude"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"CSV is missing required columns: {sorted(missing_columns)}. "
            "Expected City, Latitude, and Longitude."
        )

    return df


df = load_data()

fig = px.scatter_geo(
    df,
    lat="Latitude",
    lon="Longitude",
    text="City",
    title="Sports Market City Locations",
    projection="natural earth",
)

# Customize the appearance of the plot
edge_color = "#30011E"
background_color = "#fafafa"

# Load and prepare geo-data only when the optional dependency is installed.
if gpd is not None:
    counties = gpd.read_file("./data/cb_2018_us_county_500k/")
    counties = counties[~counties.STATEFP.isin(["72", "69", "60", "66", "78"])]
    counties = counties.set_index("GEOID")

    states = gpd.read_file("./data/cb_2018_us_state_500k/")
    states = states[~states.STATEFP.isin(["72", "69", "60", "66", "78"])]

    ax = counties.plot(edgecolor=edge_color + "55", color="None", figsize=(20, 20))
    states.plot(ax=ax, edgecolor=edge_color, color="None", linewidth=1)

    counties = counties.to_crs("ESRI:102003")
    states = states.to_crs("ESRI:102003")

    plt.axis("off")
    plt.show()

    def translate_geometries(df, x, y, scale, rotate):
     df.loc[:, "geometry"] = df.geometry.translate(yoff=y, xoff=x)
    center = df.dissolve().centroid.iloc[0]
    df.loc[:, "geometry"] = df.geometry.scale(xfact=scale, yfact=scale, origin=center)
    df.loc[:, "geometry"] = df.geometry.rotate(rotate, origin=center)
    return df

fig.update_layout(
    font=dict(family="serif"),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
)

fig.show()

