import streamlit as st
import pandas as pd
import plotly.express as px

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
    # Note: Removing the 'title' parameter to avoid duplicate subtitle.
    fig = px.imshow(
        pivot_table,
        labels=dict(x="", y="", color=""),  # Hide axis and color titles
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale="RdBu",
        text_auto=True,       # Display summation values on cells
        aspect="auto"         # Maintains the aspect ratio automatically
    )

    # Rotate the x-axis tick labels by 45 degrees
    fig.update_xaxes(tickangle=45)

    # Increase figure size (width & height) and adjust margins
    fig.update_layout(
        autosize=False,
        width=2500,    # Increase width as needed
        height=900,    # Increase height as needed
        margin=dict(l=60, r=60, t=80, b=50),
        xaxis_title=None,      # Remove the x-axis title
        yaxis_title=None,      # Remove the y-axis title
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
    # Change the main title to a smaller heading
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

    start_date = st.date_input(
        "Select start date",
        min_date,
        min_value=min_date,
        max_value=max_date
    )
    end_date = st.date_input(
        "Select end date",
        max_date,
        min_value=min_date,
        max_value=max_date
    )

    if start_date > end_date:
        st.error("Error: Start date must be before or same as end date.")
        return

    # Filter data by selected date range
    mask = (df_shortlisted['at'].dt.date >= start_date) & (df_shortlisted['at'].dt.date <= end_date)
    df_filtered = df_shortlisted.loc[mask].copy()
    st.write(f"Number of records in filtered dataset: {len(df_filtered)}")

    # ----------------------------------------------------------------
    # 4. FILTERED DATA HEATMAP
    # ----------------------------------------------------------------
    st.subheader(f"Filtered Data Heatmap ({start_date} to {end_date})")
    fig_filtered = create_heatmap(df_filtered)
    st.plotly_chart(fig_filtered, use_container_width=True)


if __name__ == "__main__":
    main()
