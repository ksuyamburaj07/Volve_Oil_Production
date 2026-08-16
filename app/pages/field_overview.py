import pandas as pd
import streamlit as st

from components.charts import (
    make_field_production_figure,
    make_latest_vs_recent_figure,
)
from components.data import (
    load_forecast_comparison,
    load_historical_production,
    load_well_monitoring,
)
from components.styles import apply_global_styles


apply_global_styles()


# ---------------------------------------------------------
# Load frozen application artifacts
# ---------------------------------------------------------

history = load_historical_production()
forecast_comparison = load_forecast_comparison()
monitoring = load_well_monitoring()


# ---------------------------------------------------------
# Overview statistics
# ---------------------------------------------------------

core_producer_count = (
    history["NPD_WELL_BORE_NAME"].nunique()
)

historical_record_count = len(history)

history_start = history["DATE"].min()
history_end = history["DATE"].max()

holdout_forecast_count = len(
    forecast_comparison
)

latest_positive_producers = int(
    (monitoring["oil_volume"] > 0).sum()
)


# ---------------------------------------------------------
# Page header
# ---------------------------------------------------------

st.markdown(
    '<div class="section-label">'
    'Field Performance'
    '</div>',
    unsafe_allow_html=True,
)

st.title("Field Overview")

st.markdown(
    '<div class="page-subtitle">'
    'Historical performance across the five core '
    'Volve producer wells, with production condition '
    'and forecasting coverage.'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# KPI strip
# ---------------------------------------------------------

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)

with kpi_1:
    st.metric(
        "Core producers",
        f"{core_producer_count}",
    )

with kpi_2:
    st.metric(
        "Historical records",
        f"{historical_record_count:,}",
    )

with kpi_3:
    st.metric(
        "History coverage",
        f"{history_start:%Y}–{str(history_end.year)[-2:]}",
    )

with kpi_4:
    st.metric(
        "Holdout forecasts",
        f"{holdout_forecast_count:,}",
    )

with kpi_5:
    st.metric(
        "Positive latest states",
        (
            f"{latest_positive_producers}"
            f" / "
            f"{core_producer_count}"
        ),
    )


st.caption(
    "Latest producer condition is evaluated at each "
    "well's own latest available monitoring origin. "
    "The five latest records are not assumed to represent "
    "one synchronous field date."
)

st.divider()


# ---------------------------------------------------------
# Historical field production
# ---------------------------------------------------------

st.markdown("### Core Producer Oil History")

st.caption(
    "Aggregated monthly oil volume from the core producer "
    "records available in the application history."
)

field_figure = make_field_production_figure(
    history
)

st.plotly_chart(
    field_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# ---------------------------------------------------------
# Latest versus recent producer performance
# ---------------------------------------------------------

st.markdown(
    "### Latest vs Recent Production"
)

st.caption(
    "Latest available oil volume compared with the "
    "recent three-observation mean for each producer."
)

latest_figure = make_latest_vs_recent_figure(
    monitoring
)

st.plotly_chart(
    latest_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# ---------------------------------------------------------
# Latest producer monitoring status
# ---------------------------------------------------------

st.markdown("### Latest Producer Status")

st.caption(
    "Well-specific monitoring condition at each producer's "
    "latest available application record."
)


status_display = pd.DataFrame(
    {
        "Well": monitoring["display_well_name"],

        "Origin": monitoring[
            "monitoring_origin_label"
        ],

        "Latest oil": monitoring[
            "oil_volume"
        ].map(
            lambda value: f"{value:,.0f}"
        ),

        "Oil change": monitoring[
            "oil_volume_change_pct"
        ].map(
            lambda value: f"{value:.1f}%"
        ),

        "Water cut": monitoring[
            "water_cut_pct"
        ].map(
            lambda value: (
                "N/A"
                if pd.isna(value)
                else f"{value:.1f}%"
            )
        ),

        "Production state": monitoring[
            "latest_production_state"
        ]
        .astype(str)
        .str.replace(
            "_",
            " ",
            regex=False,
        )
        .str.title(),
    }
)


st.table(
    status_display
)


# ---------------------------------------------------------
# Application provenance note
# ---------------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="system-note">
    Application data are frozen analytical artifacts produced
    by the validated notebook workflow. This page performs
    presentation and filtering only; it does not retrain or
    modify the forecasting model.
    </div>
    """,
    unsafe_allow_html=True,
)