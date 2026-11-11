from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.express as px
import numpy as np


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

fig.show()

