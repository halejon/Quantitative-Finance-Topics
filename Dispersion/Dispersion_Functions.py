import numpy as np
import pandas as pd
import datetime


def weighted_average_return(component_returns, weights):
    """
    Calculates and returns single-period portfolio dispersion

    :param component_returns: a list or series of portfolio component returns for a single time period
    :param weights: a list or series of portfolio weights at the start of the time period
    :return:" returns the weighted average portfolio return
    """
    return sum([x * y for x, y in zip(component_returns, weights)])


###function for Single Period Dispersion for a portfolio
def dispersion_calc(component_returns, weights, portfolio_return=None):
    """
    Calculates and returns single-period portfolio dispersion

    :param component_returns: a list or series of portfolio component returns for a single time period
    :param weights: a list or series of portfolio weights at the start of the time period
    :param portfolio_return: default to None and calculated by the function. Can provide a user specified override
    :return: returns dispersion of portfolio component returns relative to the portfolio return
    """
    if portfolio_return == None:
        portfolio_return = weighted_average_return(component_returns, weights)

    return (sum([y * ((x - portfolio_return) ** 2) for x, y in zip(component_returns, weights)])) ** (0.5)


### function to clean take prices dataframe to a clean returns dataframe
### last step to zero out any remaining NaNs if (for data where there is no price avail)

def price_df_to_returns(price_df):
    """
    returns a dataframe with a start and end date and the percentage change in stock price for each period

    :param price_df: a dataframe with a Date Index and columns containing the stock prices for a portfolio of stocks
    :return: returns a dataframe Date Index = starting date, end date and the percentage change in stock price for each stock
                in the portfolio
    """

    # converts the input dataframe of prices into one of returns
    returns = price_df.pct_change()

    # pulls out the ending date for the time periods we are looking at returns over
    end = returns.index[1:]

    # Adds in the column of ending dates, shifts the returns data up one row and reindex the columns
    returns = returns.shift(-1).iloc[:-1]
    returns['End'] = end
    returns = returns.reindex(columns=(list(returns.columns)[-1:] + list(returns.columns)[:-1]))

    return returns


def apply_returns(starting_values, current_returns):
    """
    returns a list of ending values for a given list of starting values and a list of returns corresponding to those
    starting values over a single time interval

    :param starting_values: a list of starting values for a portfolio of investments
    :param current_returns: a list of returns for each investment in a portfolio of investments
    returns should be of the format 1.xx for an xx% return (e.g. 5% increase represented as 1.05, -5% decrease
    represnted as 0.95)
    :return:returns a list of ending values for
    """

    return [x * y for x, y in zip(starting_values, current_returns)]


def portfolio_weights(portfolio_values):
    """
    returns a list of ending values for a given set of starting values and a set of returns corresponding to those
    starting values over a time interval

    :param portfolio_values: a list of values for a portfolio of investments
    :return:returns a list of weights for each investment in a portfolio of investments
    """
    return [x / sum(portfolio_values) for x in portfolio_values]


def return_portfolio_values(starting_values, returns):
    """
    returns a dataframe of ending values for a given set of starting values and a dataframe of returns corresponding to those
    starting values over a multiple time intervals

    :param starting_values: a list of starting values for a portfolio of investments
    :param returns: a dataframe of returns for each investment in a portfolio of investments
    :return:returns a dataframe of portfolio values for each investment
    """
    # headers for our output dataframe
    cols = returns.keys()

    # initialze a dataframe with starting portfolio values
    starting_values.append(returns.index[0])
    starting_values = [starting_values[-1]] + starting_values[:-1]
    values_df = pd.DataFrame(columns=cols)
    new_data = {x: y for x, y in zip(cols, starting_values)}
    values_df = values_df.append(new_data, ignore_index=True)

    # calculate subsequent portfolio values and append them to the dataframe
    x = starting_values[1:]

    for index, row in returns.iterrows():
        ending_values = apply_returns(x, list(row[1:] + 1))

        x = ending_values

        values_to_add = [row[0]] + ending_values
        new_data = {x: y for x, y in zip(cols, values_to_add)}
        values_df = values_df.append(new_data, ignore_index=True)

    return values_df


def calculate_return(start_date, end_date, price_df):
    """
    returns an array of returns given a start date and end date contained in a dataframe of prices with datetime index

    :param start_date: a starting datetime
    :param end_date: an ending datetime
    :param price_df: a dataframe of stock prices indexed with a datetime index
    :return:returns a dataframe returns between the start and end date for each stock
    """
    return [(x / y) - 1 for x, y in
            zip(price_df[price_df.index == end_date].values, price_df[price_df.index == start_date].values)]