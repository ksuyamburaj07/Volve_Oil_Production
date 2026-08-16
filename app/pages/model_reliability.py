import numpy as np
import streamlit as st

from components.charts import (
    make_negative_forecast_incidence_figure,
    make_well_wape_comparison_figure,
)
from components.data import (
    load_forecast_comparison,
    load_well_monitoring,
)
from components.styles import apply_global_styles


apply_global_styles()


# ---------------------------------------------------------
# Load frozen application artifacts
# ---------------------------------------------------------

forecast_data = load_forecast_comparison()
monitoring = load_well_monitoring()


# ---------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------

actual = forecast_data[
    "target_next_month_oil_volume"
].to_numpy()

persistence = forecast_data[
    "persistence_prediction"
].to_numpy()

ridge = forecast_data[
    "ridge_prediction"
].to_numpy()


def calculate_mae(
    observed,
    predicted,
):
    return np.mean(
        np.abs(
            observed - predicted
        )
    )


def calculate_rmse(
    observed,
    predicted,
):
    return np.sqrt(
        np.mean(
            (observed - predicted) ** 2
        )
    )


def calculate_wape(
    observed,
    predicted,
):
    denominator = np.sum(
        np.abs(observed)
    )

    return (
        np.sum(
            np.abs(
                observed - predicted
            )
        )
        / denominator
        * 100
    )


def calculate_r_squared(
    observed,
    predicted,
):
    residual_sum = np.sum(
        (observed - predicted) ** 2
    )

    total_sum = np.sum(
        (
            observed
            - np.mean(observed)
        ) ** 2
    )

    return (
        1
        - residual_sum / total_sum
    )


# ---------------------------------------------------------
# Pooled final-holdout metrics
# ---------------------------------------------------------

persistence_mae = calculate_mae(
    actual,
    persistence,
)

persistence_rmse = calculate_rmse(
    actual,
    persistence,
)

persistence_wape = calculate_wape(
    actual,
    persistence,
)

persistence_r2 = calculate_r_squared(
    actual,
    persistence,
)

ridge_mae = calculate_mae(
    actual,
    ridge,
)

ridge_rmse = calculate_rmse(
    actual,
    ridge,
)

ridge_wape = calculate_wape(
    actual,
    ridge,
)

ridge_r2 = calculate_r_squared(
    actual,
    ridge,
)


# ---------------------------------------------------------
# Holdout scope
# ---------------------------------------------------------

forecast_count = len(
    forecast_data
)

well_count = forecast_data[
    "NPD_WELL_BORE_NAME"
].nunique()

origin_start = forecast_data[
    "DATE"
].min()

origin_end = forecast_data[
    "DATE"
].max()

target_start = forecast_data[
    "target_month"
].min()

target_end = forecast_data[
    "target_month"
].max()

negative_ridge_count = int(
    forecast_data[
        "ridge_negative_prediction"
    ].sum()
)


# ---------------------------------------------------------
# Page-specific styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .matrix-header {
        color: #AAB2BF;
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 4px 0 10px 0;
    }

    .matrix-metric {
        color: #E8EAED;
        font-size: 1rem;
        font-weight: 650;
        padding: 12px 0;
        display: flex;
        align-items: center;
        min-height: 54px;
    }

    .matrix-value {
        color: #F0F2F5;
        font-size: 1.55rem;
        font-weight: 650;
        font-variant-numeric: tabular-nums;
        padding: 12px 0;
        display: flex;
        align-items: center;
        min-height: 54px;
    }

    .matrix-result {
        color: #E8EAED;
        font-size: 1rem;
        font-weight: 650;
        padding: 12px 0;
        display: flex;
        align-items: center;
        min-height: 54px;
    }

    .matrix-rule {
        border-top: 1px solid #343B47;
        margin: 2px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Page header
# ---------------------------------------------------------

st.markdown(
    '<div class="section-label">'
    'Final Holdout Evaluation'
    '</div>',
    unsafe_allow_html=True,
)

st.title("Model Reliability")

st.markdown(
    '<div class="page-subtitle">'
    'Out-of-sample reliability of the Persistence benchmark '
    'and the frozen Ridge Regression model.'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Final holdout scope
# ---------------------------------------------------------

scope_1, scope_2 = st.columns(2)

with scope_1:
    st.metric(
        "Forecast records",
        f"{forecast_count}",
    )

with scope_2:
    st.metric(
        "Producer wells",
        f"{well_count}",
    )


period_1, period_2 = st.columns(2)

with period_1:
    with st.container(border=True):
        st.caption(
            "FORECAST-ORIGIN PERIOD"
        )

        st.markdown(
            f"### {origin_start:%b %Y} – "
            f"{origin_end:%b %Y}"
        )

        st.write(
            "Months at which the one-month-ahead "
            "forecast was generated."
        )


with period_2:
    with st.container(border=True):
        st.caption(
            "TARGET PERIOD"
        )

        st.markdown(
            f"### {target_start:%b %Y} – "
            f"{target_end:%b %Y}"
        )

        st.write(
            "Observed months evaluated one month after "
            "the corresponding forecast origins."
        )


st.caption(
    "Forecast origins span April 2015 through August 2016. "
    "Because the forecasting horizon is one month ahead, "
    "the corresponding target observations span May 2015 "
    "through September 2016. The final holdout was examined "
    "only after model development and selection were complete."
)

st.divider()


# ---------------------------------------------------------
# Pooled holdout performance
# ---------------------------------------------------------

st.markdown(
    "### Pooled Holdout Performance"
)

st.caption(
    "Persistence and Ridge Regression are evaluated across "
    "the same 80 final-holdout forecast records."
)


performance_rows = [
    (
        "MAE",
        f"{persistence_mae:,.0f}",
        f"{ridge_mae:,.0f}",
    ),
    (
        "RMSE",
        f"{persistence_rmse:,.0f}",
        f"{ridge_rmse:,.0f}",
    ),
    (
        "WAPE",
        f"{persistence_wape:.1f}%",
        f"{ridge_wape:.1f}%",
    ),
    (
        "R²",
        f"{persistence_r2:.3f}",
        f"{ridge_r2:.3f}",
    ),
]


with st.container(border=True):

    header_1, header_2, header_3, header_4 = (
        st.columns(
            [0.8, 1.2, 1.2, 1.0]
        )
    )

    with header_1:
        st.markdown(
            '<div class="matrix-header">'
            'Metric'
            '</div>',
            unsafe_allow_html=True,
        )

    with header_2:
        st.markdown(
            '<div class="matrix-header">'
            'Persistence'
            '</div>',
            unsafe_allow_html=True,
        )

    with header_3:
        st.markdown(
            '<div class="matrix-header">'
            'Ridge Regression'
            '</div>',
            unsafe_allow_html=True,
        )

    with header_4:
        st.markdown(
            '<div class="matrix-header">'
            'Best Result'
            '</div>',
            unsafe_allow_html=True,
        )


    st.markdown(
        '<div class="matrix-rule"></div>',
        unsafe_allow_html=True,
    )


    for index, (
        metric_name,
        persistence_value,
        ridge_value,
    ) in enumerate(
        performance_rows
    ):

        (
            column_1,
            column_2,
            column_3,
            column_4,
        ) = st.columns(
            [0.8, 1.2, 1.2, 1.0]
        )

        with column_1:
            st.markdown(
                f'<div class="matrix-metric">'
                f'{metric_name}'
                f'</div>',
                unsafe_allow_html=True,
            )

        with column_2:
            st.markdown(
                f'<div class="matrix-value">'
                f'{persistence_value}'
                f'</div>',
                unsafe_allow_html=True,
            )

        with column_3:
            st.markdown(
                f'<div class="matrix-value">'
                f'{ridge_value}'
                f'</div>',
                unsafe_allow_html=True,
            )

        with column_4:
            st.markdown(
                '<div class="matrix-result">'
                'Persistence'
                '</div>',
                unsafe_allow_html=True,
            )

        if index < len(
            performance_rows
        ) - 1:
            st.markdown(
                '<div class="matrix-rule"></div>',
                unsafe_allow_html=True,
            )


st.caption(
    "Lower values indicate better performance for MAE, RMSE "
    "and WAPE. Higher values indicate better performance for "
    "R². Persistence performed better on all four pooled "
    "final-holdout metrics."
)

st.divider()


# ---------------------------------------------------------
# Per-well reliability
# ---------------------------------------------------------

st.markdown(
    "### Reliability by Producer Well"
)

st.caption(
    "WAPE is shown separately for each of the five core "
    "producer wells."
)

wape_figure = (
    make_well_wape_comparison_figure(
        monitoring
    )
)

st.plotly_chart(
    wape_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


# ---------------------------------------------------------
# Negative forecast behaviour
# ---------------------------------------------------------

st.markdown(
    "### Negative Ridge Forecast Incidence"
)

st.caption(
    "The unconstrained Ridge model can produce physically "
    "implausible negative oil forecasts. No retrospective "
    "clipping was applied."
)

negative_figure = (
    make_negative_forecast_incidence_figure(
        monitoring
    )
)

st.plotly_chart(
    negative_figure,
    width="stretch",
    config={
        "displayModeBar": False,
        "responsive": True,
    },
)


negative_1, negative_2 = (
    st.columns(2)
)

with negative_1:
    st.metric(
        "Negative Ridge forecasts",
        (
            f"{negative_ridge_count}"
            f" / "
            f"{forecast_count}"
        ),
    )

with negative_2:
    st.metric(
        "Holdout incidence",
        (
            f"{negative_ridge_count / forecast_count * 100:.1f}%"
        ),
    )


# ---------------------------------------------------------
# Final evaluation interpretation
# ---------------------------------------------------------

st.divider()

st.markdown(
    "### Final Evaluation Outcome"
)

st.markdown(
    f"""
On the untouched final holdout, **Persistence produced the
stronger overall forecasting result**.

Persistence achieved lower MAE
({persistence_mae:,.0f} vs {ridge_mae:,.0f}),
lower RMSE
({persistence_rmse:,.0f} vs {ridge_rmse:,.0f}),
lower WAPE
({persistence_wape:.1f}% vs {ridge_wape:.1f}%),
and higher R²
({persistence_r2:.3f} vs {ridge_r2:.3f}).

Ridge Regression remains the frozen selected
machine-learning pipeline because its selection occurred
during development before the final holdout was examined.
The holdout result is therefore retained as evidence that
the selected machine-learning model did not generalize
better than the simple Persistence benchmark.
"""
)


st.markdown(
    """
    <div class="system-note">
    Reliability statistics are historical evaluation results,
    not guarantees of future forecasting performance and not
    engineering operating limits.
    </div>
    """,
    unsafe_allow_html=True,
)