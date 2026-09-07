import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Exploratory Data Analysis Interface",
    layout="wide"
)

st.title("Exploratory Data Analysis Interface")

# ---------------------------------------------------------
# Sidebar: Dataset Controls
# ---------------------------------------------------------
st.sidebar.header("Dataset Controls")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File for Analysis", type=["csv"]
)

# ---------------------------------------------------------
# Helper: detect if a column is numerical or categorical
# ---------------------------------------------------------
def is_numerical(series: pd.Series, unique_threshold: int = 10) -> bool:
    """
    A column is treated as NUMERICAL only if:
      1. Its dtype is numeric, AND
      2. It has more unique values than `unique_threshold`.
    This avoids misclassifying integer-coded categorical columns
    (e.g. Pclass, Survived) as numerical.
    """
    if not pd.api.types.is_numeric_dtype(series):
        return False
    return series.nunique(dropna=True) > unique_threshold


if uploaded_file is not None:
    # Validate file: try reading it as CSV
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("The uploaded CSV file is empty. Please upload a valid dataset.")
            st.stop()
    except Exception as e:
        st.error(f"Could not read the uploaded file as a valid CSV. Error: {e}")
        st.stop()

    # -------------------------------------------------------
    # Sidebar: Attribute Selection (depends on loaded df)
    # -------------------------------------------------------
    st.sidebar.header("Attribute Selection")
    selected_column = st.sidebar.selectbox(
        "Select Attribute for Visualization", options=df.columns
    )

    # =========================================================
    # MAIN CONTENT AREA - TOP SECTION: Preview & Metadata
    # =========================================================
    st.header("Dataset Preview & Metadata")

    st.subheader("First 5 Rows:")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Shape:")
    st.write(f"{df.shape[0]} rows, {df.shape[1]} columns")

    st.subheader("Column Data Types:")
    dtypes_df = df.dtypes.astype(str).reset_index()
    dtypes_df.columns = ["Column", "Data Type"]
    st.dataframe(dtypes_df, use_container_width=True)

    st.subheader("Missing Values per Column:")
    missing_df = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing %": (df.isnull().sum() / len(df) * 100).round(2)
    })
    st.dataframe(missing_df, use_container_width=True)

    st.subheader("Basic Statistical Summary (Numerical Attributes):")
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        summary_df = numeric_df.agg(["mean", "median", "min", "max"]).T
        summary_df.columns = ["Mean", "Median", "Min", "Max"]
        st.dataframe(summary_df, use_container_width=True)
    else:
        st.info("No numerical columns found in this dataset.")

    # =========================================================
    # MAIN CONTENT AREA - BOTTOM SECTION: Visualization
    # =========================================================
    st.header("Visualization")

    col_data = df[selected_column]

    if is_numerical(col_data):
        st.subheader(f"Histogram of {selected_column}")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(col_data.dropna(), bins=20, color="skyblue", edgecolor="black")
        ax.set_title(f"Histogram of {selected_column}")
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        st.subheader(f"Bar Chart of {selected_column}")
        value_counts = col_data.value_counts(dropna=True)
        show_pct = st.checkbox("Show percentage instead of count", value=False)

        fig, ax = plt.subplots(figsize=(8, 4))
        if show_pct:
            pct_values = (value_counts / value_counts.sum() * 100)
            ax.bar(pct_values.index.astype(str), pct_values.values, color="salmon", edgecolor="black")
            ax.set_ylabel("Percentage (%)")
        else:
            ax.bar(value_counts.index.astype(str), value_counts.values, color="salmon", edgecolor="black")
            ax.set_ylabel("Frequency")

        ax.set_title(f"Bar Chart of {selected_column}")
        ax.set_xlabel(selected_column)
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

else:
    st.info("Upload a CSV file from the sidebar to begin exploratory data analysis. "
            "(Test file: Titanic-Dataset.csv)")
