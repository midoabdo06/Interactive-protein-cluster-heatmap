import streamlit as st
import pandas as pd
import plotly.express as px

# ─────────────────────────────────────────────
# Title and Description
# ─────────────────────────────────────────────
st.set_page_config(layout="wide")
st.title("Interactive Heatmap Viewer")
st.markdown("""
This app allows you to interactively visualize protein expression (Z-score heatmap).
Use the sidebar to select clusters and proteins of interest.
""")

# ─────────────────────────────────────────────
# Load the data
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("M.xlsx", index_col=0)
    return df

df = load_data()

# Ensure data is numeric (drop non-numeric if needed)
df = df.apply(pd.to_numeric, errors='coerce')
df = df.dropna(how='all', axis=1)  # Drop all-NaN columns
df = df.dropna(how='all', axis=0)  # Drop all-NaN rows

# ─────────────────────────────────────────────
# Sidebar for Selection
# ─────────────────────────────────────────────
st.sidebar.header("Select Options")

available_clusters = df.columns.tolist()
available_proteins = df.index.tolist()

selected_clusters = st.sidebar.multiselect("Choose clusters", available_clusters, default=available_clusters)
selected_proteins = st.sidebar.multiselect("Choose proteins", available_proteins, default=available_proteins)

# ─────────────────────────────────────────────
# Display Heatmap
# ─────────────────────────────────────────────
if selected_clusters and selected_proteins:
    filtered_df = df.loc[selected_proteins, selected_clusters]

    st.subheader("Z-Score Heatmap")
    fig = px.imshow(
        filtered_df,
        color_continuous_scale="RdBu_r",
        labels=dict(x="Cluster", y="Protein", color="Z-score"),
        aspect="auto",
        height=800
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one cluster and one protein to display the heatmap.")

# ─────────────────────────────────────────────
# Optional: Show raw data
# ─────────────────────────────────────────────
with st.expander("Show raw Z-score data"):
    st.dataframe(df.style.background_gradient(cmap='coolwarm', axis=1))
