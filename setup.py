import setuptools

setuptools.setup(
    name="nft-amm",
    version="0.1",
    author="Peita Lin",
    author_email="pta@treasure.lol",
    description="NFT AMM slippage simulations",
    packages=[
        "curve_amm",
        "uniswap_amm",
    ],
    install_requires=[
        "ipython",
        "numpy",
        "pandas",
        "matplotlib",
    ],
)
