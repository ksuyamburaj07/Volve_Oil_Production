import streamlit as st

from components.styles import apply_global_styles


st.set_page_config(
    page_title="Volve Production Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()


field_overview = st.Page(
    "pages/field_overview.py",
    title="Field Overview",
    icon=":material/dashboard:",
    default=True,
)

well_monitor = st.Page(
    "pages/well_monitor.py",
    title="Well Monitor",
    icon=":material/oil_barrel:",
)

forecast_analysis = st.Page(
    "pages/forecast_analysis.py",
    title="Forecast Analysis",
    icon=":material/query_stats:",
)

model_reliability = st.Page(
    "pages/model_reliability.py",
    title="Model Reliability",
    icon=":material/analytics:",
)

methodology = st.Page(
    "pages/methodology.py",
    title="Methodology & Limitations",
    icon=":material/science:",
)


with st.sidebar:
    st.markdown(
        """
        <div class="section-label">Volve Field</div>
        <h2 style="margin-top: 0;">Production Intelligence</h2>
        <p class="system-note">
        Historical production monitoring and one-month-ahead
        forecasting case study.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.divider()


navigation = st.navigation(
    {
        "Production": [
            field_overview,
            well_monitor,
        ],
        "Forecasting": [
            forecast_analysis,
            model_reliability,
        ],
        "Project": [
            methodology,
        ],
    }
)

navigation.run()