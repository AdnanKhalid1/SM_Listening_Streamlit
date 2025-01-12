import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

def create_summation_heatmap(df):
    """
    Create a heatmap with summation of 'thumbsUpCount_222'.
    """
    # Create pivot table of sums
    pivot_data = df.groupby(['App', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(
        index='App',
        columns='kmeans_cluster_name',
        values='thumbsUpCount_222'
    ).fillna(0)

    # Create the heatmap using Plotly Express
    fig = px.imshow(
        pivot_table,
        labels=dict(x="", y="", color=""),  # Hide axis and color titles
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale="OrRd",  # Highlights higher values with deeper reds
        text_auto=True,                 # Display summation values on cells
        aspect="auto"                   # Maintains the aspect ratio automatically
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
        width=3200,   
        height=900,   
        margin=dict(l=60, r=60, t=80, b=50),
        xaxis_title=None,       
        yaxis_title=None,       
        coloraxis_showscale=False
    )

    # Increase the font size of the text labels on each cell
    fig.update_traces(
        hovertemplate=(
            "<b>App:</b> %{y}<br>"
            "<b>kmeans_cluster_name:</b> %{x}<br>"
            "<b>Sum thumbsUpCount_222:</b> %{z}"
        ),
        textfont_size=12  # Increase cell text (summation) size
    )

    return fig


def create_percentage_heatmap(df):
    """
    Create a heatmap with row-wise percentages of 'thumbsUpCount_222'.
    Each row sums to 100%.
    """
    # Create pivot table of sums (same as summation approach)
    pivot_data = df.groupby(['App', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(
        index='App',
        columns='kmeans_cluster_name',
        values='thumbsUpCount_222'
    ).fillna(0)

    # Convert each row to percentage of that row's sum
    row_sums = pivot_table.sum(axis=1)  # Sum across columns for each row
    percentage_table = pivot_table.div(row_sums, axis=0) * 100  # Convert to row-wise percentage

    # Create heatmap for percentages
    fig = px.imshow(
        percentage_table,
        labels=dict(x="", y="", color=""),  # Hide axis and color titles
        x=percentage_table.columns,
        y=percentage_table.index,
        color_continuous_scale="OrRd",  # Same color scale, or pick another
        text_auto=True,                # Display the percentage values
        aspect="auto"
    )

    fig.update_xaxes(
        tickangle=45,
        tickfont=dict(size=14)
    )
    fig.update_yaxes(
        tickfont=dict(size=14)
    )

    fig.update_layout(
        autosize=False,
        width=3200,
        height=900,
        margin=dict(l=60, r=60, t=80, b=50),
        xaxis_title=None,
        yaxis_title=None,
        coloraxis_showscale=False  # Hide the color scale bar
    )

    # Adjust the hover and displayed text to show percentages with 1-2 decimals
    fig.update_traces(
        hovertemplate=(
            "<b>App:</b> %{y}<br>"
            "<b>kmeans_cluster_name:</b> %{x}<br>"
            "<b>% of thumbsUpCount_222 in row:</b> %{z:.2f}%"
        ),
        texttemplate="%{z:.1f}",  # show one decimal place in the cell text
        textfont_size=12
    )

    return fig


def main():
    st.set_page_config(
        page_title="Heatmap Dashboard",
        layout="wide",  # Use the full screen width
    )
    st.markdown("### Heatmap of Summation of Thumbs Up Counts")

    # ----------------------------------------------------------------
    # 1. LOAD THE DATA
    # ----------------------------------------------------------------
    df_shortlisted = pd.read_pickle('df_shortlisted.pkl')

    # ----------------------------------------------------------------
    # 2. CREATE TABS
    # ----------------------------------------------------------------
    tab1, tab2 = st.tabs(["Summation Heatmaps", "Row-wise % Heatmaps"])

    with tab1:
        # ========================
        # Summation Heatmaps
        # ========================
        st.subheader("Full Data Heatmap (Summation)")
        fig_full_sum = create_summation_heatmap(df_shortlisted)
        st.plotly_chart(fig_full_sum, use_container_width=True)

        # Date range selection
        st.subheader("Filter Data by Date Range")

        min_date = df_shortlisted['at'].min().date()
        max_date = df_shortlisted['at'].max().date()

        start_date = st.date_input(
            "Select start date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
        end_date = st.date_input(
            "Select end date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

        if start_date > end_date:
            st.error("Error: Start date must be before or same as end date.")
            st.stop()

        mask = ((df_shortlisted['at'].dt.date >= start_date) &
                (df_shortlisted['at'].dt.date <= end_date))
        df_filtered = df_shortlisted.loc[mask].copy()
        st.write(f"Number of records in filtered dataset: {len(df_filtered)}")

        st.subheader(f"Filtered Data Heatmap (Summation) [{start_date} to {end_date}]")
        fig_filtered_sum = create_summation_heatmap(df_filtered)
        st.plotly_chart(fig_filtered_sum, use_container_width=True)

    with tab2:
        # ========================
        # Row-wise Percentage Heatmaps
        # ========================
        st.subheader("Full Data Heatmap (Row-wise % of Thumbs Up)")
        fig_full_pct = create_percentage_heatmap(df_shortlisted)
        st.plotly_chart(fig_full_pct, use_container_width=True)

        # Date range selection (reuse the same approach)
        st.subheader("Filter Data by Date Range")

        min_date2 = df_shortlisted['at'].min().date()
        max_date2 = df_shortlisted['at'].max().date()

        start_date2 = st.date_input(
            "Select start date",
            value=min_date2,
            min_value=min_date2,
            max_value=max_date2,
            key="start_date_tab2"  # Provide a unique key so Streamlit handles separately from tab1
        )
        end_date2 = st.date_input(
            "Select end date",
            value=max_date2,
            min_value=min_date2,
            max_value=max_date2,
            key="end_date_tab2"    # Unique key for tab2
        )

        if start_date2 > end_date2:
            st.error("Error: Start date must be before or same as end date.")
            st.stop()

        mask2 = ((df_shortlisted['at'].dt.date >= start_date2) &
                 (df_shortlisted['at'].dt.date <= end_date2))
        df_filtered2 = df_shortlisted.loc[mask2].copy()
        st.write(f"Number of records in filtered dataset: {len(df_filtered2)}")

        st.subheader(f"Filtered Data Heatmap (Row-wise %) [{start_date2} to {end_date2}]")
        fig_filtered_pct = create_percentage_heatmap(df_filtered2)
        st.plotly_chart(fig_filtered_pct, use_container_width=True)


if __name__ == "__main__":
    main()
