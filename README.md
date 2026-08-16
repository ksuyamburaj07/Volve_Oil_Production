# Volve Oil Production Data Science Project

## Live Application

**[Open Volve Field Intelligence](https://volve-field-intelligence.streamlit.app/)**

Interactive Streamlit application for historical Volve producer-well monitoring, one-month-ahead forecasting, model reliability analysis, and operational decision-support exploration.



A portfolio-oriented data science project using the publicly available Volve field production dataset.



The project investigates oil well production behaviour, operational activity, produced fluids, water injection, production decline, and later machine learning-based forecasting.



\## Project Status



Work in progress.



Completed stages:



\- Dataset verification and structural audit

\- Daily and monthly production reconciliation

\- Production and injection well classification

\- Exploratory field-level production analysis

\- Individual producer well analysis

\- Operational activity and on-stream hour analysis

\- Oil productivity analysis

\- Water production and water-cut analysis

\- Gas-to-oil behaviour analysis

\- Water injection analysis



Machine learning modelling has not yet been selected or performed. The modelling objective will be determined from the results of the exploratory and decline-analysis stages.



\## Dataset



The project uses the Volve production dataset derived from Equinor's publicly released Volve field data.



The raw dataset is not stored in this Git repository.



Local raw files are kept under:



```text

data/raw/

Project Structure

Volve\_Oil\_Production/

├── app/

├── data/

│   ├── raw/

│   ├── interim/

│   └── processed/

├── docs/

├── models/

├── notebooks/

├── outputs/

├── src/

├── .gitignore

└── README.md

Notebooks

00 - Dataset Evidence and Structural Audit



Establishes the structure, reliability, operational roles, missing-value behaviour, and daily-to-monthly consistency of the dataset.



Important checks include:



Daily well-date uniqueness

Production and injection classification

Producer and injector profiles

Missingness by operational role

F-5 operational-role investigation

Daily-to-monthly numerical reconciliation

Active-day sensor availability

Audit findings and reproducibility outputs

01 - Exploratory Production and Well Behaviour Analysis



Investigates field and well-level production behaviour before selecting a machine learning problem.



Topics include:



Field production history

Producer well timelines

Active versus represented producers

Oil production versus operating time

Oil productivity by producer

Produced water and water cut

Gas-to-oil behaviour

Water injection behaviour

Current Analytical Direction



The exploratory analysis indicates that field-level production decline cannot be explained by operating time alone.



The long-history producer wells show declining production intensity, while produced-water behaviour changes substantially during field life. Well identity, operating history, temporal behaviour, fluid composition, and well life-cycle stage are therefore expected to be important in later modelling.



These findings will be investigated further before a final prediction target and machine learning model are selected.



Next Stage



The next stage of the project will focus on:



Production decline behaviour

Temporal patterns

Candidate forecasting targets

Feature suitability

Preparation for machine learning modelling

Tools



The project currently uses:



Python

pandas

NumPy

Matplotlib

JupyterLab

Git and GitHub



Additional modelling and deployment tools will be documented as the project develops.



Author



Suyambu Raj

