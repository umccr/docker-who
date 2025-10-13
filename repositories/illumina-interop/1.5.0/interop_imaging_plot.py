#!/usr/bin/env python3
from functools import reduce

# Imports
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
import re

from pathlib import Path
from typing import Union, List


"""
Usage:

interop_imaging_plot <input_csv> <output_png> <run_name>

"""


def header_regex_match(header_name) -> List[str]:
    """
    If the header name is in the format Name<item1;item2;item3>
    :param header_name: 
    :return: 
    """
    # Check if header name is in the format Name<item1;item2;item3>
    header_regex = re.compile(r'(.*)<(.*)>')
    header_match = header_regex.match(header_name)

    if not header_match:
        return [str(header_name)]

    # Return the header name and the items
    return list(
        map(
            lambda group_2_match_iter: f"{header_match.group(1)}_{group_2_match_iter}",
            header_match.group(2).split(";")
        )
    )


def read_csv(input_csv: Path) -> pd.DataFrame:
    """
    Read the input csv, and clean up the headers
    :param input_csv:
    :return:
    """
    # Read in header
    # Headers % Base<A;C;G;T> should be
    # Base_A, Base_C, Base_G, Base_T
    # What an insane way to encode a header!!
    imaging_df_headers_list = pd.read_csv(
        input_csv,
        comment='#',
        header=0
    ).columns.tolist()

    imaging_df_headers_list = list(
        reduce(
            lambda x, y: x + y,
            map(
                lambda column_name_iter: list(header_regex_match(column_name_iter)),
                imaging_df_headers_list
            )
        )
    )

    # Read in data
    imaging_df = pd.read_csv(
        input_csv,
        # Skip comments
        comment='#',
        # Assign header but we overwrite it with names
        header=0,
        # Set our own header
        names=imaging_df_headers_list
    ).drop_duplicates(
        subset=['Lane', '% Occupied', '% Pass Filter']
    ).assign(
        Lane=lambda row: row['Lane'].astype('category')
    )

    return imaging_df


def plot_data(imaging_df: pd.DataFrame, output_png: Path, run_id: str) -> None:
    """
    Use the seaborn scatterplot library to plot the data
    :param imaging_df:
    :param output_png:
    :param run_id:
    :return:
    """
    # Write data
    fig, ax = plt.subplots()

    # Set grid style
    sns.set_style('whitegrid')

    # SNS Dot plot
    sns.scatterplot(
        x='% Occupied',
        y='% Pass Filter',
        data=imaging_df,
        hue='Lane',
        ax=ax,
        alpha=0.6
    )

    # Set title
    fig.suptitle(f"Pct. Pass Filter vs. Pct. Occupied for run '{run_id}'")

    # Set x-axis label
    ax.set_xlabel('% Occupied')

    # Set x limits
    ax.set_xlim(left=0, right=100)

    # Set y limits
    ax.set_ylim(bottom=0, top=100)

    # Set legend
    ax.legend(title='Lane')

    # Pack everything up nicely
    fig.tight_layout()

    # Save plot
    fig.savefig(sys.argv[2])


def main():
    # Set io
    input_csv = sys.argv[1]
    output_png = sys.argv[2]
    run_id = sys.argv[3]

    # Read in data
    imaging_df = read_csv(Path(input_csv))

    # Plot data
    plot_data(imaging_df, Path(output_png), run_id)


if __name__ == "__main__":
    main()
