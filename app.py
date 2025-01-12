import streamlit as st
import pandas as pd
import plotly.express as px

def create_heatmap(df, title=None):
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
        labels=dict(x="kmeans_cluster_name", y="App", color=None),  # No legend text for color scale
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale="RdBu",
        text_auto=True,
        aspect="auto"
    )

    # Rotate the x-axis tick labels
    fig.update_xaxes(title_text="", tickangle=45, showticklabels=True)  # Hide x-axis title
    fig.update_yaxes(title_text="", showticklabels=True)               # Hide y-axis title

    # Customize layout
    fig.update_layout(
        autosize=False,
        width=2500,    # Increase width
        height=900,    # Increase height
        margin=dict(l=60, r=60, t=80, b=50),
        title_font_size=16,  # Reduce heatmap title font size
        coloraxis_showscale=False  # Hide color scale
    )

    # Customize heatmap text font size
    fig.update_traces(
        hovertemplate="<b>App:</b> %{y}<br>"
                      + "<b>kmeans_cluster_name:</b> %{x}<br>"
                      + "<b>Sum thumbsUpCount_222:</b> %{z}",
        textfont_size=20  # Increase font size of heatmap numbers
    )

    return fig


def main():
    st.set_page_config(
        page_title="Heatmap Dashboard",
        layout="wide",
    )
    st.header("Heatmap of Summation of Thumbs Up Counts")  # Reduced font size for main title

    # ----------------------------------------------------------------
    # 1. LOAD THE DATA
    # ----------------------------------------------------------------
    # In real usage, load your actual DataFrame
    df_shortlisted = pd.read_pickle('df_shortlisted.pkl')

    # ----------------------------------------------------------------
    # 2. FULL DATA HEATMAP
    # ----------------------------------------------------------------
    st.subheader("Full Data Heatmap")
    fig_full = create_heatmap(df_shortlisted, title=None)  # Removed larger subtitle
    st.plotly_chart(fig_full, use_container_width=True)

    # ----------------------------------------------------------------
    # 3. DATE RANGE SELECTION
    # ----------------------------------------------------------------
    st.subheader("Filter Data by Date Range")
    min_date = df_shortlisted['at'].min().date()
    max_date = df_shortlisted['at'].max().date()

    # Create date input widgets
    start_date = st.date_input("Select start date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("Select end date", max_date, min_value=min_date, max_value=max_date)

    if start_date > end_date:
        st.error("Error: Start date must be before or same as end date.")
        return

    # Filter the data based on user’s date selection
    mask = (df_shortlisted['at'].dt.date >= start_date) & (df_shortlisted['at'].dt.date <= end_date)
    df_filtered = df_shortlisted.loc[mask].copy()

    st.write(f"Number of records in filtered dataset: {len(df_filtered)}")

    # ----------------------------------------------------------------
    # 4. FILTERED DATA HEATMAP
    # ----------------------------------------------------------------
    st.subheader(f"Filtered Data Heatmap ({start_date} to {end_date})")
    fig_filtered = create_heatmap(df_filtered, title=None)  # Removed larger subtitle
    st.plotly_chart(fig_filtered, use_container_width=True)


if __name__ == "__main__":
    main()
