import pandas as pd
import streamlit as st

from components.charts import (
    make_well_intensity_figure,
    make_well_oil_history_figure,
    make_well_onstream_figure,
    make_well_water_cut_figure,
)
from components.data import (
    load_historical_production,
    load_well_monitoring,
)
from components.styles import apply_global_styles


apply_global_styles()


# ---------------------------------------------------------
# Load frozen application artifacts
# ---------------------------------------------------------

history = load_historical_production()
monitoring = load_well_monitoring()


# ---------------------------------------------------------
# Page header
# ---------------------------------------------------------

st.markdown(
    '<div class="section-label">'
    'Producer Well Performance'
    '</div>',
    unsafe_allow_html=True,
)

st.title("Well Monitor")

st.markdown(
    '<div class="page-subtitle">'
    'Well-specific production history, operating behaviour '
    'and latest available monitoring condition.'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Well selection
# ---------------------------------------------------------

well_options = (
    monitoring["display_well_name"]
    .dropna()
    .tolist()
)

selector_column, context_column = st.columns(
    [1, 2]
)

with selector_column:
    selected_display_well = st.selectbox(
        "Producer well",
        options=well_options,
        index=0,
        width="stretch",
    )


selected_monitoring = monitoring.loc[
    monitoring["display_well_name"]
    == selected_display_well
].iloc[0]

selected_well_name = selected_monitoring[
    "NPD_WELL_BORE_NAME"
]

well_history = (
    history.loc[
        history["NPD_WELL_BORE_NAME"]
        == selected_well_name
    ]
    .sort_values("DATE")
    .reset_index(drop=True)
)


with context_column:
    st.markdown(
        f"""
        **Dataset well:** `{selected_well_name}`
        **Latest monitoring origin:** {
            selected_monitoring["monitoring_origin_label"]
        }
        """
    )


st.caption(
    "The latest monitoring origin is specific to the "
    "selected producer and should not be interpreted as "
    "a live or synchronized field measurement."
)

st.divider()


# ---------------------------------------------------------
# Latest producer condition
# ---------------------------------------------------------

latest_oil = selected_monitoring[
    "oil_volume"
]

production_age = selected_monitoring[
    "production_age_months"
]

on_stream_hours = selected_monitoring[
    "on_stream_hours"
]

water_cut = selected_monitoring[
    "water_cut_pct"
]

oil_change = selected_monitoring[
    "oil_volume_change_pct"
]

recent_mean = selected_monitoring[
    "recent_3_observation_mean_oil"
]


metric_1, metric_2, metric_3 = st.columns(3)

with metric_1:
    st.metric(
        "Latest oil",
        f"{latest_oil:,.0f}",
    )

with metric_2:
    st.metric(
        "Production age",
        f"{production_age:,.0f} months",
    )

with metric_3:
    st.metric(
        "On-stream hours",
        f"{on_stream_hours:,.1f}",
    )


metric_4, metric_5, metric_6 = st.columns(3)

with metric_4:
    st.metric(
        "Oil change",
        f"{oil_change:.1f}%",
    )

with metric_5:
    st.metric(
        "Water cut",
        (
            "N/A"
            if pd.isna(water_cut)
            else f"{water_cut:.1f}%"
        ),
    )

with metric_6:
    st.metric(
        "Recent 3-observation mean",
        f"{recent_mean:,.0f}",
    )


# ---------------------------------------------------------
# Monitoring context
# ---------------------------------------------------------

st.markdown("### Monitoring Context")

context_1, context_2, context_3 = st.columns(3)

with context_1:
    st.caption("Production state")
    st.markdown(
        "**"
        + str(
            selected_monitoring[
                "latest_production_state"
            ]
        )
        .replace("_", " ")
        .title()
        + "**"
    )

with context_2:
    st.caption("Recent direction")
    st.markdown(
        "**"
        + str(
            selected_monitoring[
                "recent_direction"
            ]
        )
        .replace("_", " ")
        .title()
        + "**"
    )

with context_3:
    st.caption("Ratio measurement state")
    st.markdown(
        "**"
        + str(
            selected_monitoring[
                "ratio_measurement_state"
            ]
        )
        .replace("_", " ")
        .title()
        + "**"
    )


st.divider()


# ---------------------------------------------------------
# Oil-production history
# ---------------------------------------------------------

st.markdown(
    f"### {selected_display_well} Oil Production History"
)

st.caption(
    "Monthly producer-well oil volume with its recent "
    "three-observation mean."
)

oil_figure = make_well_oil_history_figure(
    well_history
)

st.plotly_chart(
    oil_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# ---------------------------------------------------------
# Production behaviour
# ---------------------------------------------------------

left_chart, right_chart = st.columns(2)

with left_chart:
    st.markdown(
        "### Production Intensity"
    )

    st.caption(
        "Oil volume relative to recorded on-stream hours."
    )

    intensity_figure = (
        make_well_intensity_figure(
            well_history
        )
    )

    st.plotly_chart(
        intensity_figure,
        width="stretch",
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


with right_chart:
    st.markdown(
        "### Water-Cut Development"
    )

    st.caption(
        "Historical produced-water share for observations "
        "where the ratio is available."
    )

    water_cut_figure = (
        make_well_water_cut_figure(
            well_history
        )
    )

    st.plotly_chart(
        water_cut_figure,
        width="stretch",
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# ---------------------------------------------------------
# Operating history
# ---------------------------------------------------------

st.markdown("### Operating History")

st.caption(
    "Recorded monthly on-stream hours for the selected "
    "producer well. Amber × markers indicate recorded "
    "zero-hour months rather than missing observations."
)

onstream_figure = make_well_onstream_figure(
    well_history
)

st.plotly_chart(
    onstream_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# ---------------------------------------------------------
# Well-level forecast reliability context
# ---------------------------------------------------------

st.markdown("### Forecast Reliability Context")

reliability_1, reliability_2, reliability_3 = (
    st.columns(3)
)

with reliability_1:
    st.metric(
        "Persistence WAPE",
        (
            f"{selected_monitoring['persistence_WAPE_pct']:.1f}%"
        ),
    )

with reliability_2:
    st.metric(
        "Ridge WAPE",
        (
            f"{selected_monitoring['ridge_WAPE_pct']:.1f}%"
        ),
    )

with reliability_3:
    st.metric(
        "Negative Ridge forecasts",
        (
            f"{int(selected_monitoring['negative_ridge_forecasts'])}"
            f" / "
            f"{int(selected_monitoring['holdout_observations'])}"
        ),
    )


st.caption(
    "These reliability values come from the frozen final "
    "holdout evaluation. They describe historical forecast "
    "performance and are not engineering operating limits."
)


# ---------------------------------------------------------
# Provenance
# ---------------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="system-note">
    The Well Monitor presents historical analytical records
    generated by the validated notebook workflow. It does
    not provide live well telemetry, engineering alarms or
    automated production-control recommendations.
    </div>
    """,
    unsafe_allow_html=True,
)
