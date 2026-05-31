# Predictive Student At-Risk Engine: Behavioral Analytics Dashboard

An end-to-end data pipeline moving from a massive MySQL data warehouse to a Python Machine Learning engine, culminating in a single-pane Power BI operational dashboard that predicts student dropouts based on early-term digital engagement.

## 1. Project Overview
A fully integrated data product that extracts and chunks 10.6 million rows of raw behavioral logs into a relational MySQL database, engineers complex predictive features using Python, and deploys an XGBoost Machine Learning model to evaluate student risk. The system outputs to a dynamic, single-pane-of-glass Power BI dashboard, enabling academic advisors to identify and intervene with at-risk students weeks before midterms.

## 2. Purpose
In the education sector, relying on reactive, end-of-semester grade reports means intervention happens too late. The purpose of this project is to replace static descriptive reporting with a proactive, automated predictive engine. It allows non-technical academic staff to explore massive datasets of digital body language (VLE clicks) and instantly export a prioritized, 3-tier triage roster to focus their support efforts where they are needed most. 

## 3. Tech Stack
The backend pipeline, predictive engine, and visual interface were built using the following tools:
* **MySQL & SQLAlchemy:** Architected a relational database to securely ingest and store 10.6 million records of student clickstream data without memory crashing.
* **Python (`pandas`, `scikit-learn`, `xgboost`):** Engineered custom behavioral features (momentum trends, activity diversity) and trained an XGBoost classification algorithm to achieve **90.72% accuracy** in predicting student outcomes based solely on the first 28 days of class.
* **Power BI:** The visualization layer connected to the ML output, designed as a single-pane-of-glass operational tool for immediate stakeholder use.

## 4. Data Source
The project utilizes the public **Open University Learning Analytics Dataset (OULAD)**, which contains demographic, assessment, and daily interaction data for massive open online courses. 
* **Source:** https://analyse.kmi.open.ac.uk/open-dataset
* *Note: A `sample_predictions.csv` file is included in the `/data` folder to demonstrate the custom output schema.*

## 5. Features

### Business Problem
University dropouts represent a massive loss in both revenue and human potential. Academic advisors struggle to quickly identify failing students because early warning signs are buried in millions of rows of digital platform logs. Standard dashboards only show what has already happened, leaving advisors reacting to failure rather than preventing it.

### Goal of the Project
* **Proactive Analytics:** Build a machine learning early warning system that evaluates just the first 4 weeks of data to predict final academic outcomes with over 90% accuracy.
* **Actionable Output:** Translate raw AI probabilities into a custom 3-tier triage system (High Risk 🔴, Monitor 🟡, Safe 🟢) so advisors know exactly who to call on a Tuesday morning.

### Walkthrough of Key Modules
* **The Engagement Cliff:** Visualizes the massive drop-off in platform clicks that failing students exhibit weeks in advance of withdrawing.
* **AI Triage Roster:** A direct output table from the XGBoost model, allowing advisors to filter by department and immediately export a targeted list of students needing intervention.
* **Demographic Multipliers:** Explores the baseline risk factors, such as how previous academic attempts significantly multiply the risk of failure when combined with low platform engagement.

## 6. Business Impact & Insights
* **Targeted Resource Allocation:** By engineering a custom 3-tier evaluation system, the dashboard filters out the noise and directs academic advising resources exactly where they are mathematically proven to be needed.
* **The 150-Click Threshold:** The data revealed a critical behavioral insight: students who eventually fail or withdraw frequently log fewer than 150 total interactions in their early weeks, acting as a massive leading indicator of academic success.
* **Operational Efficiency:** Transitioning from an overwhelming 10.6 million row dataset to a single-pane operational dashboard saves hours of manual reporting, providing stakeholders with an immediate, clear strategy for student retention.

## 7. Dashboard Demo

**[Click Here to Interact with the Live Power BI Dashboard](https://app.powerbi.com/view?r=eyJrIjoiODZhOTk5Y2MtZDk5NC00NzY1LWJiYjgtMjc0ZGMwZGI0ZjM3IiwidCI6IjhlMjQ0OTAwLWJiZDQtNGNlMC1iNzlhLTQ4ZTMwYWRjMDFkNyJ9)**

*(If the live link is unavailable, view the automated system demonstration below)*

![Dashboard Demo](https://github.com/chinmai-budati/Student-Performace-Analysis/blob/main/Demo.gif)
