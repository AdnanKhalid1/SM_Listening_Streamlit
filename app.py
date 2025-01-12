import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

def create_heatmap(df):
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
    fig = px.imshow(
        pivot_table,
        labels=dict(x="", y="", color=""),  # Hide axis and color titles
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale="OrRd",      # Highlights higher values with deeper reds
        text_auto=True,                     # Display summation values on cells
        aspect="auto"                       # Maintains the aspect ratio automatically
    )

    # Rotate x-axis labels and increase axis-label font size
    fig.update_xaxes(
        tickangle=45,
        tickfont=dict(size=14)  # Increase X-axis category label font size
    )
    fig.update_yaxes(
        tickfont=dict(size=14)  # Increase Y-axis category label font size
    )

    # Increase figure size (width & height) and adjust margins
    fig.update_layout(
        autosize=False,
        width=2900,   # Increase width as needed
        height=900,   # Increase height as needed
        margin=dict(l=60, r=60, t=80, b=50),
        xaxis_title=None,       # Remove the x-axis title
        yaxis_title=None,       # Remove the y-axis title
        coloraxis_showscale=False
    )

    # Increase the font size of the text labels on each cell
    fig.update_traces(
        hovertemplate="<b>App:</b> %{y}<br>"
                      + "<b>kmeans_cluster_name:</b> %{x}<br>"
                      + "<b>Sum thumbsUpCount_222:</b> %{z}",
        textfont_size=12       # Increase cell text (summation) size
    )

    return fig

def main():
    st.set_page_config(
        page_title="Heatmap Dashboard",
        layout="wide",  # Use the full screen width
    )
    # Smaller heading for main title
    st.markdown("### Heatmap of Summation of Thumbs Up Counts")

    # ----------------------------------------------------------------
    # 1. LOAD THE DATA
    # ----------------------------------------------------------------
    df_shortlisted = pd.read_pickle('df_shortlisted.pkl')

    # ----------------------------------------------------------------
    # 2. FULL DATA HEATMAP
    # ----------------------------------------------------------------
    st.subheader("Full Data Heatmap")
    fig_full = create_heatmap(df_shortlisted)
    st.plotly_chart(fig_full, use_container_width=True)

    # ----------------------------------------------------------------
    # 3. DATE RANGE SELECTION
    # ----------------------------------------------------------------
    st.subheader("Filter Data by Date Range")
    min_date = df_shortlisted['at'].min().date()
    max_date = df_shortlisted['at'].max().date()

    # Default to current year's Jan 1 and today's date
    today = datetime.date.today()
    start_of_year = datetime.date(today.year, 1, 1)

    # If your data is older or doesn’t extend to current date, adjust accordingly
    default_start = max(start_of_year, min_date)  # later of (start_of_year, min_date)
    default_end = min(today, max_date)            # earlier of (today, max_date)

    start_date = st.date_input(
        "Select start date",
        value=default_start,
        min_value=min_date,
        max_value=max_date
    )
    end_date = st.date_input(
        "Select end date",
        value=default_end,
        min_value=min_date,
        max_value=max_date
    )

    # Show an error if invalid, but do not stop execution
    if start_date > end_date:
        st.error("Error: Start date must be before or same as end date.")

    # ----------------------------------------------------------------
    # 4. FILTERED DATA HEATMAP
    # ----------------------------------------------------------------
    mask = (df_shortlisted['at'].dt.date >= start_date) & (df_shortlisted['at'].dt.date <= end_date)
    df_filtered = df_shortlisted.loc[mask].copy()

    st.write(f"Number of records in filtered dataset: {len(df_filtered)}")

    st.subheader(f"Filtered Data Heatmap ({start_date} to {end_date})")
    fig_filtered = create_heatmap(df_filtered)
    st.plotly_chart(fig_filtered, use_container_width=True)

if __name__ == "__main__":
    main()
