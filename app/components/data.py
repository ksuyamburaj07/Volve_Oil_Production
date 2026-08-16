from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

APPLICATION_DATA_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "05_application_integration"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "ridge_next_month_oil_forecast_pipeline.joblib"
)


@st.cache_data
def load_historical_production() -> pd.DataFrame:
    path = APPLICATION_DATA_DIR / "app_historical_production.csv"

    data = pd.read_csv(
        path,
        parse_dates=["DATE"],
    )

    return data.sort_values(
        ["NPD_WELL_BORE_NAME", "DATE"]
    ).reset_index(drop=True)


@st.cache_data
def load_forecast_comparison() -> pd.DataFrame:
    path = APPLICATION_DATA_DIR / "app_forecast_comparison.csv"

    data = pd.read_csv(
        path,
        parse_dates=["DATE", "target_month"],
    )

    return data.sort_values(
        ["NPD_WELL_BORE_NAME", "DATE"]
    ).reset_index(drop=True)


@st.cache_data
def load_well_monitoring() -> pd.DataFrame:
    path = APPLICATION_DATA_DIR / "app_well_monitoring.csv"

    data = pd.read_csv(
        path,
        parse_dates=["DATE"],
    )

    return data.sort_values(
        "NPD_WELL_BORE_NAME"
    ).reset_index(drop=True)


@st.cache_data
def load_limitations() -> pd.DataFrame:
    path = APPLICATION_DATA_DIR / "app_limitations.csv"
    return pd.read_csv(path)


@st.cache_data
def load_metadata() -> dict:
    path = APPLICATION_DATA_DIR / "app_metadata.json"

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_resource
def load_forecasting_pipeline():
    return joblib.load(MODEL_PATH)