import pandas as pd
from preprocess_data import preprocess_data
from global_map import create_global_map
from descriptive_stats import descriptive_stats, scatter_graph, plot_histograms, create_cont_table, analyse_by_type
from regression import run_lin_regression, run_prob_regression
import matplotlib.pyplot as plt

# reading from the file
df = preprocess_data('data/reputation.data')
num_df, cat_df = descriptive_stats(df)

# create_global_map(df)

# create_cont_table(df)
# scatter_graph(df)
# plot_histograms(df)

# run_lin_regression(df)
# run_prob_regression(df)
analyse_by_type(cat_df)
plt.tight_layout()
plt.show()
