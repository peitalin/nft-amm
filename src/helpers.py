import numpy as np


def generate_trade(mu, sigma, u):
    rv = np.random.normal(mu, sigma)
    if rv >= 0:
        amount = u.spot_price() * np.abs(rv)
        return dict({ 'type': "x", 'amount': amount })
    else:
        # amount = 1 / u.spot_price() * np.abs(rv)
        amount = np.abs(rv)
        return dict({ 'type': "y", 'amount': amount })


def create_time_series_data_store():
    """ stores timeseries data for simulations """
    avg_prices = []
    colors = ["dodgerblue"]

    return dict({
        'avg_prices': avg_prices,
        'colors': colors,
    })


def quadratic_tax(price, usd_amount):
    # tax is only in-effet under the peg
    if price > 1:
        return 0

    tax = (1 - price)**2 * np.abs(usd_amount)
    assert tax <= usd_amount
    return tax

def logistic_tax(price, usd_amount):
    return 1/(1 + np.exp((price-0.5)*10)) * np.abs(usd_amount)



