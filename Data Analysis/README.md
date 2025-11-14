# Water Level Projection Analysis for Louisiana Coastal Cities

## Overview

This project predicts future water levels at Louisiana coastal monitoring stations to assess flood risk for coastal cities. The analysis uses an **optimized blended ensemble model** that combines station-specific historical trends with established scientific sea level rise rates to generate projections for 2030, 2035, 2040, 2045, and 2050.

---

## The Prediction Model: Blended Ensemble Model

### Model Type Classification

**Primary Classification:** Weighted Ensemble / Hybrid Model

**Sub-classifications:**
- Ensemble Model (combines multiple base models)
- Hybrid Model (combines statistical and physics-based components)
- Linear Regression Ensemble
- Time Series Forecasting Model

### Why This Model?

The blended ensemble model was selected after comprehensive evaluation of multiple approaches (linear, polynomial, exponential, random forest, and government baseline models). It outperformed all alternatives by:

1. **Balancing local observations with scientific consensus** - Uses station-specific trends while anchoring to established sea level rise rates
2. **Handling data limitations** - Adapts to stations with varying data quality and duration
3. **Providing robust uncertainty estimates** - Combines confidence intervals from multiple sources
4. **Maintaining physical plausibility** - Ensures projections align with established scientific understanding

---

## Model Architecture

The blended model is a **weighted ensemble** that combines two complementary approaches:

### Component 1: Linear Regression (Station-Specific Trend)

**Type:** Ordinary Least Squares (OLS) Linear Regression

**Purpose:** Captures the actual observed trend at each monitoring station

**How it works:**
- Fits a linear regression model: `water_level(t) = intercept + slope × t`
- Uses historical annual mean water levels from each station
- Calculates station-specific sea level rise rate (ft/year)
- Provides 95% confidence intervals using standard statistical methods

**Example rates observed:**
- Grand Isle: 0.0273 ft/year (8.33 mm/year) - 45 years of data
- New Canal Station: 0.0357 ft/year (10.88 mm/year) - 19 years of data
- Port Fourchon: 0.0438 ft/year (13.34 mm/year) - 21 years of data

**Weight in ensemble:** `(1 - weight_gov)` - typically 60-80%

### Component 2: Government Baseline Rate Model

**Type:** Physics-based / Constant Rate Model

**Purpose:** Incorporates the established scientific sea level rise rate for the region

**Government Baseline Rate:**
- **Rate:** 6.2 mm/year = 0.0203 ft/year
- **Uncertainty:** ±0.0032 ft/year (standard deviation)
- **Source:** Based on 1982-2024 monthly mean sea level data from NOAA
- **Period:** Represents long-term regional trend

**How it works:**
- Takes the last observed water level value
- Projects forward using: `prediction(t) = last_value + (t - last_year) × 0.0203`
- Provides confidence intervals based on rate uncertainty

**Weight in ensemble:** `weight_gov` - typically 20-40%

---

## Mathematical Formulation

### Core Model Equation

```
Prediction(t) = (1 - w) × Linear_Trend(t) + w × Government_Baseline(t)
```

Where:
- `w` = `weight_gov` (optimized hyperparameter, typically 0.2-0.4)
- `Linear_Trend(t)` = Station-specific linear regression prediction at time t
- `Government_Baseline(t)` = Last_observed_value + (t - last_year) × 0.0203 ft/year

### Detailed Calculation Steps

1. **Linear Trend Component:**
   ```
   Linear_Trend(t) = β₀ + β₁ × t
   ```
   Where β₁ is the station-specific rate (ft/year) estimated from historical data

2. **Government Baseline Component:**
   ```
   Government_Baseline(t) = y_last + (t - t_last) × 0.0203
   ```
   Where y_last is the last observed water level and t_last is the last observation year

3. **Blended Prediction:**
   ```
   Blended(t) = (1 - w) × Linear_Trend(t) + w × Government_Baseline(t)
   ```

### Confidence Interval Calculation

The model combines uncertainty from both components:

```
CI_range = √[(1-w)² × station_CI² + w² × gov_CI²]
```

Where:
- `station_CI` = Confidence interval from linear regression (accounts for data uncertainty)
- `gov_CI` = Confidence interval from government rate (accounts for rate uncertainty)

The final 95% confidence interval is:
```
CI_lower = Blended(t) - CI_range/2
CI_upper = Blended(t) + CI_range/2
```

---

## Hyperparameter Tuning

The model uses **automated hyperparameter tuning** to optimize the `weight_gov` parameter for each station.

### Tuning Process

1. **Data Splitting:**
   - **Training Set:** All data before 2015
   - **Validation Set:** Data from 2015 onwards
   - If insufficient validation data (< 5 years), uses default weights

2. **Search Strategy:**
   - Tests `weight_gov` values from 0.1 to 0.55 in steps of 0.05
   - Evaluates each weight using Root Mean Squared Error (RMSE) on validation set
   - Selects weight with minimum RMSE

3. **Optimization Metric:**
   ```
   RMSE = √[Σ(observed - predicted)² / n]
   ```
   Also tracks:
   - **MAE:** Mean Absolute Error
   - **R²:** Coefficient of Determination

4. **Fallback Strategy:**
   If validation data is insufficient:
   - **Short data periods** (<25 years): `weight_gov = 0.4` (more trust in government rate)
   - **Long data periods** (≥25 years): `weight_gov = 0.2` (more trust in station trend)

### Why This Tuning Matters

The optimal weight balances:
- **Station-specific trends** (may include local effects like subsidence)
- **Regional scientific consensus** (established sea level rise rate)

Stations with longer, higher-quality data get more weight on their observed trends. Stations with shorter histories rely more on the established scientific rate.

---

## Model Validation

### Validation Metrics

The model reports three key metrics during hyperparameter tuning:

1. **RMSE (Root Mean Squared Error):**
   - Measures average prediction error magnitude
   - Lower is better
   - Units: feet

2. **MAE (Mean Absolute Error):**
   - Average absolute difference between predictions and observations
   - More robust to outliers than RMSE
   - Units: feet

3. **R² (Coefficient of Determination):**
   - Proportion of variance explained by the model
   - Range: 0 to 1 (higher is better)
   - Values close to 1 indicate good fit

### Example Validation Output

```
--- Hyperparameter Tuning ---
  Best weight_gov: 0.250
  Validation RMSE: 0.0234 ft
  Validation MAE: 0.0198 ft
  Validation R²: 0.9876
```

---

## Model Advantages

1. **Robustness:** Combines data-driven (statistical) and physics-based approaches
2. **Adaptability:** Hyperparameter tuning adapts to each station's data quality and duration
3. **Uncertainty Quantification:** Provides comprehensive confidence intervals
4. **Physical Plausibility:** Incorporates established scientific sea level rise rates
5. **Station-Specific:** Captures local trends while maintaining regional consistency
6. **Handles Data Limitations:** Works well even with shorter data histories

---

## Model Limitations

1. **Assumes Linear Trends:** May not capture acceleration or deceleration in sea level rise
2. **Assumes Constant Government Rate:** Doesn't account for potential future rate changes
3. **Limited to Historical Patterns:** Extrapolates based on past trends, not future scenarios
4. **No External Factors:** Doesn't incorporate climate scenarios (RCP), storm surge, or extreme events
5. **No Subsidence Modeling:** Local subsidence effects may be captured in station trends but aren't explicitly separated

---

## Data Sources

The model uses historical water level data from three NOAA monitoring stations:

- **Grand Isle**: 1980-2025 (45 years of hourly data)
- **New Canal Station**: 2006-2024 (19 years of hourly data)
- **Port Fourchon**: 2004-2025 (21 years of hourly data)

### Data Preprocessing

Data cleaning and aggregation (brief overview):
- Raw CSV files are cleaned to handle missing values and format inconsistencies
- Hourly data is aggregated to annual means for trend analysis
- See `data_cleaning/` folder for preprocessing scripts

---

## Usage

### Run Complete Analysis Pipeline

```bash
python run_analysis.py
```

This executes the full pipeline:
1. Data aggregation (hourly → annual)
2. Trend analysis
3. Model projections with hyperparameter tuning
4. Flood risk assessment
5. Model validation and summary

### Run Individual Components

```bash
# Data preprocessing
python data_cleaning/aggregate_data.py

# Trend analysis
python models/trend_analysis.py

# Model projections (with hyperparameter tuning)
python models/projection_models.py

# Flood risk assessment
python models/flood_risk_assessment.py

# Model validation and summary
python models/compare_projections.py
```

---

## Output Files

All outputs are saved in the `output/` directory:

### Model Outputs

- **`water_level_projections.csv`** - Projections for all stations and years
  - Columns: station, year, model, prediction_ft, ci_lower_ft, ci_upper_ft, optimal_weight_gov
  
- **`best_model_projections.csv`** - Selected best model projections (same as above, all are blended model)

- **`trend_analysis_summary.csv`** - Historical trend analysis results

### Assessment Outputs

- **`flood_risk_assessment.csv`** - Detailed flood risk by city and year
- **`flood_risk_summary.csv`** - Summary table of city flood risks by year

### Reports and Visualizations

- **`final_report.txt`** - Comprehensive text report with projections
- **`trend_analysis.png`** - Historical trend visualizations
- **`model_comparison.png`** - Projection plots with confidence intervals

---

## Example Projections

### Grand Isle (45 years of data, weight_gov ≈ 0.2)
- **2030**: 0.925 ft (CI: 0.752 - 1.097 ft)
- **2035**: 1.054 ft (CI: 0.878 - 1.230 ft)
- **2040**: 1.184 ft (CI: 1.004 - 1.363 ft)
- **2045**: 1.313 ft (CI: 1.129 - 1.497 ft)
- **2050**: 1.443 ft (CI: 1.254 - 1.632 ft)

### New Canal Station (19 years of data, weight_gov ≈ 0.3-0.4)
- **2030**: 1.141 ft (CI: 0.966 - 1.316 ft)
- **2035**: 1.289 ft (CI: 1.095 - 1.483 ft)
- **2040**: 1.437 ft (CI: 1.220 - 1.653 ft)
- **2045**: 1.584 ft (CI: 1.343 - 1.825 ft)
- **2050**: 1.732 ft (CI: 1.465 - 2.000 ft)

### Port Fourchon (21 years of data, weight_gov ≈ 0.3-0.4)
- **2030**: 1.164 ft (CI: 0.992 - 1.336 ft)
- **2035**: 1.336 ft (CI: 1.150 - 1.523 ft)
- **2040**: 1.508 ft (CI: 1.304 - 1.712 ft)
- **2045**: 1.680 ft (CI: 1.457 - 1.904 ft)
- **2050**: 1.852 ft (CI: 1.607 - 2.097 ft)

---

## Project Structure

```
Data Analysis/
├── data/                          # Raw data files
│   ├── grandisle@data/           # Grand Isle station data
│   ├── New Canal Station/        # New Canal Station data
│   └── Port Fourchan/            # Port Fourchon station data
│
├── data_cleaning/                 # Data preprocessing modules
│   ├── clean_data.py             # Clean raw CSV files
│   └── aggregate_data.py          # Aggregate hourly to annual
│
├── models/                        # Model and analysis modules
│   ├── trend_analysis.py          # Trend analysis
│   ├── projection_models.py       # Blended ensemble model (main)
│   ├── compare_projections.py    # Model validation
│   └── flood_risk_assessment.py   # Flood risk assessment
│
├── output/                        # Generated outputs (CSV, PNG, TXT)
├── run_analysis.py                # Main pipeline script
└── README.md                      # This file
```

---

## Dependencies

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **scipy** - Statistical functions and confidence intervals
- **scikit-learn** - Linear regression model
- **matplotlib** - Visualizations

Install with:
```bash
pip install pandas numpy scipy scikit-learn matplotlib
```

---

## Key Considerations

1. **Relative vs Absolute Levels:** Projections are relative to the baseline period. Absolute sea level rise is incorporated through the government baseline rate.

2. **Uncertainty:** All projections include 95% confidence intervals. Wider intervals indicate higher uncertainty, often due to shorter data histories.

3. **Station Variability:** Different stations show different rates due to:
   - Local subsidence
   - Regional sea level rise variations
   - Data quality and duration differences

4. **Model Selection:** The blended model was selected after comprehensive evaluation. It provides the best balance of accuracy, physical plausibility, and uncertainty quantification.

---

## Future Enhancements

Potential improvements to the model:

1. **Non-linear Trends:** Incorporate acceleration/deceleration detection
2. **Climate Scenarios:** Integrate IPCC RCP scenarios (2.6, 4.5, 8.5)
3. **Subsidence Modeling:** Explicitly model and separate subsidence effects
4. **Extreme Events:** Include storm surge and extreme event modeling
5. **Ensemble Methods:** Combine multiple projection approaches with advanced weighting

---

## References

- **Government Baseline Rate:** NOAA sea level rise data (1982-2024), 6.2 mm/year
- **Monitoring Stations:** NOAA Tides & Currents
- **Model Methodology:** Weighted ensemble combining OLS regression with physics-based rate model

---

## License

See project license file.
