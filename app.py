import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

def create_summation_heatmap(df):
    """
    Create a heatmap with summation of 'thumbsUpCount_222'.
    Each cell shows the total thumbsUpCount_222 for that App x kmeans_cluster_name.
    """
    pivot_data = df.groupby(['App', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(
        index='App',
        columns='kmeans_cluster_name',
        values='thumbsUpCount_222'
    ).fillna(0)

    fig = px.imshow(
        pivot_table,
        labels=dict(x="", y="", color=""),
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale="OrRd",
        text_auto=True,
        aspect="auto"
    )

    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))
    fig.update_layout(
        autosize=False,
        width=3200,
        height=900,  # default height
        margin=dict(l=60, r=60, t=80, b=50),
        xaxis_title=None,
        yaxis_title=None,
        coloraxis_showscale=False
    )
    fig.update_traces(
        hovertemplate="<b>App:</b> %{y}<br>"
                      "<b>kmeans_cluster_name:</b> %{x}<br>"
                      "<b>Sum thumbsUpCount_222:</b> %{z}",
        textfont_size=12
    )
    return fig


def create_percentage_heatmap(df):
    """
    Create a heatmap with row-wise percentages of 'thumbsUpCount_222'.
    Each row sums to 100%.
    """
    pivot_data = df.groupby(['App', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(
        index='App',
        columns='kmeans_cluster_name',
        values='thumbsUpCount_222'
    ).fillna(0)

    row_sums = pivot_table.sum(axis=1)
    percentage_table = pivot_table.div(row_sums, axis=0) * 100

    fig = px.imshow(
        percentage_table,
        labels=dict(x="", y="", color=""),
        x=percentage_table.columns,
        y=percentage_table.index,
        color_continuous_scale="OrRd",
        text_auto=True,
        aspect="auto"
    )

    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))
    fig.update_layout(
        autosize=False,
        width=3200,
        height=900,  # default height
        margin=dict(l=60, r=60, t=80, b=50),
        xaxis_title=None,
        yaxis_title=None,
        coloraxis_showscale=False
    )
    fig.update_traces(
        hovertemplate="<b>App:</b> %{y}<br>"
                      "<b>kmeans_cluster_name:</b> %{x}<br>"
                      "<b>% of thumbsUpCount_222 in row:</b> %{z:.2f}%",
        texttemplate="%{z:.1f}",
        textfont_size=12
    )
    return fig


def get_intra_app_swot_table(df):
    """
    1. Create row-wise % table from the original sums.
    2. Convert that row-wise % table into column-wise %.
       => Each column sums to 100%.
    Returns the final DataFrame (NOT a figure).
    """
    pivot_data = df.groupby(['App', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(
        index='App',
        columns='kmeans_cluster_name',
        values='thumbsUpCount_222'
    ).fillna(0)

    row_sums = pivot_table.sum(axis=1)
    row_wise_pct_table = pivot_table.div(row_sums, axis=0) * 100

    col_sums = row_wise_pct_table.sum(axis=0)
    col_wise_pct_table = row_wise_pct_table.div(col_sums, axis=1) * 100

    return col_wise_pct_table


def create_intra_app_swot_heatmap(df_table):
    """
    Each column sums to 100%.
    """
    fig = px.imshow(
        df_table,
        labels=dict(x="", y="", color=""),
        x=df_table.columns,
        y=df_table.index,
        color_continuous_scale="OrRd",
        text_auto=True,
        aspect="auto"
    )

    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))

    fig.update_layout(
        autosize=False,
        width=3200,
        height=900,
        margin=dict(l=60, r=60, t=80, b=50),
        coloraxis_showscale=False
    )
    fig.update_traces(
        hovertemplate="<b>App:</b> %{y}<br>"
                      "<b>kmeans_cluster_name:</b> %{x}<br>"
                      "<b>Column % (SWOT):</b> %{z:.2f}%",
        texttemplate="%{z:.1f}",
        textfont_size=12
    )
    return fig


def create_inter_app_strength_heatmap(df_table):
    """
    Takes the final table from Intra-App SWOT (column-wise %)
    and converts it to a row-wise % table => each row sums to 100%.
    """
    row_sums = df_table.sum(axis=1)
    row_wise_again = df_table.div(row_sums, axis=0) * 100

    fig = px.imshow(
        row_wise_again,
        labels=dict(x="", y="", color=""),
        x=row_wise_again.columns,
        y=row_wise_again.index,
        color_continuous_scale="OrRd",
        text_auto=True,
        aspect="auto"
    )

    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))

    fig.update_layout(
        autosize=False,
        width=3200,
        height=900,
        margin=dict(l=60, r=60, t=80, b=50),
        coloraxis_showscale=False
    )
    fig.update_traces(
        hovertemplate="<b>App:</b> %{y}<br>"
                      "<b>kmeans_cluster_name:</b> %{x}<br>"
                      "<b>Row % (Inter-App):</b> %{z:.2f}%",
        texttemplate="%{z:.1f}",
        textfont_size=12
    )
    return fig


def create_monthly_scatter_plot(df):
    """
    - Convert 'at' to monthly period
    - Group by (month_year, kmeans_cluster_name) summing thumbsUpCount_222
    - Circle size = sum(thumbsUpCount_222)
    - Legend at the bottom
    """
    if df.empty:
        return None

    df['month_year'] = df['at'].dt.to_period("M").dt.to_timestamp()
    grouped = df.groupby(['month_year', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()

    fig = px.scatter(
        grouped,
        x='month_year',
        y='thumbsUpCount_222',
        color='kmeans_cluster_name',
        size='thumbsUpCount_222',
        size_max=40,
        title="Monthly Summation of ThumbsUpCount_222 by kmeans_cluster_name",
        labels={
            'month_year': 'Month',
            'thumbsUpCount_222': 'Sum Thumbs Up'
        },
        hover_data=['kmeans_cluster_name', 'thumbsUpCount_222'],
    )

    fig.update_layout(
        autosize=False,
        width=1200,
        height=600,
        margin=dict(l=60, r=60, t=80, b=50),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_xaxes(
        tickformat="%Y-%m",
        tickangle=45,
        tickfont=dict(size=12),
        title_text="Month"
    )
    fig.update_yaxes(
        title_text="Summation of ThumbsUpCount_222",
        tickfont=dict(size=12)
    )
    return fig


def create_daily_scatter_plot(df):
    """
    - Convert 'at' to day (just date)
    - Group by (day, kmeans_cluster_name) summing thumbsUpCount_222
    - Circle size = sum(thumbsUpCount_222)
    - Legend at the bottom
    """
    if df.empty:
        return None

    df['day'] = df['at'].dt.date
    grouped = df.groupby(['day', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()

    fig = px.scatter(
        grouped,
        x='day',
        y='thumbsUpCount_222',
        color='kmeans_cluster_name',
        size='thumbsUpCount_222',
        size_max=40,
        title="Daily Summation of ThumbsUpCount_222 by kmeans_cluster_name",
        labels={
            'day': 'Day',
            'thumbsUpCount_222': 'Sum Thumbs Up'
        },
        hover_data=['kmeans_cluster_name', 'thumbsUpCount_222'],
    )

    fig.update_layout(
        autosize=False,
        width=1200,
        height=600,
        margin=dict(l=60, r=60, t=80, b=50),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_xaxes(
        tickangle=45,
        tickfont=dict(size=12),
        title_text="Day"
    )
    fig.update_yaxes(
        title_text="Summation of ThumbsUpCount_222",
        tickfont=dict(size=12)
    )
    return fig


# --------------------------------------------------------------------------------
# Updated helper functions for Tab 6 with increased height
# --------------------------------------------------------------------------------
def create_appversion_summation_heatmap(df_app_filtered):
    """
    Summation heatmap where rows = appVersion, columns = kmeans_cluster_name,
    values = sum(thumbsUpCount_222).
    """
    pivot_data = df_app_filtered.groupby(['appVersion', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(
        index='appVersion',
        columns='kmeans_cluster_name',
        values='thumbsUpCount_222'
    ).fillna(0)

    fig = px.imshow(
        pivot_table,
        labels=dict(x="kmeans_cluster_name", y="appVersion", color=""),
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale="OrRd",
        text_auto=True,
        aspect="auto"
    )

    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))

    # Increase height to 1100 (or other desired value)
    fig.update_layout(
        autosize=False,
        width=2200,
        height=1100,  # <--- increased height
        margin=dict(l=60, r=60, t=80, b=50),
        coloraxis_showscale=False
    )
    fig.update_traces(
        hovertemplate="<b>appVersion:</b> %{y}<br>"
                      "<b>kmeans_cluster_name:</b> %{x}<br>"
                      "<b>Sum thumbsUpCount_222:</b> %{z}",
        textfont_size=12
    )
    return fig


def create_appversion_percentage_heatmap(df_app_filtered):
    """
    Row-wise % heatmap for the top table in Tab 6.
    Rows = appVersion, columns = kmeans_cluster_name.
    Each row sums to 100%.
    """
    pivot_data = df_app_filtered.groupby(['appVersion', 'kmeans_cluster_name'])['thumbsUpCount_222'].sum().reset_index()
    pivot_table = pivot_data.pivot(
        index='appVersion',
        columns='kmeans_cluster_name',
        values='thumbsUpCount_222'
    ).fillna(0)

    row_sums = pivot_table.sum(axis=1)
    pct_table = pivot_table.div(row_sums, axis=0) * 100

    fig = px.imshow(
        pct_table,
        labels=dict(x="kmeans_cluster_name", y="appVersion", color=""),
        x=pct_table.columns,
        y=pct_table.index,
        color_continuous_scale="OrRd",
        text_auto=True,
        aspect="auto"
    )

    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))

    # Increase height to 1100 (or other desired value)
    fig.update_layout(
        autosize=False,
        width=2200,
        height=1100,  # <--- increased height
        margin=dict(l=60, r=60, t=80, b=50),
        coloraxis_showscale=False
    )
    fig.update_traces(
        hovertemplate="<b>appVersion:</b> %{y}<br>"
                      "<b>kmeans_cluster_name:</b> %{x}<br>"
                      "<b>% of row:</b> %{z:.2f}%",
        texttemplate="%{z:.1f}",
        textfont_size=12
    )
    return fig


def main():
    st.set_page_config(page_title="Heatmap Dashboard", layout="wide")
    st.markdown("### Heatmap of Summation of Thumbs Up Counts")

    # ----------------------------------------------------------------
    # 1. LOAD THE DATA
    # ----------------------------------------------------------------
    df_shortlisted = pd.read_pickle('df_shortlisted.pkl')

    # ----------------------------------------------------------------
    # 2. GLOBAL DATE FILTER (applies to bottom plots in tabs 1-3)
    # ----------------------------------------------------------------
    st.write("#### Global Date Filter for Bottom Plots (Tabs 1-3, 4-6 are unaffected by these filters)")
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

    mask_global = (df_shortlisted['at'].dt.date >= start_date) & (df_shortlisted['at'].dt.date <= end_date)
    df_bottom_filtered = df_shortlisted.loc[mask_global].copy()

    # ----------------------------------------------------------------
    # 3. CREATE TABS
    # ----------------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Tab 1: Summation Heatmaps",
        "Tab 2: Row-wise % Heatmaps",
        "Tab 3: Row-wise % + App/Cluster Filter",
        "Tab 4: SWOT & Strength Analysis",
        "Tab 5: Single App Time Charts",
        "Tab 6: Single AppVersion vs. kmeans_cluster"
    ])

    # ----------------------------------------
    # TAB 1: SUMMATION HEATMAPS
    # ----------------------------------------
    with tab1:
        st.subheader("Top Plot (Summation) - Full Data (No Date Filter)")
        fig_full_sum = create_summation_heatmap(df_shortlisted)
        st.plotly_chart(fig_full_sum, use_container_width=True, key="summation_top_tab1")

        st.subheader(f"Bottom Plot (Summation) - Date Filtered [{start_date} to {end_date}]")
        fig_filtered_sum = create_summation_heatmap(df_bottom_filtered)
        st.plotly_chart(fig_filtered_sum, use_container_width=True, key="summation_bottom_tab1")

    # ----------------------------------------
    # TAB 2: ROW-WISE % HEATMAPS
    # ----------------------------------------
    with tab2:
        st.subheader("Top Plot (Row-wise %) - Full Data (No Date Filter)")
        fig_full_pct = create_percentage_heatmap(df_shortlisted)
        st.plotly_chart(fig_full_pct, use_container_width=True, key="percentage_top_tab2")

        st.subheader(f"Bottom Plot (Row-wise %) - Date Filtered [{start_date} to {end_date}]")
        fig_filtered_pct = create_percentage_heatmap(df_bottom_filtered)
        st.plotly_chart(fig_filtered_pct, use_container_width=True, key="percentage_bottom_tab2")

    # ----------------------------------------
    # TAB 3: ROW-WISE % + APP & CLUSTER FILTERS
    # ----------------------------------------
    with tab3:
        st.subheader("Row-wise % Heatmaps with Additional Filters")
        st.markdown(
            "Use the filters below to select specific **Apps** and **kmeans_cluster_name**. "
            "These filters apply to **both** the top (full date range) and bottom (date-filtered) plots."
        )

        all_apps = sorted(df_shortlisted['App'].unique())
        selected_apps = st.multiselect("Select App(s)", options=all_apps, default=all_apps, key="apps_tab3")

        all_clusters = sorted(df_shortlisted['kmeans_cluster_name'].unique())
        selected_clusters = st.multiselect("Select kmeans_cluster_name(s)", options=all_clusters,
                                           default=all_clusters, key="clusters_tab3")

        df_tab3_top = df_shortlisted.copy()
        if selected_apps:
            df_tab3_top = df_tab3_top[df_tab3_top['App'].isin(selected_apps)]
        if selected_clusters:
            df_tab3_top = df_tab3_top[df_tab3_top['kmeans_cluster_name'].isin(selected_clusters)]

        st.subheader("Top Plot - Row-wise % (Filtered by App & Cluster, No Date Filter)")
        fig_tab3_top = create_percentage_heatmap(df_tab3_top)
        st.plotly_chart(fig_tab3_top, use_container_width=True, key="percentage_top_tab3")

        st.subheader(f"Bottom Plot - Row-wise % (Filtered by App, Cluster, and Date [{start_date} to {end_date}])")

        df_tab3_bottom = df_bottom_filtered.copy()
        if selected_apps:
            df_tab3_bottom = df_tab3_bottom[df_tab3_bottom['App'].isin(selected_apps)]
        if selected_clusters:
            df_tab3_bottom = df_tab3_bottom[df_tab3_bottom['kmeans_cluster_name'].isin(selected_clusters)]

        fig_tab3_bottom = create_percentage_heatmap(df_tab3_bottom)
        st.plotly_chart(fig_tab3_bottom, use_container_width=True, key="percentage_bottom_tab3")

    # ----------------------------------------
    # TAB 4: SWOT & STRENGTH ANALYSIS
    # ----------------------------------------
    with tab4:
        st.subheader("Inter-App SWOT Analysis (Top Plot, Full Data)")
        st.markdown(
            "This top plot starts with **row-wise %** of thumbsUpCount_222, "
            "then converts those values to **column-wise %** so each column sums to 100%."
        )

        intra_app_table = get_intra_app_swot_table(df_shortlisted)
        fig_intra_app_swot = create_intra_app_swot_heatmap(intra_app_table)
        st.plotly_chart(fig_intra_app_swot, use_container_width=True, key="tab4_intra_app_swot_top")

        st.subheader("Intra-App Strength Analysis (Bottom Plot, Full Data)")
        st.markdown(
            "Now we take the Inter-App SWOT table above (where each column sums to 100%) "
            "and calculate **row-wise %** again, so each row sums to 100%. "
            "We call this 'Inter-App Strength Analysis.'"
        )

        fig_inter_app_strength = create_inter_app_strength_heatmap(intra_app_table)
        st.plotly_chart(fig_inter_app_strength, use_container_width=True, key="tab4_intra_app_strength_bottom")

    # ----------------------------------------
    # TAB 5: SINGLE APP TIME CHARTS
    # ----------------------------------------
    with tab5:
        st.subheader("Single App - Monthly and Daily Summation Charts (No Date Filter)")
        st.markdown(
            "Pick an **App** and optionally some **kmeans_cluster_name** categories. "
            "We’ll plot monthly and daily summations of thumbsUpCount_222 with distinct colors for each cluster. "
            "Circle size is proportional to thumbsUpCount_222, and the legend is shown at the bottom."
        )

        all_apps_5 = sorted(df_shortlisted['App'].unique())
        selected_app_5 = st.selectbox("Select an App", options=all_apps_5, key="tab5_app")

        all_clusters_5 = sorted(df_shortlisted['kmeans_cluster_name'].unique())
        selected_clusters_5 = st.multiselect("Select kmeans_cluster_name(s) to include",
                                             options=all_clusters_5,
                                             default=all_clusters_5,
                                             key="tab5_clusters")

        df_tab5 = df_shortlisted.copy()
        df_tab5 = df_tab5[df_tab5['App'] == selected_app_5]
        if selected_clusters_5:
            df_tab5 = df_tab5[df_tab5['kmeans_cluster_name'].isin(selected_clusters_5)]

        st.subheader("Monthly Summation Chart")
        fig_monthly = create_monthly_scatter_plot(df_tab5)
        if fig_monthly is None:
            st.warning("No data available for the selected filters (monthly).")
        else:
            st.plotly_chart(fig_monthly, use_container_width=True, key="tab5_monthly_scatter")

        st.subheader("Daily Summation Chart")
        fig_daily = create_daily_scatter_plot(df_tab5)
        if fig_daily is None:
            st.warning("No data available for the selected filters (daily).")
        else:
            st.plotly_chart(fig_daily, use_container_width=True, key="tab5_daily_scatter")

    # ----------------------------------------
    # TAB 6: SINGLE APPVERSION vs. kmeans_cluster
    # ----------------------------------------
    with tab6:
        st.subheader("Single AppVersion vs. kmeans_cluster_name (No Date Filter)")
        st.markdown(
            "Pick an **App**. We'll display two plots:\n"
            "1. Summation heatmap of `thumbsUpCount_222` with rows=appVersion, columns=kmeans_cluster_name.\n"
            "2. Row-wise percentage heatmap of the same table."
        )

        # 1) Select one App
        all_apps_6 = sorted(df_shortlisted['App'].unique())
        selected_app_6 = st.selectbox("Select an App", options=all_apps_6, key="tab6_app")

        # 2) Filter data for that App
        df_tab6 = df_shortlisted[df_shortlisted['App'] == selected_app_6].copy()

        # 3) Summation heatmap (increased height)
        st.subheader("Top Plot: Summation Heatmap (appVersion vs. kmeans_cluster_name)")
        fig_tab6_sum = create_appversion_summation_heatmap(df_tab6)  # <-- increased height inside function
        st.plotly_chart(fig_tab6_sum, use_container_width=True, key="tab6_sum_heatmap")

        # 4) Row-wise percentage heatmap (increased height)
        st.subheader("Bottom Plot: Row-wise Percentage Heatmap")
        fig_tab6_pct = create_appversion_percentage_heatmap(df_tab6)  # <-- increased height inside function
        st.plotly_chart(fig_tab6_pct, use_container_width=True, key="tab6_pct_heatmap")


if __name__ == "__main__":
    main()
