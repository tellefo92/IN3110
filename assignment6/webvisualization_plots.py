from datetime import datetime, date
from functools import lru_cache
import altair as alt
import pandas as pd
import os
from os.path import exists
import urllib.request
from tqdm import tqdm


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_csv():
    """
    Function that will download the latest version of the covid data and remove previous versions
    """
    today = date.today()
    today = today.strftime("%Y%m%d")
    filename = "covid-data/owid-covid-data-" + today + ".csv"
    data_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    # Check if we have the most recent covid data
    if not exists(filename):
        dir = 'covid-data'
        # Create directory /covid-data/ if it doesn't exist
        if not os.path.isdir(dir):
            os.mkdir(dir)
        else:
            # Delete previous covid data in /covid-data/ directory
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
        # Download most recent covid data from OWID github and showing progress bar
        with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=data_url.split('/')[-1]) as t:
            urllib.request.urlretrieve(data_url, filename, reporthook=t.update_to)
            




@lru_cache()
def get_data_from_csv(countries=None, start=None, end=None, return_countries=False, get_highest=False):
    """Creates pandas dataframe from .csv file.
    Data will be filtered based on data column name, list of countries to be plotted and
    time frame chosen.
    Args:
        columns (list(string)): a list of data columns you want to include
        countries ((list(string), optional): List of countries you want to include.
        If none is passed, dataframe should be filtered for the 6 countries with the highest
        number of cases per million at the last current date available in the timeframe chosen.
        start (string, optional): The first date to include in the returned dataframe.
            If specified, records earlier than this will be excluded.
            Default: include earliest date
            Example format: "2021-10-10"
        end (string, optional): The latest date to include in the returned data frame.
            If specified, records later than this will be excluded.
            Example format: "2021-10-10"
    Returns:
        cases_df (dataframe): returns dataframe for the timeframe, columns, and countries chosen
    """
    # add path to .csv file from 6.0
    today = date.today()
    today = today.strftime("%Y%m%d")
    path = "covid-data/owid-covid-data-" + today + ".csv"

    # read .csv file, define which columns to read
    df = pd.read_csv(
        path,
        sep=",",
        usecols=["location"] + ["date"] + ["new_cases_per_million"],
        parse_dates=["date"],
        date_parser=lambda col: pd.to_datetime(col, format="%Y-%m-%d"),
    )

    if return_countries:
        return df['location'].unique()

    df['cumsum'] = df.groupby('location')['new_cases_per_million'].transform(pd.Series.cumsum)

    if countries is None:
        # no countries specified, pick 6 countries with the highest case count at end_date
        if end is None:
            # no end date specified, pick latest date available
            end_date = df.date.iloc[-1]
        else:
            end_date = datetime.strptime(end, "%Y-%m-%d")
            if end_date > df.date.iloc[-1]:
                end_date = df.date.iloc[-1]
            
        df_latest_dates = df[df['date'] == end_date].sort_values(by=["new_cases_per_million"], ascending=False)


        # identify the 6 countries with the highest case count
        # on the last included day
        countries = df_latest_dates['location'].head(6).to_list()

        # Return list of 6 countries if get_highest is set to true
        if get_highest:
            return countries
    # now filter to include only the selected countries
    cases_df = df[df['location'].isin(countries)]

    # apply date filters
    if start is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        # exclude records earlier than start_date
        cases_df = cases_df[cases_df['date'] > start_date]

    if end is not None:
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if start_date is not None and start_date >= end_date:
            raise ValueError("The start date must be earlier than the end date.")

        # exclude records later than end date
        cases_df = cases_df[cases_df['date'] <= end_date]
    return cases_df

def get_countries():
    """
    Gets country names from data frame
    """
    return get_data_from_csv(return_countries=True)

@lru_cache()
def get_highest_countries(date=None):
    """
    Gets the 6 countries with highest infection rate per million
    """ 
    return get_data_from_csv(end=date, get_highest=True)

@lru_cache()
def plot_reported_cases_per_million(countries=None, start=None, end=None, typeofCases="daily"):
    """Plots data of reported covid-19 cases per million using altair.
    Calls the function get_data_from_csv to receive a dataframe used for plotting.
    Args:
        countries ((list(string), optional): List of countries you want to filter.
        If none is passed, dataframe will be filtered for the 6 countries with the highest
        number of cases per million at the last current date available in the timeframe chosen.
        start (string, optional): a string of the start date of the table, none
        of the dates will be older then this on
        end (string, optional): a string of the en date of the table, none of
        the dates will be newer then this one
    Returns:
        altair Chart of number of reported covid-19 cases over time.
    """
    if typeofCases == "daily":
        stats = "new_cases_per_million"
        stat_title = "New cases"
        x_title = "Daily new cases per million"
        y_title = "Number of Reported Cases per Million"
    elif typeofCases == "cumulative":
        stats = "cumsum"
        stat_title = "Cumulative cases per million"
        x_title = stat_title
        y_title = stat_title
    else:
        raise TypeError ("Case type must be either daily or cumulative")
    # create dataframe
    cases_df = get_data_from_csv(countries=countries, start=start, end=end)

    # Note: when you want to plot all countries simultaneously while enabling checkboxes, you might need to disable altairs max row limit by commenting in the following line
    # alt.data_transformers.disable_max_rows()
    
    chart = (
        alt.Chart(cases_df, title=x_title)
        .mark_line()
        .encode(
            x=alt.X(
                "date:T",
                axis=alt.Axis(
                    format="%b, %Y", title="Date", titleFontSize=14, tickCount=20
                ),
            ),
            y=alt.Y(
                stats,
                axis=alt.Axis(
                    title=y_title,
                    titleFontSize=14,
                    tickCount=10,
                ),
            ),
            color=alt.Color("location:N", legend=alt.Legend(title="Country")),
            tooltip=[
                alt.Tooltip("location", title="Country"),
                alt.Tooltip("date", title="Date"),
                alt.Tooltip(stats, title=stat_title, format=".0f")
                ]
        )
        .interactive()
    )
    return chart


def main():
    """Function called when run as a script
    Creates a chart and display it or save it to a file
    """
    download_csv()
    countries = None
    start = None
    end = None
    chart = plot_reported_cases_per_million(countries=countries, start=start, end=end)
    # chart.show requires altair_viewer
    # or you could save to a file instead
    chart.show()


if __name__ == "__main__":
    main()