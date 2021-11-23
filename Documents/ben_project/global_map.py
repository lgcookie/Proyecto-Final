from geopandas import GeoDataFrame
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt


def create_global_map(df):
    # initialize an axis
    fig, ax = plt.subplots(figsize=(16, 6))

    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = GeoDataFrame(df, geometry=geometry)

    # this is a simple map that goes with geopandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world[(world.pop_est > 0) & (world.name != "Antarctica")].plot(
        color="lightgrey", edgecolor='black', ax=ax)

    # plot confirmed cases world map
    gdf.plot(ax=ax, column='X', c="X Score",
             legend=True, cmap='coolwarm')
    plt.title('Heat Map', fontsize=12)
    ax.legend()
    ax.set_axis_off()
    ax.grid(b=True, alpha=0.5)
    # plt.tight_layout()

    # plt.show()

    return
