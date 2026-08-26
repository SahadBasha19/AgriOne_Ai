import os

import pandas as pd
import streamlit as st

from config import SCHEME_FILE
from utils.helper import page_header, footer


# ============================================================
# LOAD SCHEMES
# ============================================================

@st.cache_data(show_spinner=False)
def load_schemes():
    """
    Load the schemes dataset once.

    Returns:
        DataFrame, error_message
    """

    if not os.path.exists(SCHEME_FILE):

        return (
            pd.DataFrame(),
            f"Scheme dataset not found: {SCHEME_FILE}",
        )

    try:

        df = pd.read_csv(
            SCHEME_FILE
        )

        # Remove completely empty rows/columns
        df = df.dropna(
            how="all"
        )

        df = df.loc[
            :,
            df.notna().any()
        ]

        # Clean column names
        df.columns = [
            str(column)
            .strip()
            for column in df.columns
        ]

        return (
            df,
            None,
        )

    except Exception as error:

        return (
            pd.DataFrame(),
            f"Could not read scheme dataset: {error}",
        )


# ============================================================
# COLUMN HELPERS
# ============================================================

def find_column(
    columns,
    possible_names,
):
    """
    Find a column using common naming variations.
    """

    normalized = {
        str(column).strip().lower(): column
        for column in columns
    }

    # Exact match
    for name in possible_names:

        if name.lower() in normalized:

            return normalized[
                name.lower()
            ]

    # Partial match
    for column in columns:

        column_lower = (
            str(column)
            .strip()
            .lower()
        )

        for name in possible_names:

            if name.lower() in column_lower:

                return column

    return None


# ============================================================
# SAFE TEXT
# ============================================================

def safe_text(
    value,
    default="Not available",
):
    """
    Convert dataset values to readable text.
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
# SEARCH
# ============================================================

def search_schemes(
    df,
    search_text,
):
    """
    Search across all columns.
    """

    if not search_text:

        return df

    search_text = (
        search_text
        .strip()
        .lower()
    )

    if not search_text:

        return df

    mask = pd.Series(
        False,
        index=df.index,
    )

    for column in df.columns:

        mask = mask | (
            df[column]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False,
                regex=False,
            )
        )

    return df.loc[
        mask
    ]


# ============================================================
# SCHEME CARD
# ============================================================

def display_scheme(
    row,
    column_map,
):
    """
    Display one scheme from the CSV.
    """

    name_column = column_map.get(
        "name"
    )

    description_column = column_map.get(
        "description"
    )

    eligibility_column = column_map.get(
        "eligibility"
    )

    benefit_column = column_map.get(
        "benefit"
    )

    state_column = column_map.get(
        "state"
    )

    link_column = column_map.get(
        "link"
    )

    name = (
        safe_text(
            row[name_column],
            "Government Scheme",
        )
        if name_column
        else "Government Scheme"
    )

    description = (
        safe_text(
            row[description_column]
        )
        if description_column
        else ""
    )

    eligibility = (
        safe_text(
            row[eligibility_column]
        )
        if eligibility_column
        else ""
    )

    benefit = (
        safe_text(
            row[benefit_column]
        )
        if benefit_column
        else ""
    )

    state = (
        safe_text(
            row[state_column]
        )
        if state_column
        else ""
    )

    link = (
        safe_text(
            row[link_column],
            "",
        )
        if link_column
        else ""
    )

    st.markdown(
        f"### 🏛 {name}"
    )

    if state and state != "Not available":

        st.caption(
            f"📍 {state}"
        )

    if description:

        st.write(
            description
        )

    if eligibility:

        st.markdown(
            f"**👨‍🌾 Eligibility:** {eligibility}"
        )

    if benefit:

        st.markdown(
            f"**💰 Benefit:** {benefit}"
        )

    # Only render an actual URL as a clickable link.
    if (
        link
        and link.startswith(
            (
                "http://",
                "https://",
            )
        )
    ):

        st.link_button(
            "🔗 Visit Official Website",
            link,
        )

    st.divider()


# ============================================================
# PAGE
# ============================================================

def app():

    page_header(
        "🏛 Government Schemes"
    )

    st.write(
        "Explore agricultural government schemes "
        "available in your dataset."
    )

    st.info(
        "Scheme information is loaded from the project's "
        "schemes.csv dataset. Always verify eligibility, "
        "deadlines and current requirements on the official "
        "government portal before applying."
    )

    st.divider()

    # --------------------------------------------------------
    # Load Dataset
    # --------------------------------------------------------

    df, error = load_schemes()

    if error:

        st.error(
            error
        )

        st.code(
            SCHEME_FILE,
            language="text",
        )

        st.info(
            "Make sure schemes.csv exists inside the "
            "dataset folder."
        )

        footer()

        return

    if df.empty:

        st.warning(
            "The scheme dataset is empty."
        )

        footer()

        return

    # --------------------------------------------------------
    # Detect Columns
    # --------------------------------------------------------

    column_map = {

        "name": find_column(
            df.columns,
            [
                "name",
                "scheme",
                "scheme name",
                "scheme_name",
                "title",
            ],
        ),

        "description": find_column(
            df.columns,
            [
                "description",
                "details",
                "about",
                "scheme description",
            ],
        ),

        "eligibility": find_column(
            df.columns,
            [
                "eligibility",
                "eligible",
                "eligibility criteria",
            ],
        ),

        "benefit": find_column(
            df.columns,
            [
                "benefit",
                "benefits",
                "amount",
                "financial benefit",
                "assistance",
            ],
        ),

        "state": find_column(
            df.columns,
            [
                "state",
                "states",
                "location",
                "region",
            ],
        ),

        "link": find_column(
            df.columns,
            [
                "link",
                "url",
                "website",
                "official website",
                "official link",
            ],
        ),
    }

    # --------------------------------------------------------
    # Dataset Summary
    # --------------------------------------------------------

    st.subheader(
        "📊 Available Schemes"
    )

    metric1, metric2 = st.columns(
        2
    )

    with metric1:

        st.metric(
            "Total Schemes",
            len(df),
        )

    with metric2:

        st.metric(
            "Dataset Columns",
            len(df.columns),
        )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    st.subheader(
        "🔎 Search Schemes"
    )

    search_text = st.text_input(
        "Search by scheme, state, eligibility, benefit...",
        placeholder="Example: farmer, crop, Andhra Pradesh",
        key="scheme_search",
    )

    filtered_df = search_schemes(
        df,
        search_text,
    )

    # --------------------------------------------------------
    # State Filter
    # --------------------------------------------------------

    if column_map["state"]:

        states = (
            df[
                column_map["state"]
            ]
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

        if states:

            selected_state = st.selectbox(
                "📍 Filter by State / Region",
                [
                    "All",
                    *states,
                ],
                key="scheme_state",
            )

            if selected_state != "All":

                filtered_df = filtered_df[
                    filtered_df[
                        column_map["state"]
                    ]
                    .astype(str)
                    .str.strip()
                    == selected_state
                ]

    # --------------------------------------------------------
    # Results Count
    # --------------------------------------------------------

    st.write(
        f"Showing **{len(filtered_df)}** scheme(s)."
    )

    if filtered_df.empty:

        st.warning(
            "No schemes matched your search."
        )

        footer()

        return

    # --------------------------------------------------------
    # Display Results
    # --------------------------------------------------------

    for _, row in filtered_df.iterrows():

        display_scheme(
            row,
            column_map,
        )

    # --------------------------------------------------------
    # Dataset Preview
    # --------------------------------------------------------

    with st.expander(
        "📋 View Scheme Dataset"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # Download Filtered Data
    # --------------------------------------------------------

    csv_data = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Scheme Data",
        data=csv_data,
        file_name="AgriOne_AI_Schemes.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    st.markdown("---")

    st.success(
        "🌾 Stay informed about government support "
        "available to farmers."
    )

    footer()