# Volve Oil Production Data Science Project

## Live Application

**[Open Volve Field Intelligence](https://volve-field-intelligence.streamlit.app/)**

Interactive Streamlit application for historical Volve producer-well monitoring, one-month-ahead forecasting, model reliability analysis, and operational decision-support exploration.

---

## Project Overview

This repository contains an end-to-end data science case study using the publicly available Volve field production dataset derived from Equinor's released Volve data.

The project investigates historical oil-well production behaviour, operational activity, produced fluids, water injection, production decline, temporal forecasting, model reliability, and decision-support interpretation.

The complete workflow covers:

- dataset verification and structural auditing
- daily and monthly production reconciliation
- exploratory production analysis
- individual producer-well analysis
- decline and temporal feature engineering
- forecasting-target formulation
- machine-learning model development
- chronological validation
- benchmark comparison
- untouched final holdout evaluation
- operational monitoring analysis
- application integration
- Streamlit application development
- public deployment

The final application is a historical analytical and forecasting case study. It is not a live oil-field production system.

---

## Project Status

**Complete and publicly deployed.**

The analytical workflow, forecasting system, validation, application integration, documentation, Git workflow, and deployment have been completed.

### Completed Stages

1. Dataset Evidence and Structural Audit
2. Exploratory Production and Well Behaviour Analysis
3. Production Decline and Feature Analysis
4. Predictive Model Development and Validation
5. Operational Production Insights and Decision Support
6. Application Integration and Final System Validation
7. Streamlit Application Development
8. Public Deployment

---

## Dataset

The project uses Volve production data derived from Equinor's publicly released Volve field dataset.

The working dataset was obtained through the Kaggle dataset **Volve production data**, published by Albert Lamy Christian and derived from the Equinor Volve open dataset.

The raw dataset is intentionally **not stored in this Git repository**.

Local raw files are maintained under:

```text
data/raw/
```

The analytical workflow uses both daily and monthly well-level records and distinguishes production and injection activity rather than treating every well identically.

---

## Dataset Audit and Operational Roles

The initial structural audit was performed before exploratory analysis or modelling.

Important checks included:

- daily well-date uniqueness
- daily and monthly dataset structure
- missing-value behaviour
- producer and injector classification
- well operational-role investigation
- active-day sensor availability
- daily-to-monthly numerical reconciliation
- structural versus potentially problematic missing values

The analysis identified six producer wells and two injector wells within the wider production data, with **15/9-F-5** exhibiting mixed production and injection activity.

Structural missingness was preserved where appropriate rather than automatically replacing missing values with zero.

---

## Core Forecasting Wells

The final forecasting workflow focuses on five core producer wells:

- 15/9-F-1 C
- 15/9-F-11
- 15/9-F-12
- 15/9-F-14
- 15/9-F-15 D

The application contains:

```text
295 valid historical forecast-origin records
5 core producer wells
80 final-holdout forecasts
```

The 295 application-history records represent **valid forecasting origins**, not the complete raw monthly field history.

---

## Forecasting Objective

The final forecasting problem is:

> Using information available up to and including producer-well month t, predict the oil production volume of the same well in month t+1.

### Forecast Horizon

**One month ahead**

The target is:

```text
Next-month monthly oil volume
```

Future information from the target month is not permitted as model input.

Random train-test splitting was avoided because the observations have a temporal ordering.

---

## Feature Engineering

Feature engineering was performed chronologically at producer-well level.

The modelling workflow uses information derived from:

- producer-well identity
- production age
- current production behaviour
- current operational activity
- historical oil-production lags
- recent rolling production behaviour
- production-intensity information
- historical fluid-behaviour information

The final serialized forecasting pipeline contains:

```text
10 numeric input features
1 categorical input feature
11 total input columns
```

Temporal continuity was checked before forecasting features were created.

No producer-well gaps greater than one calendar month were found in the core monthly histories used to formulate the forecasting problem.

---

## Model Development

Several candidate modelling approaches were considered during development.

The final selected machine-learning model was:

**Ridge Regression**

with:

```text
alpha = 10
```

Ridge Regression was selected during the development stage before the untouched final holdout was examined.

The fitted preprocessing and forecasting workflow was serialized as a scikit-learn Pipeline:

```text
models/ridge_next_month_oil_forecast_pipeline.joblib
```

---

## Persistence Benchmark

The machine-learning model was evaluated against a simple forecasting benchmark:

**Naive Persistence**

Persistence assumes:

> Next month's oil production volume will equal the current month's oil production volume.

This benchmark is intentionally simple, but it is highly relevant for a one-step-ahead production forecasting problem.

A machine-learning model should provide evidence that it improves upon such a baseline rather than being considered successful solely because it is more complex.

---

## Validation Strategy

The project uses **temporal validation**.

The validation design includes:

- chronological observation ordering
- expanding-window validation during development
- a separate final temporal holdout
- no random train-test split
- no model reselection after examining the final holdout
- no post-holdout retuning

The final holdout contains:

```text
Forecast records:        80
Producer wells:          5
Forecast-origin period:  April 2015 - August 2016
Target period:           May 2015 - September 2016
```

The final holdout was examined only after model development and selection were complete.

---

## Final Holdout Results

### Pooled Performance

| Metric | Persistence | Ridge Regression | Better Result |
|---|---:|---:|---|
| MAE | 1,786.68 | 3,370.28 | Persistence |
| RMSE | 2,896.88 | 4,577.99 | Persistence |
| R² | 0.9379 | 0.8448 | Persistence |
| WAPE | 17.55% | 33.10% | Persistence |

Persistence produced the stronger overall result on the untouched final holdout.

It achieved:

- lower MAE
- lower RMSE
- lower WAPE
- higher R²

The Ridge model is nevertheless retained as the frozen selected machine-learning model because it was selected before the final holdout was examined.

The project does **not** retrospectively choose another model after observing the final test result.

---

## Per-Well Reliability

Persistence also produced lower WAPE than Ridge Regression for each of the five core producer wells on the final holdout.

| Well | Persistence WAPE | Ridge WAPE |
|---|---:|---:|
| F-1 C | 44.16% | 58.56% |
| F-11 | 13.63% | 18.57% |
| F-12 | 15.20% | 15.99% |
| F-14 | 15.43% | 95.82% |
| F-15 D | 37.35% | 102.12% |

This demonstrates that the stronger pooled Persistence result was not driven by only one producer well.

---

## Negative Ridge Forecasts

The unconstrained Ridge Regression model generated:

```text
12 negative forecasts
out of 80 final-holdout forecasts
```

Negative oil-volume predictions are physically implausible.

They were deliberately **not retrospectively clipped to zero** because doing so would modify the behaviour of the already frozen model after evaluation.

The application exposes these cases transparently as part of the model-reliability analysis.

---

## Main Forecasting Finding

One of the most important results of the project is that a more sophisticated machine-learning model did not automatically outperform a simple benchmark.

> On the final untouched holdout, Naive Persistence generalized better than the selected Ridge Regression model.

This result is retained rather than hidden or replaced.

It highlights the importance of:

- meaningful baselines
- temporal validation
- untouched final test data
- transparent model limitations
- separating model complexity from actual predictive improvement

---

## Exploratory and Operational Analysis

Before forecasting, the project investigates historical Volve field and well behaviour.

The analytical workflow includes:

- field production history
- producer-well timelines
- active versus represented producers
- oil production behaviour
- production decline
- production age
- on-stream activity
- oil production intensity
- produced-water behaviour
- water cut
- gas-to-oil behaviour
- water injection
- zero-production periods
- recent production direction

These indicators are interpreted descriptively.

Observed relationships do not establish operational causation.

---

## Zero-Production and Structural Missingness

Zero-production and zero-on-stream months are preserved as meaningful operational states.

When on-stream hours are zero, variables such as:

- oil production per on-stream hour
- water cut in some records
- gas-to-oil ratio in some records

may be structurally undefined.

These cases are preserved as missing where appropriate rather than being automatically converted to zero.

The application also distinguishes recorded zero-hour months from missing observations in its visualizations.

---

## Volve Field Intelligence

The completed project includes a multi-page Streamlit application.

**Live application:**

https://volve-field-intelligence.streamlit.app/

### Field Overview

Provides a field-level view of the five core producer wells, including:

- historical producer oil-volume behaviour
- latest available producer conditions
- recent production comparison
- producer-status summaries

Latest monitoring observations are evaluated separately for each producer well and are not assumed to represent a single synchronous field date.

---

### Well Monitor

Allows an individual producer well to be selected and examined through:

- oil-production history
- recent production behaviour
- production intensity
- water cut
- on-stream hours
- current monitoring context
- historical forecasting reliability

Recorded zero-hour months are explicitly marked so they cannot be confused with missing observations.

---

### Forecast Analysis

Allows historical final-holdout forecast events to be examined interactively.

For each selected forecasting event, the application displays:

- forecast origin
- target month
- current oil volume
- Persistence forecast
- Ridge Regression forecast
- observed next-month oil volume
- forecast errors
- operational context
- well-level reliability information

Negative Ridge predictions remain visible and are not clipped.

---

### Model Reliability

Provides the final model-evaluation evidence, including:

- pooled holdout metrics
- Persistence versus Ridge comparison
- per-well WAPE
- negative Ridge forecast incidence
- final evaluation interpretation

---

### Methodology and Limitations

Documents:

- forecasting target
- one-month-ahead horizon
- model scope
- benchmark definition
- temporal validation strategy
- final holdout
- application boundaries
- model limitations
- analytical provenance

---

## Application Data

The application consumes frozen outputs produced during the analytical workflow.

Main deployment artifacts include:

```text
outputs/05_application_integration/
├── app_forecast_comparison.csv
├── app_historical_production.csv
├── app_limitations.csv
├── app_metadata.json
├── app_well_monitoring.csv
└── application_implementation_manifest.json
```

The application does not retrain or retune the forecasting model during normal use.

---

## Project Structure

```text
Volve_Oil_Production/
│
├── .streamlit/
│   └── config.toml
│
├── app/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   ├── data.py
│   │   └── styles.py
│   │
│   ├── pages/
│   │   ├── field_overview.py
│   │   ├── forecast_analysis.py
│   │   ├── methodology.py
│   │   ├── model_reliability.py
│   │   └── well_monitor.py
│   │
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── docs/
│
├── models/
│   └── ridge_next_month_oil_forecast_pipeline.joblib
│
├── notebooks/
│   ├── 00_Dataset_Evidence_and_Structural_Audit.ipynb
│   ├── 01_Exploratory_Production_and_Well_Behaviour_Analysis.ipynb
│   ├── 02_Production_Decline_and_Feature_Analysis.ipynb
│   ├── 03_Predictive_Model_Development_and_Validation.ipynb
│   ├── 04_Operational_Production_Insights_and_Decision_Support.ipynb
│   └── 05_Application_Integration_and_Final_System_Validation.ipynb
│
├── outputs/
│   └── 05_application_integration/
│
├── src/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Analytical Notebooks

### 00 - Dataset Evidence and Structural Audit

Establishes the structure and reliability of the source data before analysis.

Major tasks include:

- structural inspection
- uniqueness checks
- producer and injector classification
- operational-role investigation
- missing-value analysis
- daily-to-monthly reconciliation
- reproducibility evidence

---

### 01 - Exploratory Production and Well Behaviour Analysis

Investigates historical field and well-level production behaviour.

Major topics include:

- field production history
- producer timelines
- oil production
- operating activity
- production intensity
- produced water
- water cut
- gas-to-oil behaviour
- water injection

---

### 02 - Production Decline and Feature Analysis

Develops the temporal forecasting formulation.

Major tasks include:

- production decline analysis
- production-age calculation
- monthly continuity verification
- lag-feature creation
- rolling-feature creation
- forecasting-target comparison
- next-month target construction
- model-ready dataset preparation

The final target selected is next-month monthly oil volume.

---

### 03 - Predictive Model Development and Validation

Performs forecasting model development and evaluation.

Major tasks include:

- chronological development design
- Persistence benchmarking
- machine-learning development
- Ridge Regression selection
- expanding-window validation
- untouched final holdout evaluation
- pooled reliability analysis
- per-well reliability analysis

---

### 04 - Operational Production Insights and Decision Support

Transforms analytical results into monitoring-oriented outputs.

Major tasks include:

- latest producer conditions
- production direction
- recent production behaviour
- zero-production states
- operational context
- forecasting-reliability summaries
- decision-support-oriented outputs

No causal operational claims are made from descriptive associations.

---

### 05 - Application Integration and Final System Validation

Prepares the frozen analytical outputs for application use.

Major tasks include:

- application dataset creation
- saved-model reproducibility verification
- application metadata
- limitation documentation
- implementation manifest
- application-readiness checks

No model training, model selection, or post-holdout tuning is performed in this notebook.

---

## Technologies

The completed project uses:

- Python
- pandas
- NumPy
- scikit-learn
- joblib
- Plotly
- Streamlit
- JupyterLab
- Git
- GitHub
- Streamlit Community Cloud

---

## Python Environment

The deployed application was prepared and locally validated using Python 3.12.

Core deployment dependencies are defined in:

```text
requirements.txt
```

The Streamlit application configuration is stored in:

```text
.streamlit/config.toml
```

---

## Running the Application Locally

Clone the repository and move into the project directory.

Install the application dependencies:

```bash
pip install -r requirements.txt
```

Launch Streamlit from the repository root:

```bash
streamlit run app/streamlit_app.py
```

The application loads the frozen historical application artifacts and serialized forecasting pipeline from the repository.

---

## Reproducibility

The repository separates the project into:

```text
raw data
    ↓
structural audit
    ↓
exploratory analysis
    ↓
decline and temporal feature engineering
    ↓
model development
    ↓
temporal validation
    ↓
operational analysis
    ↓
application integration
    ↓
Streamlit deployment
```

Notebook 05 verifies that the serialized Ridge Regression pipeline reproduces the previously generated predictions to numerical precision.

The deployed application consumes frozen analytical artifacts rather than training a model on application startup.

---

## Limitations

The project has several important limitations.

### Dataset Scale

The monthly forecasting dataset is relatively small and contains a limited number of independent producer-well histories.

### Generalization

The selected Ridge Regression model did not outperform the Persistence benchmark on the untouched final holdout.

### Negative Forecasts

The unconstrained Ridge model produced 12 negative final-holdout predictions.

### Zero-Production States

Zero-production and zero-on-stream months can make ratio-based variables structurally undefined.

### Historical Scope

The project uses historical Volve data and is not connected to a live production system.

### Operational Interpretation

Observed relationships involving production, water cut, gas-to-oil behaviour, on-stream hours, or injection should not be interpreted as proof of causation.

### Application Scope

The Streamlit application is an analytical and portfolio case study, not a production engineering control system.

### Decision Support

Application outputs should not be interpreted as engineering operating limits, automated field recommendations, or substitutes for domain-expert judgement.

---

## Data and Repository Scope

The raw Volve dataset is not redistributed through this repository.

The repository contains the analytical notebooks, application code, serialized forecasting pipeline, and project outputs required to demonstrate and reproduce the case-study workflow.

Users wishing to reproduce the project from the original source data should obtain the Volve dataset from its original public source.

---

## Public Application

### Volve Field Intelligence

**https://volve-field-intelligence.streamlit.app/**

The deployed application provides interactive access to the final historical monitoring, forecasting, and model-reliability workflow.

---

## Project Status

**Complete.**

The project has progressed from raw-data verification through exploratory analysis, forecasting, temporal validation, operational interpretation, application development, Git-based release management, and public deployment.

The repository is retained as a reproducible historical data-science case study and portfolio project.

---

## Author

**Suyambu Raj**

BSc (Hons) Computer Science