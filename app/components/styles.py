import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        /* Main application width */
        .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* General typography */
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }

        h1 {
            font-weight: 650;
        }

        /* Reduce default Streamlit header space */
        header[data-testid="stHeader"] {
            background: transparent;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background: #171C24;
            border: 1px solid #2A303B;
            border-radius: 10px;
            padding: 16px 18px;
        }

        div[data-testid="stMetricLabel"] {
            color: #AAB2BF;
        }

        div[data-testid="stMetricValue"] {
            font-weight: 600;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            border-right: 1px solid #252B35;
        }

        /* Horizontal rule */
        hr {
            border-color: #252B35;
        }

        /* Small contextual labels */
        .section-label {
            color: #D9A441;
            font-size: 0.78rem;
            font-weight: 650;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .page-subtitle {
            color: #AAB2BF;
            font-size: 1rem;
            margin-top: -0.6rem;
            margin-bottom: 1.6rem;
        }

        .system-note {
            color: #8E97A5;
            font-size: 0.85rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )