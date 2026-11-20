# Project 4 — Air Quality Insights Dashboard: Results

## Dataset overview
- Records: **600**
- Columns: **7**
- Cities: **4** (Chandigarh, Delhi, Jaipur, Lucknow)
- Missing PM2.5 readings: **15**
- Missing values in other columns: **0**

## Missing-value approach
The 15 missing PM2.5 readings were filled with the city-specific median; a global median fallback is included. The original PM25 field is retained and `PM25_Clean` is used for analyses.

## Overall PM2.5 statistics
- Average: **82.61**
- Median: **82.25**
- Maximum: **192.30**
- Sample standard deviation: **35.27**
- Percentiles (25th, 50th, 75th, 90th, 95th): **60.17, 82.25, 105.33, 126.56, 142.18**

## City ranking (average PM2.5)
- **Chandigarh**: 84.19\n- **Jaipur**: 82.52\n- **Lucknow**: 82.24\n- **Delhi**: 81.58\n
Highest average in this dataset: **Chandigarh** (84.19). Lowest average: **Delhi** (81.58).

## PM10 vs PM2.5 (city averages)
- Chandigarh: PM2.5 **84.19**; PM10 **150.59**\n- Delhi: PM2.5 **81.58**; PM10 **152.77**\n- Jaipur: PM2.5 **82.52**; PM10 **141.82**\n- Lucknow: PM2.5 **82.24**; PM10 **144.40**\n
## Highest reading dates
The top 20 readings are listed in `outputs/high_pm25_dates_top20.csv`. Highest record: **2026-07-22**, city **Delhi**, reading **192.3**.

## Project-defined categories
- Low (<=30): **46**
- Moderate (31–60): **104**
- High (61–90): **215**
- Very High (>90): **235**

These simplified categories are assignment-specific and not official AQI classifications.

## Monthly overview
The highest monthly average across city/month groups was **99.61** in **December**. Detailed city/month data is in `outputs/monthly_average_pm25_by_city.csv`.

## IQR outliers
- Q1: **60.17**
- Q3: **105.33**
- IQR: **45.15**
- Lower bound: **-7.55**
- Upper bound: **173.05**
- Outlier count: **7**

Outlier records are in `outputs/pm25_iqr_outliers.csv`.

## Temperature correlation
Pearson correlation between temperature and cleaned PM2.5: **0.028**. This indicates a very weak linear association in this dataset; it does not establish causation.

## Proportion above selected threshold
Selected threshold: **PM2.5 > 60** (project-selected, not an official standard).  
Count: **450 of 600** records (**75.00%**).

## Five recommendations
1. Prioritize monitoring and pollution-source investigations in Chandigarh, which has the highest city-average PM2.5 in these data.
2. Use monthly summaries to focus awareness campaigns and monitoring on months with higher city-level averages.
3. Share clear public-awareness messages and direct people to official local advisories during pollution episodes.
4. Investigate potential sources such as traffic, construction dust, industry and burning with additional evidence; this dataset cannot attribute pollution sources.
5. Continue routine monitoring in Delhi and all cities; a lower average does not guarantee safe air or represent every neighbourhood.

## Limitations
This is an observational dataset. It does not prove causes, and imputation affects calculated results. Project categories are not official AQI or health guidance.
