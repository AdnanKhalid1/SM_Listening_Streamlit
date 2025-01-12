import streamlit as st
import pandas as pd
import plotly.express as px

def create_heatmap(df, title="Heatmap of Summation of thumbsUpCount_222"):
    """
    Given a DataFrame df with 'App', 'kmeans_cluster_name', and 'thumbsUpCount_222',
    this function pivots the data and creates a Plotly heatmap figure.
    """
    # Create pivot table
    pivot_data = df.groupby(['App', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(index='App',
                                   columns='kmeans_cluster_name',
                                   values='thumbsUpCount_222').fillna(0)
    
    # Create the heatmap using Plotly Express
    # 'text_auto=True' will automatically display the values on each cell
    fig = px.imshow(
        pivot_table,
        labels=dict(x="kmeans_cluster_name", y="App", color="Sum of thumbsUpCount_222"),
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale="RdBu",
        text_auto=True,
        aspect="auto",  # Let Plotly decide the best aspect ratio
        title=title
    )

    # Rotate the x-axis tick labels by 45 degrees
    fig.update_xaxes(tickangle=45)

    # Optionally tweak layout, margins, etc.
    fig.update_layout(
        margin=dict(l=60, r=60, t=80, b=50),
        xaxis_title="kmeans_cluster_name",
        yaxis_title="App",
    )

    # Improve hover template (optionally)
    fig.update_traces(
        hovertemplate="<b>App:</b> %{y}<br>"
                      + "<b>kmeans_cluster_name:</b> %{x}<br>"
                      + "<b>Sum thumbsUpCount_222:</b> %{z}"
    )

    return fig


def main():
    st.set_page_config(
        page_title="Heatmap Dashboard",
        layout="wide",  # Use the full screen width
    )
    st.title("Heatmap of Summation of Thumbs Up Counts")

    # Load your df_shortlisted dataframe here or assume it's already loaded
    # In real usage, replace the below line with your data loading code
    # Example dummy data creation (REMOVE this in your final code and use your actual df_shortlisted)
    import numpy as np
    import datetime
    
    df_shortlisted = pd.read_pickle('df_shortlisted.pkl')

    # -------------------------------------------------------------
    # 1. Full Data Heatmap
    # -------------------------------------------------------------
    st.subheader("Full Data Heatmap")
    fig_full = create_heatmap(df_shortlisted, title="Full Data Heatmap")
    st.plotly_chart(fig_full, use_container_width=True)

    # -------------------------------------------------------------
    # 2. Date Range Selection
    # -------------------------------------------------------------
    st.subheader("Filter Data by Date Range")

    min_date = df_shortlisted['at'].min().date()
    max_date = df_shortlisted['at'].max().date()

    # Create two date input widgets
    start_date = st.date_input("Select start date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("Select end date", max_date, min_value=min_date, max_value=max_date)

    if start_date > end_date:
        st.error("Error: Start date must be before or same as end date.")
        return

    # Filter the data based on user’s date selection
    mask = (df_shortlisted['at'].dt.date >= start_date) & (df_shortlisted['at'].dt.date <= end_date)
    df_filtered = df_shortlisted.loc[mask].copy()

    st.write(f"Number of records in filtered dataset: {len(df_filtered)}")

    # -------------------------------------------------------------
    # 3. Filtered Data Heatmap
    # -------------------------------------------------------------
    fig_filtered = create_heatmap(df_filtered, title=f"Filtered Data Heatmap ({start_date} to {end_date})")

    # -------------------------------------------------------------
    # 4. Switch/Toggle to Show One or Two Heatmaps
    # -------------------------------------------------------------
    st.subheader("View Mode")
    show_side_by_side = st.checkbox("Show full data heatmap and filtered data heatmap side by side?")

    if show_side_by_side:
        # Use columns to display two figures side by side
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Full Data**")
            st.plotly_chart(fig_full, use_container_width=True)
        with col2:
            st.write("**Filtered Data**")
            st.plotly_chart(fig_filtered, use_container_width=True)
    else:
        # Show only filtered data heatmap
        st.plotly_chart(fig_filtered, use_container_width=True)


if __name__ == "__main__":
    main()
