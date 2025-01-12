import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

def create_summation_heatmap(df):
    """
    Create a heatmap with summation of 'thumbsUpCount_222'.
    Each cell shows the total thumbsUpCount_222 for that App x kmeans_cluster_name.
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
    # Create pivot table of sums
    pivot_data = df.groupby(['App', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(
        index='App',
        columns='kmeans_cluster_name',
        values='thumbsUpCount_222'
    ).fillna(0)

    # Convert each row to percentage of that row's sum
    row_sums = pivot_table.sum(axis=1)
    percentage_table = pivot_table.div(row_sums, axis=0) * 100  # row-wise %

    # Create heatmap for percentages
    fig = px.imshow(
        percentage_table,
        labels=dict(x="", y="", color=""),
        x=percentage_table.columns,
        y=percentage_table.index,
        color_continuous_scale="OrRd",
        text_auto=True,
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
        coloraxis_showscale=False
    )

    # Show percentages with 1 decimal in cells, 2 decimals on hover
    fig.update_traces(
        hovertemplate=(
            "<b>App:</b> %{y}<br>"
            "<b>kmeans_cluster_name:</b> %{x}<br>"
            "<b>% of thumbsUpCount_222 in row:</b> %{z:.2f}%"
        ),
        texttemplate="%{z:.1f}",
        textfont_size=12
    )

    return fig


def main():
    st.set_page_config(page_title="Heatmap Dashboard", layout="wide")
    st.markdown("### Heatmap of Summation of Thumbs Up Counts")

    # ----------------------------------------------------------------
    # LOAD THE DATA
    # ----------------------------------------------------------------
    df_shortlisted = pd.read_pickle('df_shortlisted.pkl')

    # ----------------------------------------------------------------
    # GLOBAL DATE FILTER (applies to bottom plots in all tabs)
    # ----------------------------------------------------------------
    st.write("#### Global Date Filter for Bottom Plots (All Tabs)")
    min_date = df_shortlisted['at'].min().date()
    max_date = df_shortlisted['at'].max().date()

    start_date = st.date_input(
        "Start Date (for bottom plots)",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key="global_start_date"
    )
    end_date = st.date_input(
        "End Date (for bottom plots)",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        key="global_end_date"
    )

    if start_date > end_date:
        st.error("Error: Start date must be before or same as end date.")
        # Instead of st.stop(), just skip creating bottom plots
        # return or pass
        pass

    # Create a filtered DataFrame for the BOTTOM plots in each tab
    mask_global = (df_shortlisted['at'].dt.date >= start_date) & \
                  (df_shortlisted['at'].dt.date <= end_date)
    df_bottom_filtered = df_shortlisted.loc[mask_global].copy()

    # ----------------------------------------------------------------
    # CREATE TABS
    # ----------------------------------------------------------------
    tab1, tab2, tab3 = st.tabs([
        "Tab 1: Summation Heatmaps",
        "Tab 2: Row-wise % Heatmaps",
        "Tab 3: Row-wise % with App/Cluster Filter"
    ])

    # ===========================
    # TAB 1: SUMMATION HEATMAPS
    # ===========================
    with tab1:
        st.subheader("Top Plot (Summation) - Full Data (No Date Filter)")
        # Top Plot: Full data, summation
        fig_full_sum = create_summation_heatmap(df_shortlisted)
        st.plotly_chart(fig_full_sum, use_container_width=True, key="summation_top_tab1")

        st.subheader(f"Bottom Plot (Summation) - Date Filtered [{start_date} to {end_date}]")
        fig_filtered_sum = create_summation_heatmap(df_bottom_filtered)
        st.plotly_chart(fig_filtered_sum, use_container_width=True, key="summation_bottom_tab1")

    # ===========================
    # TAB 2: ROW-WISE % HEATMAPS
    # ===========================
    with tab2:
        st.subheader("Top Plot (Row-wise %) - Full Data (No Date Filter)")
        fig_full_pct = create_percentage_heatmap(df_shortlisted)
        st.plotly_chart(fig_full_pct, use_container_width=True, key="percentage_top_tab2")

        st.subheader(f"Bottom Plot (Row-wise %) - Date Filtered [{start_date} to {end_date}]")
        fig_filtered_pct = create_percentage_heatmap(df_bottom_filtered)
        st.plotly_chart(fig_filtered_pct, use_container_width=True, key="percentage_bottom_tab2")

    # ================================================
    # TAB 3: ROW-WISE % + APP & CLUSTER FILTERS
    # ================================================
    with tab3:
        st.subheader("Row-wise % Heatmaps with Additional Filters")
        st.markdown(
            "Use the filters below to select specific **Apps** and **kmeans_cluster_name**. "
            "These filters apply to **both** the top (full date range) and bottom (date-filtered) plots."
        )

        # 1. Let user pick Apps
        all_apps = sorted(df_shortlisted['App'].unique())
        selected_apps = st.multiselect(
            "Select App(s)",
            options=all_apps,
            default=all_apps, 
            key="apps_tab3"
        )

        # 2. Let user pick Clusters
        all_clusters = sorted(df_shortlisted['kmeans_cluster_name'].unique())
        selected_clusters = st.multiselect(
            "Select kmeans_cluster_name(s)",
            options=all_clusters,
            default=all_clusters,
            key="clusters_tab3"
        )

        # 3. Filter the data by selected Apps and Clusters (TOP plot)
        df_tab3_filtered_top = df_shortlisted.copy()
        if selected_apps:
            df_tab3_filtered_top = df_tab3_filtered_top[df_tab3_filtered_top['App'].isin(selected_apps)]
        if selected_clusters:
            df_tab3_filtered_top = df_tab3_filtered_top[df_tab3_filtered_top['kmeans_cluster_name'].isin(selected_clusters)]

        st.subheader("Top Plot - Row-wise % (Filtered by App & Cluster, No Date Filter)")
        fig_tab3_top = create_percentage_heatmap(df_tab3_filtered_top)
        st.plotly_chart(fig_tab3_top, use_container_width=True, key="percentage_top_tab3")

        # 4. BOTTOM plot (App/Cluster + global date filter)
        st.subheader(f"Bottom Plot - Row-wise % (Filtered by App, Cluster, and Date [{start_date} to {end_date}])")

        df_tab3_filtered_bottom = df_bottom_filtered.copy()  # already date-filtered
        if selected_apps:
            df_tab3_filtered_bottom = df_tab3_filtered_bottom[df_tab3_filtered_bottom['App'].isin(selected_apps)]
        if selected_clusters:
            df_tab3_filtered_bottom = df_tab3_filtered_bottom[df_tab3_filtered_bottom['kmeans_cluster_name'].isin(selected_clusters)]

        fig_tab3_bottom = create_percentage_heatmap(df_tab3_filtered_bottom)
        st.plotly_chart(fig_tab3_bottom, use_container_width=True, key="percentage_bottom_tab3")


if __name__ == "__main__":
    main()
