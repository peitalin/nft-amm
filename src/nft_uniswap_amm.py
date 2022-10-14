
import numpy as np
import pandas as pd
# plots
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D




class Uniswap:
    "This is a Uniswap AMM"

    def __init__(self,
        x=1200,
        y=400,
        tokenX="MAGIC",
        tokenY="ERC20SMOL",
        redemptionRate=100
        # erc20Toerc721ExchangeRate=100
        # 100 ERC20SMOL to redeem a single SmolBrain ERC721
    ):
        # x, y are initial balances
        self.balance_x = x
        self.balance_y = y
        self.tokenX = tokenX
        self.tokenY = tokenY
        self.lp_tokens = np.sqrt(x * y)
        self.k = x * y # invariant
        # for more on how AMMs work:
        # https://uniswap.org/docs/v2/protocol-overview/how-uniswap-works/
        self.history = dict({
            # history of prices
            'prices': [self.spot_price()], # initial price
        })
        self.redemptionRate = redemptionRate


    def __repr__(self):
        return """
        Liquidity Pool:
        {tokenX} balance:\t{balance_x:>12.4f}
        {tokenY} balance:\t{balance_y:>12.4f}
        {tokenY}/{tokenX} price: {price:.10f}
        """.format(
            tokenX = self.tokenX,
            balance_x = self.balance_x,
            tokenY = self.tokenY,
            balance_y = self.balance_y,
            price = self.spot_price(),
        )


    def spot_price(self):
        return self.balance_x / self.balance_y

    def dydx(y2, y1, x2, x1):
        """calculates derivative dy/dx"""
        # actual price paid by a trade, accounting for slippage/price impact
        return np.diff([y2, y1])[0] / np.diff([x2, x1])[0]

    #### Invariants ####
    ## work out balance of token X in a pool, given Y
    ## holding invariant constant
    def uniswap_invariant(self, a):
        b = self.k / a
        return b


    def swap(self, trade):
        """
        trade: dict({ 'type': 'x'|'y', 'amount': float })
        """
        if trade['type'] == 'x':
            # trader deposits tokenX into pool, receives some tokenY
            # determined by Uniswap invariant
            self.balance_x += trade['amount']
            new_y = self.uniswap_invariant(self.balance_x)
            y_received = self.balance_y - new_y
            self.balance_y = new_y

            price_after = self.spot_price()
            self.history['prices'].append(price_after)
            return y_received
        else:
            # trader deposits tokenY into pool, receives some tokenX
            self.balance_y += trade['amount']
            new_x = self.uniswap_invariant(self.balance_y)
            x_received = self.balance_x - new_x
            self.balance_x = new_x

            price_after = self.spot_price()
            self.history['prices'].append(price_after)
            return x_received


    def withdraw_LP(self, percentage):

        assert percentage <= 1

        x_to_remove = self.balance_x * percentage
        y_to_remove = self.balance_y * percentage

        self.balance_x -= x_to_remove
        self.balance_y -= y_to_remove

        return {
            "x_removed": x_to_remove,
            "y_removed": y_to_remove
        }







