import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.api import OLS
from statsmodels.tools.tools import add_constant
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import math
palette = itertools.cycle(sns.color_palette())


def run_lin_regression(df):
    top10 = df.value_counts(df["Country"])[0:10].index
    top10_df = df[df["Country"].isin(top10)]
    top10_df = pd.get_dummies(top10_df, columns=["Country"])

    Ys = ["Risk", "Reliability", "X"]
    X = top10_df.drop(["Risk", "Reliability", "X", "IP", "IP Type",
                       "Locale", "Longitude", "Latitude", "Country_CN"], axis=1)
    X = add_constant(X, prepend=True, has_constant='skip')
    for Y in Ys:
        model = LinearRegression()
        Y_df = top10_df[Y]
        res = OLS(Y_df, X).fit()
        df = pd.concat((res.params, res.pvalues), axis=1)
        df = df.rename(columns={0: 'Coefficients', 1: 'P-Value'}
                       )
        results_summary = res.summary()
        results_as_html = results_summary.tables[1].as_html()
        results_as_pd = pd.read_html(results_as_html, header=0, index_col=0)[0]
        results_as_pd.to_excel(f"results/{Y}_regression_results.xlsx")
        plot_reg_results(df, f"{Y}")
    print(df)


def run_prob_regression(df):
    top10 = df.value_counts(df["Country"])[0:10].index
    top10_df = df[df["Country"].isin(top10)]
    print(top10)
    top10_df.loc[((top10_df['IP Type'] == 'Scanning Host')), 'Threat'] = 0
    top10_df['Threat'] = top10_df['Threat'].fillna(1)
    Y = top10_df['Threat']
    top10_df = pd.get_dummies(top10_df, columns=["Country"],)
    X = top10_df.drop(["Threat", "Risk", "Reliability", "X", "IP", "IP Type",
                       "Locale", "Longitude", "Latitude", "Country_CN"], axis=1)
    X = add_constant(X, prepend=True, has_constant='skip')

    res = OLS(Y, X).fit()
    df = pd.concat((res.params, res.pvalues), axis=1)

    df = df.rename(columns={0: 'Coefficients', 1: 'P-Value'}
                   )
    df.to_excel(f"results/type_regression_results.xlsx")
    plot_reg_results(df, "Threat Probability")
    return df


def plot_reg_results(df, name):
    labels = range(12)
    width = 0.9
    fig, ax = plt.subplots()
    ax = sns.barplot(
        x=df.index, y=df['Coefficients'].values)
    ax.set_ylabel('Coefficient Value')

    for c in ax.containers:
        labels = [round(x, 3) for x in df['P-Value'].values]

        ax.bar_label(c, fmt='%.0f', labels=labels, label_type='center')

    ax.set_title(f'{name} Coefficient Estimates')
    for country in ax.get_xticklabels():
        country.set_rotation(45)

    plt.tight_layout()
    plt.show()
