import pandas as pd

DATASET = "dataset/market_prices.csv"


def load_market_data():

    try:
        df = pd.read_csv(DATASET)
        return df

    except Exception:
        return pd.DataFrame()


def search_crop(df, crop_name):

    if df.empty:
        return df

    return df[
        df["Crop"].str.contains(
            crop_name,
            case=False,
            na=False
        )
    ]


def search_market(df, market):

    if df.empty:
        return df

    return df[
        df["Market"] == market
    ]


def highest_price(df):

    if df.empty:
        return None

    return df.loc[df["Price"].idxmax()]


def lowest_price(df):

    if df.empty:
        return None

    return df.loc[df["Price"].idxmin()]


def average_price(df):

    if df.empty:
        return 0

    return round(df["Price"].mean(), 2)