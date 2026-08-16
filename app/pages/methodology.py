import pandas as pd
import streamlit as st

from components.data import (
    load_limitations,
    load_metadata,
)
from components.styles import apply_global_styles


apply_global_styles()


# ---------------------------------------------------------
# Load frozen application documentation artifacts
# ---------------------------------------------------------

metadata = load_metadata()
limitations = load_limitations()


project = metadata["project"]
forecasting_task = metadata["forecasting_task"]
selected_model = metadata["selected_model"]
benchmark = metadata["benchmark"]
validation = metadata["validation"]
holdout_results = metadata["final_holdout_results"]
application_scope = metadata["application_scope"]
provenance = metadata["provenance"]


holdout_start = pd.to_datetime(
    validation["final_holdout_origin_start"]
)

holdout_end = pd.to_datetime(
    validation["final_holdout_origin_end"]
)


# ---------------------------------------------------------
# Page header
# ---------------------------------------------------------

st.markdown(
    '<div class="section-label">'
    'Technical Documentation'
    '</div>',
    unsafe_allow_html=True,
)

st.title("Methodology & Limitations")

st.markdown(
    '<div class="page-subtitle">'
    'Forecasting design, validation framework, application '
    'scope and known limitations of the Volve historical '
    'production-intelligence case study.'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Project scope
# ---------------------------------------------------------

st.markdown("### Project Scope")

scope_1, scope_2, scope_3 = st.columns(3)

with scope_1:
    st.metric(
        "Core producer wells",
        len(
            application_scope[
                "core_producer_wells"
            ]
        ),
    )

with scope_2:
    st.metric(
        "Historical app records",
        application_scope[
            "historical_application_rows"
        ],
    )

with scope_3:
    st.metric(
        "Holdout forecasts",
        application_scope[
            "forecast_comparison_rows"
        ],
    )


with st.container(border=True):
    st.markdown(
        f"**Case study:** {project['case_study']}"
    )

    st.markdown(
        f"**Application type:** "
        f"{project['application_type']}"
    )

    st.markdown(
        f"**Monitoring interpretation:** "
        f"{application_scope['latest_monitoring_origin']}"
    )


st.divider()


# ---------------------------------------------------------
# Forecasting task
# ---------------------------------------------------------

st.markdown("### Forecasting Design")

design_1, design_2 = st.columns(2)

with design_1:
    with st.container(border=True):
        st.caption("FORECASTING TASK")

        st.markdown(
            f"**Target**  \n"
            f"{forecasting_task['target']}"
        )

        st.markdown(
            f"**Forecast horizon**  \n"
            f"{forecasting_task['forecast_horizon']}"
        )

        st.markdown(
            f"**Forecast origin**  \n"
            f"{forecasting_task['forecast_origin']}"
        )

        st.markdown(
            f"**Model scope**  \n"
            f"{forecasting_task['model_scope']}"
        )


with design_2:
    with st.container(border=True):
        st.caption("SELECTED MACHINE-LEARNING MODEL")

        st.markdown(
            f"**Algorithm**  \n"
            f"{selected_model['algorithm']}"
        )

        st.markdown(
            f"**Ridge alpha**  \n"
            f"{selected_model['ridge_alpha']}"
        )

        st.markdown(
            f"**Numeric inputs**  \n"
            f"{selected_model['numeric_feature_count']}"
        )

        st.markdown(
            f"**Categorical inputs**  \n"
            f"{selected_model['categorical_feature_count']}"
        )

        st.markdown(
            f"**Total input columns**  \n"
            f"{selected_model['total_input_columns']}"
        )


st.divider()


# ---------------------------------------------------------
# Benchmark
# ---------------------------------------------------------

st.markdown("### Benchmark Strategy")

with st.container(border=True):
    st.markdown(
        f"**{benchmark['approach']}**"
    )

    st.write(
        benchmark["definition"]
    )

    st.info(
        benchmark["final_observation"]
    )


st.caption(
    "The persistence benchmark is intentionally simple. "
    "A trained forecasting model must provide useful "
    "out-of-sample improvement over this reference before "
    "greater model complexity can be considered beneficial."
)


# ---------------------------------------------------------
# Temporal validation
# ---------------------------------------------------------

st.markdown("### Validation Framework")

validation_left, validation_right = st.columns(2)

with validation_left:
    with st.container(border=True):
        st.caption("VALIDATION STRATEGY")

        st.markdown(
            f"### {validation['strategy']}"
        )

        st.write(
            validation["development_design"]
        )

with validation_right:
    with st.container(border=True):
        st.caption("FINAL HOLDOUT ORIGINS")

        st.markdown(
            f"### {holdout_start:%b %Y} – {holdout_end:%b %Y}"
        )

        st.write(
            f"{validation['final_holdout_observations']} "
            f"forecast observations across "
            f"{validation['final_holdout_wells']} "
            f"producer wells."
        )


control_left, control_right = st.columns(2)

with control_left:
    with st.container(border=True):
        st.caption("RANDOM TRAIN-TEST SPLIT")

        st.markdown(
            "### No"
            if not validation["random_split_used"]
            else "### Yes"
        )

        st.write(
            "Random splitting was intentionally avoided "
            "because the forecasting problem is temporally "
            "ordered."
        )

with control_right:
    with st.container(border=True):
        st.caption("POST-HOLDOUT RETUNING")

        st.markdown(
            "### No"
            if not validation["post_holdout_retuning"]
            else "### Yes"
        )

        st.write(
            "Model selection and tuning were completed "
            "before the untouched final holdout was examined."
        )


st.caption(
    "The development period used expanding-window temporal "
    "validation. The untouched final holdout spans forecast "
    "origins from April 2015 through August 2016, with "
    "one-month-ahead targets extending through September 2016."
)

st.divider()

# ---------------------------------------------------------
# Frozen final evaluation
# ---------------------------------------------------------

st.markdown("### Frozen Final Evaluation")

persistence_results = holdout_results[
    "persistence"
]

ridge_results = holdout_results[
    "ridge_regression"
]


evaluation_table = pd.DataFrame(
    {
        "Approach": [
            "Persistence",
            "Ridge Regression",
        ],
        "MAE": [
            persistence_results["MAE"],
            ridge_results["MAE"],
        ],
        "RMSE": [
            persistence_results["RMSE"],
            ridge_results["RMSE"],
        ],
        "WAPE (%)": [
            persistence_results["WAPE_pct"],
            ridge_results["WAPE_pct"],
        ],
        "R²": [
            persistence_results["R2"],
            ridge_results["R2"],
        ],
    }
)


st.dataframe(
    evaluation_table,
    hide_index=True,
    width="stretch",
    column_config={
        "Approach": "Approach",
        "MAE": st.column_config.NumberColumn(
            "MAE",
            format="%.0f",
        ),
        "RMSE": st.column_config.NumberColumn(
            "RMSE",
            format="%.0f",
        ),
        "WAPE (%)": st.column_config.NumberColumn(
            "WAPE (%)",
            format="%.1f",
        ),
        "R²": st.column_config.NumberColumn(
            "R²",
            format="%.3f",
        ),
    },
)


st.markdown(
    f"""
The selected Ridge Regression model was retained as the
frozen machine-learning pipeline because selection occurred
during model development.

On the untouched final holdout, however, **Persistence
produced the stronger observed out-of-sample result**.

Ridge Regression also produced
**{ridge_results['negative_predictions']} negative forecasts**
during the final holdout. These predictions were retained
unchanged rather than retrospectively clipped.
"""
)


st.divider()


# ---------------------------------------------------------
# Application boundaries
# ---------------------------------------------------------

st.markdown("### Application Boundaries")

boundary_1, boundary_2 = st.columns(2)

with boundary_1:
    with st.container(border=True):
        st.markdown("**What the application does**")

        st.markdown(
            """
- Presents historical Volve producer-well behaviour.
- Supports well-specific production monitoring.
- Replays frozen one-month-ahead forecast evaluations.
- Compares Ridge Regression with Persistence.
- Presents historical forecast reliability.
- Preserves structural missingness and negative-model diagnostics.
            """
        )


with boundary_2:
    with st.container(border=True):
        st.markdown("**What the application does not do**")

        st.markdown(
            """
- It is not connected to live field telemetry.
- It is not a SCADA or production-control system.
- It does not provide engineering alarm thresholds.
- It does not perform reservoir simulation.
- It does not automate production optimization.
- It does not provide causal engineering conclusions.
            """
        )


st.caption(
    "The interface should therefore be interpreted as a "
    "historical analytical and decision-support case study, "
    "not as a live field-operating platform."
)


st.divider()


# ---------------------------------------------------------
# Limitations
# ---------------------------------------------------------

st.markdown("### Study & Application Limitations")

st.caption(
    "These limitations are exported directly from the "
    "validated application-integration workflow."
)


for _, row in limitations.iterrows():
    title = (
        f"{row['limitation_id']} · "
        f"{row['category']}"
    )

    with st.expander(
        title,
        expanded=False,
    ):
        st.markdown(
            "**Limitation**"
        )

        st.write(
            row["limitation"]
        )

        st.markdown(
            "**Application implication**"
        )

        st.write(
            row[
                "application_implication"
            ]
        )


st.divider()


# ---------------------------------------------------------
# Analytical provenance
# ---------------------------------------------------------

st.markdown("### Analytical Provenance")

st.caption(
    "Application artifacts are generated from the frozen "
    "analytical workflow rather than reconstructed manually "
    "inside Streamlit."
)


provenance_rows = []

for notebook_name, role in provenance.items():
    readable_name = (
        notebook_name
        .replace(
            "notebook_",
            "Notebook ",
        )
    )

    provenance_rows.append(
        {
            "Workflow stage": readable_name,
            "Role": role,
        }
    )


provenance_table = pd.DataFrame(
    provenance_rows
)


st.dataframe(
    provenance_table,
    hide_index=True,
    width="stretch",
)


# ---------------------------------------------------------
# Final methodology note
# ---------------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="system-note">
    The application consumes frozen CSV, JSON and serialized
    model artifacts produced by the validated notebook
    workflow. Streamlit is used as the presentation and
    interaction layer; application navigation does not
    reopen model training, feature selection or final
    holdout evaluation.
    </div>
    """,
    unsafe_allow_html=True,
)