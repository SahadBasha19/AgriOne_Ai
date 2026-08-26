import os

import pandas as pd
import streamlit as st

from utils.helper import page_header, footer


# ============================================================
# SETTINGS
# ============================================================

POSSIBLE_FILES = [
    "dataset/market.csv",
    "dataset/market_prices.csv",
    "dataset/mandi_prices.csv",
    "dataset/market_data.csv",
]


# ============================================================
# FIND DATASET
# ============================================================

def find_market_file():
    """
    Find the first available market CSV.
    """

    for file_path in POSSIBLE_FILES:

        if os.path.exists(file_path):

            return file_path

    return None


# ============================================================
# LOAD MARKET DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_market_data(file_path):
    """
    Load market CSV safely.
    """

    if not file_path:

        return (
            pd.DataFrame(),
            "Market dataset was not found.",
        )

    try:

        df = pd.read_csv(
            file_path
        )

        df = df.dropna(
            how="all"
        )

        df = df.loc[
            :,
            df.notna().any()
        ]

        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        return (
            df,
            None,
        )

    except Exception as error:

        return (
            pd.DataFrame(),
            f"Unable to read market dataset: {error}",
        )


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column(
    columns,
    possible_names,
):
    """
    Find a column using exact and partial matching.
    """

    normalized = {
        str(column).strip().lower(): column
        for column in columns
    }

    # Exact match
    for name in possible_names:

        key = name.lower()

        if key in normalized:

            return normalized[key]

    # Partial match
    for column in columns:

        column_name = (
            str(column)
            .strip()
            .lower()
        )

        for name in possible_names:

            if name.lower() in column_name:

                return column

    return None


# ============================================================
# SAFE TEXT
# ============================================================

def safe_text(
    value,
    default="N/A",
):
    """

    Convert values into readable text.
    """

    if pd.isna(value):

        return default

    value = str(
        value
    ).strip()

    if not value:

        return default

    return value


# ============================================================
# PRICE TO NUMBER
# ============================================================

def price_to_number(value):
    """
    Convert common price strings into numbers.

    Examples:
        ₹2,500 -> 2500
        2500/kg -> 2500
    """

    if pd.isna(value):

        return None

    if isinstance(
        value,
        (int, float),
    ):

        return float(value)

    text = str(
        value
    )

    text = (
        text.replace(
            "₹",
            "",
        )
        .replace(
            ",",
            "",
        )
        .strip()
    )

    # Keep digits and decimal point
    cleaned = ""

    for character in text:

        if (
            character.isdigit()
            or character == "."
        ):

            cleaned += character

    try:

        return float(
            cleaned
        )

    except ValueError:

        return None


# ============================================================
# PAGE
# ============================================================

def app():

    page_header(
        "💰 Market Prices"
    )

    st.write(
        "Check commodity and Mandi prices from your "
        "market dataset."
    )

    st.info(
        "Market prices can change frequently. "
        "Verify the latest price with the relevant "
        "Mandi or official market source before making "
        "selling decisions."
    )

    st.divider()

    # --------------------------------------------------------
    # Dataset
    # --------------------------------------------------------

    market_file = find_market_file()

    if not market_file:

        st.error(
            "Market dataset not found."
        )

        st.write(
            "Place your market CSV in the dataset folder."
        )

        st.code(
            """
dataset/
├── market.csv
or
├── market_prices.csv
or
├── mandi_prices.csv
or
└── market_data.csv
""",
            language="text",
        )

        footer()

        return

    df, error = load_market_data(
        market_file
    )

    if error:

        st.error(
            error
        )

        footer()

        return

    if df.empty:

        st.warning(
            "The market dataset is empty."
        )

        footer()

        return

    # --------------------------------------------------------
    # Detect Columns
    # --------------------------------------------------------

    crop_column = find_column(
        df.columns,
        [
            "crop",
            "commodity",
            "commodity name",
            "crop name",
            "product",
            "item",
        ],
    )

    market_column = find_column(
        df.columns,
        [
            "market",
            "mandi",
            "market name",
            "mandi name",
            "marketplace",
        ],
    )

    state_column = find_column(
        df.columns,
        [
            "state",
            "state name",
        ],
    )

    district_column = find_column(
        df.columns,
        [
            "district",
            "district name",
        ],
    )

    price_column = find_column(
        df.columns,
        [
            "modal price",
            "modal_price",
            "price",
            "market price",
            "average price",
            "avg price",
            "modal",
        ],
    )

    min_price_column = find_column(
        df.columns,
        [
            "min price",
            "minimum price",
            "min_price",
        ],
    )

    max_price_column = find_column(
        df.columns,
        [
            "max price",
            "maximum price",
            "max_price",
        ],
    )

    date_column = find_column(
        df.columns,
        [
            "date",
            "arrival date",
            "price date",
            "market date",
        ],
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    st.subheader(
        "📊 Market Overview"
    )

    metric1, metric2 = st.columns(
        2
    )

    with metric1:

        st.metric(
            "Total Records",
            len(df),
        )

    with metric2:

        if crop_column:

            unique_crops = (
                df[crop_column]
                .dropna()
                .astype(str)
                .nunique()
            )

        else:

            unique_crops = 0

        st.metric(
            "Commodities",
            unique_crops,
        )

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    st.subheader(
        "🔎 Search Market Prices"
    )

    filter_col1, filter_col2 = st.columns(
        2
    )

    with filter_col1:

        search_text = st.text_input(
            "Search commodity",
            placeholder="Example: Rice",
            key="market_search",
        )

    with filter_col2:

        if state_column:

            states = (
                df[state_column]
                .dropna()
                .astype(str)
                .str.strip()
            )

            states = sorted(
                [
                    state
                    for state in states.unique()
                    if state
                ]
            )

            selected_state = st.selectbox(
                "Select State",
                [
                    "All",
                    *states,
                ],
                key="market_state",
            )

        else:

            selected_state = "All"

    # --------------------------------------------------------
    # Apply Filters
    # --------------------------------------------------------

    filtered_df = df.copy()

    if (
        search_text
        and crop_column
    ):

        search_text = (
            search_text
            .strip()
            .lower()
        )

        filtered_df = filtered_df[
            filtered_df[
                crop_column
            ]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False,
                regex=False,
            )
        ]

    if (
        selected_state != "All"
        and state_column
    ):

        filtered_df = filtered_df[
            filtered_df[
                state_column
            ]
            .astype(str)
            .str.strip()
            == selected_state
        ]

    # --------------------------------------------------------
    # District Filter
    # --------------------------------------------------------

    if district_column:

        districts = (
            filtered_df[
                district_column
            ]
            .dropna()
            .astype(str)
            .str.strip()
        )

        districts = sorted(
            [
                district
                for district in districts.unique()
                if district
            ]
        )

        if districts:

            selected_district = st.selectbox(
                "Select District",
                [
                    "All",
                    *districts,
                ],
                key="market_district",
            )

            if (
                selected_district
                != "All"
            ):

                filtered_df = filtered_df[
                    filtered_df[
                        district_column
                    ]
                    .astype(str)
                    .str.strip()
                    == selected_district
                ]

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    st.write(
        f"Showing **{len(filtered_df)}** market record(s)."
    )

    if filtered_df.empty:

        st.warning(
            "No market records matched your filters."
        )

        footer()

        return

    # --------------------------------------------------------
    # Price Cards
    # --------------------------------------------------------

    if price_column:

        st.subheader(
            "💵 Current Market Records"
        )

        display_df = filtered_df.head(
            20
        )

        for _, row in display_df.iterrows():

            crop_name = (
                safe_text(
                    row[crop_column],
                    "Commodity",
                )
                if crop_column
                else "Commodity"
            )

            market_name = (
                safe_text(
                    row[market_column],
                    "Market not available",
                )
                if market_column
                else "Market not available"
            )

            state_name = (
                safe_text(
                    row[state_column],
                    "",
                )
                if state_column
                else ""
            )

            price_value = price_to_number(
                row[price_column]
            )

            if price_value is not None:

                price_text = (
                    f"₹{price_value:,.2f}"
                )

            else:

                price_text = safe_text(
                    row[price_column]
                )

            with st.container(
                border=True
            ):

                card_col1, card_col2 = st.columns(
                    [2, 1]
                )

                with card_col1:

                    st.markdown(
                        f"### 🌾 {crop_name}"
                    )

                    st.write(
                        f"📍 **Market:** {market_name}"
                    )

                    if state_name:

                        st.write(
                            f"🗺 **State:** {state_name}"
                        )

                    if date_column:

                        st.caption(
                            f"📅 {safe_text(row[date_column])}"
                        )

                with card_col2:

                    st.metric(
                        "Market Price",
                        price_text,
                    )

                    if (
                        min_price_column
                        and max_price_column
                    ):

                        min_price = price_to_number(
                            row[min_price_column]
                        )

                        max_price = price_to_number(
                            row[max_price_column]
                        )

                        if (
                            min_price is not None
                            and max_price is not None
                        ):

                            st.caption(
                                f"Range: ₹{min_price:,.2f} – "
                                f"₹{max_price:,.2f}"
                            )

    # --------------------------------------------------------
    # Full Data
    # --------------------------------------------------------

    st.divider()

    with st.expander(
        "📋 View Full Market Data"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    csv_data = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Market Data",
        data=csv_data,
        file_name="AgriOne_AI_Market_Prices.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # Important Note
    # --------------------------------------------------------

    st.markdown("---")

    st.warning(
        "⚠️ Market prices may change throughout the day. "
        "Use the displayed dataset as reference information "
        "and verify the latest local market price before selling."
    )

    footer()