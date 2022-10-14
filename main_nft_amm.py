import numpy as np
import pandas as pd
# plots
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from src.nft_uniswap_amm import Uniswap
from src.helpers import generate_trade, create_time_series_data_store





if __name__=="__main__":
    print("NFT-AMM Uniswap Simulations!")


# Create data structures to hold simulation time series data
data_stores = create_time_series_data_store()
avg_prices = data_stores['avg_prices']
colors = data_stores['colors']



# initial price: $1
# lp_initial_magic = 1_000_000
# lp_initial_erc20smols  = 100_000
lp_initial_magic = 400
lp_initial_erc20smols  = 1200
k= 400*1200

## Random trade params
mu = 0
sigma = 1
nobs = 5000

alpha_opacity = 0.1
num_iterations = 20




########## START PLOTS ############
fig, ax = plt.subplots()

for i in range(num_iterations):

    print('Iteration: ', i)
    u = Uniswap(lp_initial_magic, lp_initial_erc20smols)
    trades = [generate_trade(mu, sigma, u) for x in range(nobs)]
    _ = [u.swap(x) for x in trades]

    ax.plot(
        np.linspace(0, nobs, nobs+1),
        u.history['prices'],
        color=colors[0],
        alpha=alpha_opacity,
    )

    if i == 0:
        avg_prices = u.history['prices']
    else:
        # accumulate prices, divide by num_iterations after
        avg_prices = np.add(
            avg_prices,
            u.history['prices']
        )

    if i == (num_iterations - 1):
        # last loop, average over all iterations
        avg_prices = np.divide(
            avg_prices,
            num_iterations
        )
        # Then plot mean price line with alpha=1
        ax.plot(
            np.linspace(0,nobs,nobs+1),
            avg_prices,
            color=colors[0],
            alpha=1,
            linewidth=2,
            linestyle="dotted",
        )



if __name__=="__main__":

    plt.title("Simulating slippage and rounding on NFT-AMM")
    plt.xlabel("#Trades")
    plt.ylabel("Price: ERC20SMOL/MAGIC")
    # place a text box in upper left in axes coords
    ax.text(
        6000, .15,
        r'''
        {runs} runs of {nobs} trades sampled from a
        $X \sim N(\mu=${mu},$\sigma$={sigma}) distribution.

        Initial price: 0.1 ERC20SMOL/MAGIC
        Initial LP: 1,000,000 MAGIC / 10,000,000 ERC20SMOL
        '''.format(runs=4*num_iterations, nobs=nobs, mu=mu, sigma=sigma),
        {'color': 'black', 'fontsize': 8},
        verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.5)
    )


    legend_elements = [
        Line2D([0], [0], color=colors[0], lw=2,
            label=r'$(1-price)^2 \times {sold}$ '),
    ]
    ax.legend(handles=legend_elements, loc='upper left')


    plt.show()



