from geopandas import GeoDataFrame
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import matplotlib.pyplot as plt
import pycountry
from IPython.display import HTML

plt.style.use('ggplot')


def getlatlong(x):
    return pd.Series([float(x.split(',')[0]),
                      float(x.split(',')[1])],
                     index=["Latitude", "Longitude"])


def preprocess_data(filepath):
    df = pd.read_csv(filepath, sep="#",
                     names=["IP", "Reliability", "Risk", "Type", "Country", "Locale", "Coords", "X"])
    df = pd.concat((df, df.Coords.apply(getlatlong)), axis=1)

    # Counting non numeric values and replacing them by 0
    mask = pd.to_numeric(df['X'], errors='coerce').isna()
    print(f"non-numeric X values {mask.sum()}")
    df["IP Type"] = df["Type"]
    df['X'] = pd.to_numeric(df.X, errors='coerce').fillna(0).astype(int)
    df = df.drop(["Coords", "Type"], axis=1)

    return df
