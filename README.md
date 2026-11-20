# Project 4: Air Quality Insights Dashboard

**Industry:** Environment / Smart Cities  
**Dataset:** `04_air_quality.csv` (600 observations, 7 columns)

## Business scenario
Analyze air-quality readings across cities and identify periods and locations with higher particulate pollution.

## Questions and tasks
This project completes assignment Tasks 49–63: data inspection, missing values, PM2.5 cleaning, datetime/month extraction, statistics, city rankings, high-reading dates, PM10 vs PM2.5, project-defined categories, monthly summaries, NumPy statistics and percentiles, IQR outliers, temperature correlation, proportion above a selected threshold, and recommendations.

## Tools
- Python
- Pandas
- NumPy
- Matplotlib

## Data cleaning
There are 15 missing PM2.5 readings. These are imputed with the median PM2.5 for the corresponding city; a dataset-wide median fallback is included if a city median is unavailable. Median imputation is chosen to be less sensitive to extreme readings. The original `PM25` column remains available and `PM25_Clean` stores the imputed values.

## Project-defined thresholds (not official AQI categories)
For Task 57, categories are defined for this project only:
- Low: PM2.5 <= 30
- Moderate: 31–60
- High: 61–90
- Very High: >90

Task 62 uses a selected analysis threshold of **PM2.5 > 60**. Neither these bands nor the selected threshold are represented as official standards.

## Run
1. Install dependencies: `pip install pandas numpy matplotlib`
2. Place the CSV in this folder (already included).
3. Run: `python air_quality_analysis.py`

Outputs are saved in `outputs/`; plots are saved in `charts/`.

## Limitations
The dataset does not identify pollution sources or establish causality. Correlation does not imply causation. Imputed values are included in the analysis; interpret results with that limitation in mind. Categories are simplified project labels, not health advice or official AQI classifications.
