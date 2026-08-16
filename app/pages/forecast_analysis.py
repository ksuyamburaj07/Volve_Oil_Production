import pandas as pd
import streamlit as st

from components.charts import (
    make_forecast_error_figure,
    make_forecast_event_figure,
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
forecast_data = load_forecast_comparison()
monitoring = load_well_monitoring()


# ---------------------------------------------------------
# Display-name mapping
# ---------------------------------------------------------

well_name_map = dict(
    zip(
        monitoring["NPD_WELL_BORE_NAME"],
        monitoring["display_well_name"],
    )
)

forecast_wells = sorted(
    forecast_data["NPD_WELL_BORE_NAME"]
    .dropna()
    .unique()
)

display_to_dataset = {
    well_name_map.get(well, well): well
    for well in forecast_wells
}


# ---------------------------------------------------------
# Page header
# ---------------------------------------------------------

st.markdown(
    '<div class="section-label">'
    'One-Month-Ahead Forecasting'
    '</div>',
    unsafe_allow_html=True,
)

st.title("Forecast Analysis")

st.markdown(
    '<div class="page-subtitle">'
    'Historical forecast evaluation using the frozen '
    'Persistence benchmark and selected Ridge Regression '
    'pipeline.'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Forecast selection
# ---------------------------------------------------------

selector_1, selector_2 = st.columns(2)

with selector_1:
    selected_display_well = st.selectbox(
        "Producer well",
        options=list(
            display_to_dataset.keys()
        ),
        width="stretch",
    )


selected_well = display_to_dataset[
    selected_display_well
]

well_forecasts = (
    forecast_data.loc[
        forecast_data[
            "NPD_WELL_BORE_NAME"
        ]
        == selected_well
    ]
    .sort_values("DATE")
    .reset_index(drop=True)
)

forecast_origins = (
    well_forecasts["DATE"]
    .drop_duplicates()
    .tolist()
)


with selector_2:
    selected_origin = st.selectbox(
        "Forecast origin",
        options=forecast_origins,
        index=len(forecast_origins) - 1,
        format_func=lambda value: (
            value.strftime("%B %Y")
        ),
        width="stretch",
    )


selected_forecast = (
    well_forecasts.loc[
        well_forecasts["DATE"]
        == selected_origin
    ]
    .iloc[0]
)


target_month = selected_forecast[
    "target_month"
]

well_history = (
    history.loc[
        history[
            "NPD_WELL_BORE_NAME"
        ]
        == selected_well
    ]
    .sort_values("DATE")
    .reset_index(drop=True)
)


# ---------------------------------------------------------
# Forecast-origin production context
# ---------------------------------------------------------

origin_context_matches = history.loc[
    (
        history["NPD_WELL_BORE_NAME"]
        == selected_well
    )
    &
    (
        history["DATE"]
        == selected_origin
    )
]

if origin_context_matches.empty:
    origin_context = None
else:
    origin_context = (
        origin_context_matches.iloc[0]
    )


# ---------------------------------------------------------
# Forecast horizon banner
# ---------------------------------------------------------

st.markdown(
    f"""
    **Forecast origin:** {selected_origin:%B %Y}
    **Forecast target:** {target_month:%B %Y}
    **Forecast horizon:** One month ahead
    """
)

st.caption(
    "This page replays observations from the frozen final "
    "holdout evaluation. Changing the selector does not "
    "retrain, retune or replace either forecasting approach."
)

st.divider()


# ---------------------------------------------------------
# Forecast result strip
# ---------------------------------------------------------

current_oil = selected_forecast[
    "oil_volume"
]

persistence_prediction = selected_forecast[
    "persistence_prediction"
]

ridge_prediction = selected_forecast[
    "ridge_prediction"
]

observed_target = selected_forecast[
    "target_next_month_oil_volume"
]


result_1, result_2, result_3, result_4 = (
    st.columns(4)
)

with result_1:
    st.metric(
        "Current oil",
        f"{current_oil:,.0f}",
    )

with result_2:
    st.metric(
        "Persistence forecast",
        f"{persistence_prediction:,.0f}",
    )

with result_3:
    st.metric(
        "Ridge forecast",
        f"{ridge_prediction:,.0f}",
    )

with result_4:
    st.metric(
        "Observed next month",
        f"{observed_target:,.0f}",
    )


if ridge_prediction < 0:
    st.warning(
        "The frozen Ridge model produced a negative oil "
        "forecast for this historical observation. The "
        "prediction is displayed unchanged because no "
        "retrospective clipping was applied."
    )


# ---------------------------------------------------------
# Forecast event chart
# ---------------------------------------------------------

st.markdown(
    f"### {selected_display_well} Forecast Event"
)

st.caption(
    "Historical production together with the selected "
    "forecast origin, next-month observation and both "
    "forecasting approaches."
)

forecast_figure = make_forecast_event_figure(
    well_history,
    selected_forecast,
)

st.plotly_chart(
    forecast_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# ---------------------------------------------------------
# Forecast error
# ---------------------------------------------------------

st.markdown("### Forecast Error")

persistence_error = selected_forecast[
    "persistence_absolute_error"
]

ridge_error = selected_forecast[
    "ridge_absolute_error"
]

error_difference = selected_forecast[
    "ridge_minus_persistence_absolute_error"
]


error_1, error_2, error_3 = st.columns(3)

with error_1:
    st.metric(
        "Persistence absolute error",
        f"{persistence_error:,.0f}",
    )

with error_2:
    st.metric(
        "Ridge absolute error",
        f"{ridge_error:,.0f}",
    )

with error_3:
    st.metric(
        "Ridge minus persistence",
        f"{error_difference:,.0f}",
    )


error_figure = make_forecast_error_figure(
    selected_forecast
)

st.plotly_chart(
    error_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# ---------------------------------------------------------
# Production context at forecast origin
# ---------------------------------------------------------

st.markdown(
    "### Production Context at Forecast Origin"
)

st.caption(
    "Historical producer variables available at the "
    "selected forecast origin."
)


if origin_context is not None:
    production_age = origin_context[
        "production_age_months"
    ]

    on_stream_hours = origin_context[
        "on_stream_hours"
    ]

    water_cut = origin_context[
        "water_cut_pct"
    ]

    production_intensity = origin_context[
        "oil_per_on_stream_hour"
    ]

    recent_mean = origin_context[
        "oil_volume_recent_mean_3"
    ]

    context_1, context_2, context_3 = (
        st.columns(3)
    )

    with context_1:
        st.metric(
            "Production age",
            f"{production_age:,.0f} months",
        )

    with context_2:
        st.metric(
            "On-stream hours",
            f"{on_stream_hours:,.1f}",
        )

    with context_3:
        st.metric(
            "Water cut",
            (
                "N/A"
                if pd.isna(water_cut)
                else f"{water_cut:.1f}%"
            ),
        )


    context_4, context_5 = st.columns(2)

    with context_4:
        st.metric(
            "Oil per on-stream hour",
            (
                "N/A"
                if pd.isna(
                    production_intensity
                )
                else (
                    f"{production_intensity:,.2f}"
                )
            ),
        )

    with context_5:
        st.metric(
            "Recent 3-observation mean",
            f"{recent_mean:,.0f}",
        )

else:
    st.info(
        "Production-context variables are unavailable "
        "for this forecast origin."
    )


# ---------------------------------------------------------
# Historical well-level reliability
# ---------------------------------------------------------

selected_monitoring = monitoring.loc[
    monitoring[
        "NPD_WELL_BORE_NAME"
    ]
    == selected_well
].iloc[0]


st.markdown(
    "### Well-Level Holdout Reliability"
)

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
    "The values above summarize all final-holdout forecast "
    "records for the selected producer. They should not be "
    "interpreted as an uncertainty interval for the single "
    "forecast event displayed above."
)


# ---------------------------------------------------------
# Interpretation note
# ---------------------------------------------------------

st.divider()

if persistence_error < ridge_error:
    comparison_statement = (
        "Persistence produced the lower absolute error "
        "for this forecast event."
    )
elif ridge_error < persistence_error:
    comparison_statement = (
        "Ridge Regression produced the lower absolute "
        "error for this forecast event."
    )
else:
    comparison_statement = (
        "Both approaches produced the same absolute "
        "error for this forecast event."
    )


st.markdown(
    f"""
    **Event interpretation**

    {comparison_statement}

    The comparison is descriptive for this historical
    forecast origin. Model selection is not reopened from
    individual forecast events, and the final holdout remains
    the basis for overall out-of-sample evaluation.
    """
)


st.markdown(
    """
    <div class="system-note">
    Forecast Analysis is a historical evaluation interface,
    not a live production forecast service. Forecasts shown
    here are frozen outputs from the validated modelling
    workflow.
    </div>
    """,
    unsafe_allow_html=True,
)
