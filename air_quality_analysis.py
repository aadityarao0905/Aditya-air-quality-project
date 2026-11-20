"""
Project 4: Air Quality Insights Dashboard
Tasks 49-63 | Pandas, NumPy and Matplotlib

Run from this folder:
    pip install pandas numpy matplotlib
    python air_quality_analysis.py

PM2.5 categories in Task 57 are project-defined for this assignment, NOT official AQI categories:
    Low <= 30, Moderate 31-60, High 61-90, Very High > 90
Task 62 uses a project-selected threshold of PM2.5 > 60 (not an official health standard).
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "04_air_quality.csv"
OUT = BASE / "outputs"
CHARTS = BASE / "charts"
OUT.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)

# Task 49: Load and inspect dataset
df = pd.read_csv(DATA)
print("TASK 49 | Shape:", df.shape)
print(df.head())
print("\\nData types:\\n", df.dtypes)
print("\\nColumn names:", df.columns.tolist())

# Task 50: Identify missing values
missing = df.isna().sum()
print("\\nTASK 50 | Missing values:\\n", missing)

# Task 51: Handle missing PM2.5 values using city median imputation.
# Rationale: city median is less sensitive to extreme readings than mean;
# a global median fallback handles any city with all PM2.5 values missing.
df["PM25"] = pd.to_numeric(df["PM25"], errors="coerce")
df["PM25_Clean"] = df["PM25"].fillna(df.groupby("City")["PM25"].transform("median"))
df["PM25_Clean"] = df["PM25_Clean"].fillna(df["PM25"].median())
print("\\nTASK 51 | Missing PM2.5 before imputation:", missing.get("PM25", 0))
print("Missing PM2.5 after imputation:", df["PM25_Clean"].isna().sum())

# Task 52: Convert date and extract month
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Month"] = df["Date"].dt.month_name()
df["Month_Number"] = df["Date"].dt.month

# Task 53: Average, median and maximum PM2.5
pm25_stats = df["PM25_Clean"].agg(["mean", "median", "max"])
print("\\nTASK 53 | PM2.5 statistics:\\n", pm25_stats)
pm25_stats.to_csv(OUT / "pm25_overall_statistics.csv")

# Task 54: City ranking by average PM2.5
city_rank = df.groupby("City")["PM25_Clean"].mean().sort_values(ascending=False)
print("\\nTASK 54 | City ranking:\\n", city_rank)
city_rank.to_csv(OUT / "city_average_pm25_ranking.csv")

# Task 55: Dates with highest PM2.5 readings
high_dates = df.nlargest(20, "PM25_Clean")[["Date", "City", "PM25_Clean"]]
print("\\nTASK 55 | Top 20 high-reading records:\\n", high_dates)
high_dates.to_csv(OUT / "high_pm25_dates_top20.csv", index=False)

# Task 56: City-wise PM10 and PM2.5 comparison
city_comparison = df.groupby("City")[["PM25_Clean", "PM10"]].mean()
city_comparison = city_comparison.rename(columns={"PM25_Clean": "Average_PM25", "PM10": "Average_PM10"})
print("\\nTASK 56 | PM10 vs PM2.5:\\n", city_comparison)
city_comparison.to_csv(OUT / "city_pm25_pm10_comparison.csv")

# Task 57: Project-defined PM2.5 categories (not official AQI bands)
bins = [-np.inf, 30, 60, 90, np.inf]
labels = ["Low", "Moderate", "High", "Very High"]
df["PM25_Category"] = pd.cut(df["PM25_Clean"], bins=bins, labels=labels)
category_counts = df["PM25_Category"].value_counts().reindex(labels, fill_value=0)
print("\\nTASK 57 | Project-defined categories:\\n", category_counts)
category_counts.to_csv(OUT / "pm25_category_counts.csv")

# Task 58: Monthly average PM2.5 by city
monthly = df.groupby(["City", "Month_Number", "Month"])["PM25_Clean"].mean().reset_index(name="Average_PM25")
print("\\nTASK 58 | Monthly averages:\\n", monthly.head())
monthly.to_csv(OUT / "monthly_average_pm25_by_city.csv", index=False)

# Task 59: NumPy standard deviation and percentiles
values = df["PM25_Clean"].to_numpy()
std = np.std(values, ddof=1)  # sample standard deviation
percentiles = np.percentile(values, [25, 50, 75, 90, 95])
print("\\nTASK 59 | Sample standard deviation:", std)
print("Percentiles (25, 50, 75, 90, 95):", percentiles)
pd.Series(percentiles, index=["P25", "P50", "P75", "P90", "P95"]).to_csv(OUT / "pm25_percentiles.csv")

# Task 60: IQR outliers
q1, q3 = np.percentile(values, [25, 75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df["PM25_Clean"] < lower) | (df["PM25_Clean"] > upper)][["Date", "City", "PM25_Clean"]]
print("\\nTASK 60 | IQR bounds:", lower, upper, "| Outlier count:", len(outliers))
outliers.to_csv(OUT / "pm25_iqr_outliers.csv", index=False)

# Task 61: Correlation between temperature and PM2.5
correlation = df["Temperature_C"].corr(df["PM25_Clean"])
print("\\nTASK 61 | Temperature-PM2.5 correlation:", correlation)

# Task 62: Proportion above selected project threshold (PM2.5 > 60)
threshold = 60
above = (df["PM25_Clean"] > threshold).sum()
proportion = above / len(df) * 100
print(f"\\nTASK 62 | Above {threshold}: {above}/{len(df)} = {proportion:.2f}%")
pd.Series({"threshold": threshold, "count_above": above, "percent_above": proportion}).to_csv(OUT / "above_threshold_proportion.csv")

# Optional performance summary table
summary = df.groupby("City").agg(
    Records=("City", "size"),
    Average_PM25=("PM25_Clean", "mean"),
    Median_PM25=("PM25_Clean", "median"),
    Maximum_PM25=("PM25_Clean", "max"),
    Average_PM10=("PM10", "mean"),
    Average_Temperature=("Temperature_C", "mean")
).sort_values("Average_PM25", ascending=False)
summary.to_csv(OUT / "city_pollution_summary.csv")

# Charts
city_rank.plot(kind="bar", figsize=(8, 5), title="Average PM2.5 by City")
plt.ylabel("PM2.5"); plt.tight_layout(); plt.savefig(CHARTS / "city_pm25_ranking.png", dpi=150); plt.close()

monthly_pivot = monthly.pivot(index="Month_Number", columns="City", values="Average_PM25")
monthly_pivot.plot(figsize=(10, 5), title="Monthly Average PM2.5 by City")
plt.xlabel("Month number"); plt.ylabel("Average PM2.5"); plt.tight_layout()
plt.savefig(CHARTS / "monthly_pm25_by_city.png", dpi=150); plt.close()

city_comparison.plot(kind="bar", figsize=(8, 5), title="City-wise PM10 vs PM2.5")
plt.ylabel("Average reading"); plt.tight_layout(); plt.savefig(CHARTS / "pm10_vs_pm25_city.png", dpi=150); plt.close()

plt.figure(figsize=(8, 5)); plt.scatter(df["Temperature_C"], df["PM25_Clean"])
plt.title(f"Temperature vs PM2.5 (r={correlation:.2f})")
plt.xlabel("Temperature (°C)"); plt.ylabel("PM2.5")
plt.tight_layout(); plt.savefig(CHARTS / "temperature_pm25_correlation.png", dpi=150); plt.close()

category_counts.plot(kind="bar", figsize=(8, 5), title="Project-defined PM2.5 Categories")
plt.ylabel("Records"); plt.tight_layout(); plt.savefig(CHARTS / "pm25_categories.png", dpi=150); plt.close()

df["PM25_Clean"].hist(bins=25, figsize=(8, 5))
plt.title("PM2.5 Distribution"); plt.xlabel("PM2.5"); plt.ylabel("Frequency")
plt.tight_layout(); plt.savefig(CHARTS / "pm25_distribution.png", dpi=150); plt.close()

# Task 63: Data-supported recommendations to review and contextualize
highest_city = city_rank.index[0]
lowest_city = city_rank.index[-1]
recommendations = [
    f"Prioritize monitoring and pollution-source investigations in {highest_city}, the city with the highest average PM2.5 in this dataset.",
    "Use the monthly city summaries to target awareness campaigns and monitoring during months with elevated averages.",
    "Publish clear, practical air-quality awareness messages and encourage people to consult official local advisories during pollution episodes.",
    "Investigate local sources such as traffic, construction dust, industry and burning using additional data; this dataset alone cannot attribute pollution sources.",
    f"Maintain routine monitoring in {lowest_city} as well; a lower dataset average does not guarantee safe air or represent every neighbourhood."
]
with open(OUT / "recommendations.txt", "w", encoding="utf-8") as f:
    f.write("TASK 63 | PUBLIC-AWARENESS RECOMMENDATIONS\\n\\n")
    for i, item in enumerate(recommendations, 1):
        f.write(f"{i}. {item}\\n")

# Save cleaned copy and concise report
df.to_csv(OUT / "cleaned_air_quality.csv", index=False)
with open(OUT / "analysis_summary.txt", "w", encoding="utf-8") as f:
    f.write(f"Records: {len(df)}\\nMissing PM2.5 initially: {missing.get('PM25',0)}\\n")
    f.write(f"Average PM2.5: {pm25_stats['mean']:.2f}\\nMedian PM2.5: {pm25_stats['median']:.2f}\\nMaximum PM2.5: {pm25_stats['max']:.2f}\\n")
    f.write(f"Sample standard deviation: {std:.2f}\\nPercentiles 25/50/75/90/95: {percentiles}\\n")
    f.write(f"IQR outliers: {len(outliers)} (bounds {lower:.2f}, {upper:.2f})\\n")
    f.write(f"Temperature correlation: {correlation:.3f}\\n")
    f.write(f"Percent above project threshold {threshold}: {proportion:.2f}%\\n\\n")
    f.write("City ranking:\\n" + city_rank.to_string() + "\\n\\n")
    f.write("Recommendations:\\n" + "\\n".join(f"{i}. {r}" for i,r in enumerate(recommendations,1)))
print("\\nTASK 63 | Recommendations:")
for i, rec in enumerate(recommendations, 1): print(f"{i}. {rec}")
print("\\nFinished. See outputs/ and charts/.")
