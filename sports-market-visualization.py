from pathlib import Path
from importlib import import_module
from typing import Optional

import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import sports_market_styles as styles

def load_data(csv_path: Optional[str] = None) -> pd.DataFrame:
    default_csv = Path(__file__).with_name("us-sports-teams-evvytools.csv")
    csv_file = Path(csv_path) if csv_path else default_csv

    if csv_file.exists():
        df = pd.read_csv(csv_file)
    else:
        sample_data = {
            "team_name": ["Team A", "Team B", "Team C", "Team D", "Team E"],
            "league": ["NFL", "NBA", "NHL", "MLB", "NFC"],
            "conference": ["AFC", "NFC", "Eastern", "Western", "Central"],
            "division": ["Division 1", "Division 2", "Division 3", "Division 4", "Division 5"],
            "city": ["New York", "Los Angeles", "Chicago", "Houston", "Miami"],
            "state": ["NY", "CA", "IL", "TX", "FL"],
            "latitude": [40.7128, 34.0522, 41.8781, 29.7604, 25.7617],
            "longitude": [-74.0060, -118.2437, -87.6298, -95.3698, -80.1918],
            "venue": ["Stadium A", "Stadium B", "Stadium C", "Stadium D", "Stadium E"],
            "founded": [1990, 1985, 1995, 1980, 2000]
        }
        df = pd.DataFrame(sample_data)

    required_columns = {
        "team_name",
        "league",
        "conference",
        "division",
        "city",
        "state",
        "latitude",
        "longitude",
        "venue",
        "founded",
    }
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"CSV is missing required columns: {sorted(missing_columns)}. "
            f"Expected columns: {sorted(required_columns)}."
        )

    return df

df = load_data()

fig = px.scatter_geo(
    df,
    lat="latitude",
    lon="longitude",
    color="league",
    hover_name="team_name",
    hover_data={
        "conference": True,
        "division": True,
        "city": True,
        "state": True,
        "venue": True,
        "founded": True,
        "latitude": False,
        "longitude": False,
    },
    projection="natural earth",
    scope="north america",
)

fig = styles.apply_plotly_style(fig)

fig.show()

