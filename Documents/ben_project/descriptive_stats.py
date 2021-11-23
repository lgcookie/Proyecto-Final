import math
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import itertools
sns.set()
palette = itertools.cycle(sns.color_palette())


def descriptive_stats(df):

    # for numeric variables
    num_df = df[["Reliability", "Risk", "X"]].apply(pd.to_numeric)
    num_df_stats = num_df.describe()
    num_df_stats.to_excel("results/num_var_stats.xlsx")
    numeric_histograms(num_df)

    # for categorical variables
    cat_df = df[["IP Type", "Country"]]

    df1 = cat_df.melt(var_name='Variable', value_name='Category')
    cat_df_stats = df1.groupby(
        ['Variable', 'Category']).size().reset_index(name='Count')
    cat_df_stats['Percentage'] = cat_df_stats['Count'].div(cat_df_stats.groupby(
        'Variable')['Count'].transform('sum')).mul(100)
    cat_df_stats.to_excel("results/cat_var_stats.xlsx")

    # categorical_histograms(cat_df)
    return num_df, cat_df


def scatter_graph(df):
    # counts how many obs from each country
    country_group = df.groupby(['Country']).mean()
    country_group = df.groupby('Country') \
        .agg({'Longitude': 'size', 'Risk': 'mean', 'Reliability': 'mean', 'X': 'mean'}) \
        .rename(columns={'Longitude': 'Count', 'Risk': 'Mean Risk', 'Reliability': 'Mean Reliability', 'X': 'Mean X'}) \
        .reset_index()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Some random colours:
    colours = range(country_group.shape[0])

    ax.scatter(country_group["Mean Risk"], country_group["Mean Reliability"],
               s=country_group["Mean X"], c=colours)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel('Mean Risk')
    ax.set_ylabel('Mean Reliability')
    ax.title.set_text(
        f'Scatter Graph of Mean Risk and Mean Reliability by Country')
    for x, y, s, country in zip(country_group["Mean Risk"], country_group["Mean Reliability"], country_group["Count"], country_group["Country"]):
        offset = random.uniform(0, 2)
        ax.text(x+offset, y, country, va='center')


def analyse_by_type(df):
    # need to group spamming and malicious together
    top5 = df.value_counts(df["Country"])[0:5].index
    # go through each type entry, assign it a new type based on if the string starts with these 4 values

    top5_df = df[df["Country"].isin(top5)]
    counts = top5_df['Country'].value_counts().to_dict()
    top5_df["Type"] = np.NaN
    # removes scanning host to focus analysis on malicious nodes
    df_bad_types = top5_df[~top5_df["IP Type"].str.contains("Scanning Host")]
    for index, row in df_bad_types.iterrows():

        if row["IP Type"].startswith("C&C"):
            df_bad_types.loc[index, ["Type"]] = "C&C"
        if row["IP Type"].startswith("Malicious"):
            df_bad_types.loc[index, ["Type"]] = "Malicious"
        if row["IP Type"].startswith("Malware"):
            df_bad_types.loc[index, ["Type"]] = "Malware"
        elif row["IP Type"].startswith("Spamming"):
            df_bad_types.loc[index, ["Type"]] = "Spamming"

    df_bad_types = df_bad_types.groupby(['Country', 'Type']).size()
    df_bad_types_unstack = df_bad_types.unstack()
    df_bad_types_unstack.plot.bar(
        title="Top 5 Countries Count of IP Type", ylabel="Count")

    # scale by occurence
    for country in counts.keys():
        df_bad_types_unstack.loc[country] = df_bad_types_unstack.loc[country]/counts[country]
    df_bad_types_unstack.plot.bar(
        title="Top 5 Countries Count of IP Type, Scaled by Country Occurance", ylabel="Proportion")

    plt.show()
    return df


def create_cont_table(df):
    df = df[["Country", "Risk", "Reliability", "X"]]
    num_vars = ["Risk", "Reliability", "X"]
    top5 = df.value_counts(df["Country"])[0:5].index
    top5_df = df[df["Country"].isin(top5)]
    country = top5_df["Country"]
    reliability = top5_df["Reliability"]
    risk = top5_df['Risk']

    tab = pd.crosstab(country, [reliability, risk], rownames=[
                      'Country'], colnames=['Reliability', 'Risk'])

    tab.plot(kind='bar', legend=False,
             title="Risk~Reliability | Country").grid(False)


def plot_histograms(df):
    # find top 5 most prevalent countries
    df = df[["Country", "Risk", "Reliability", "X"]]
    num_vars = ["Risk", "Reliability", "X"]
    top5 = df.value_counts(df["Country"])[0:5].index
    top5_df = df[df["Country"].isin(top5)]

    for column in num_vars:
        ax = plt.figure().gca()
        ax.title.set_text(f'Distribution of {column} for Top 5 Countries')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        sns.histplot(top5_df, x=column, hue="Country", multiple="stack")

    return top5


def categorical_histograms(df):
    top10 = df.value_counts(df["Country"])[0:10].index
    top10_df = df[df["Country"].isin(top10)]
    for column in top10_df.columns.values:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(top10_df[column], ax=ax)
        ax.title.set_text(f'{column} Counts')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        for c in ax.containers:
            # set the bar label
            ax.bar_label(c, fmt='%.0f', label_type='edge')


def numeric_histograms(df):

    labels = range(12)
    ax = sns.countplot(hue="variable", x="value",
                       data=pd.melt(df), dodge=True)
    # for c in ax.containers:
    #     labels = [math.trunc(v.get_height()) if v.get_height()
    #               > 3000 else '' for v in c]
    #     ax.bar_label(c, fmt='%d', labels=labels, label_type='center')

    ax.set_ylabel('Count')
    ax.set_xlabel('Value')
    ax.set_title('Stacked Chart of Reliability, Risk and X values')
    ax.legend()

    plt.show()

    return
