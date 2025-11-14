#!/usr/bin/env python3
"""
Optimized Blended Model for Long-term Water Level Projections (2030-2050).
This is an ensemble model that combines:
- Linear regression (station-specific trend)
- Government baseline rate (6.2 mm/year = 0.0203 ft/year)

Model Type: Weighted Ensemble / Hybrid Model
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy import stats
import os

# Government baseline rate: 6.2 mm/year = 0.0203 ft/year
GOVERNMENT_SLR_RATE_FT_YEAR = 0.0203
GOVERNMENT_SLR_RATE_FT_YEAR_STD = 0.0032

# Target years for projections
TARGET_YEARS = [2030, 2035, 2040, 2045, 2050]

def linear_model_predict(years_train, values_train, years_predict):
    """Linear regression model for station-specific trend."""
    X_train = years_train.reshape(-1, 1)
    X_predict = years_predict.reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X_train, values_train)
    
    predictions = model.predict(X_predict)
    
    # Calculate confidence intervals
    y_pred_train = model.predict(X_train)
    residuals = values_train - y_pred_train
    mse = np.mean(residuals**2)
    n = len(years_train)
    
    # Standard error for predictions
    X_mean = np.mean(X_train)
    Sxx = np.sum((X_train - X_mean)**2)
    se_pred = np.sqrt(mse * (1 + 1/n + (X_predict - X_mean)**2 / Sxx))
    
    # 95% confidence interval
    t_val = stats.t.ppf(0.975, n - 2)
    ci_lower = predictions - t_val * se_pred.flatten()
    ci_upper = predictions + t_val * se_pred.flatten()
    
    return {
        'predictions': predictions,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'model': model,
        'rate_ft_per_year': model.coef_[0]
    }

def government_baseline_model(years_train, values_train, years_predict):
    """Model using government baseline rate."""
    # Use last observed value as starting point
    last_value = values_train[-1]
    last_year = years_train[-1]
    
    # Calculate cumulative rise using government rate
    years_since_last = years_predict - last_year
    cumulative_rise = GOVERNMENT_SLR_RATE_FT_YEAR * years_since_last
    
    predictions = last_value + cumulative_rise
    
    # Confidence intervals based on government rate uncertainty
    cumulative_std = GOVERNMENT_SLR_RATE_FT_YEAR_STD * np.abs(years_since_last)
    ci_lower = predictions - 1.96 * cumulative_std
    ci_upper = predictions + 1.96 * cumulative_std
    
    return {
        'predictions': predictions,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'model': {'type': 'government_baseline', 'rate': GOVERNMENT_SLR_RATE_FT_YEAR}
    }

def blend_models_with_government_rate(station_result, years_train, values_train, years_predict, 
                                     weight_gov=0.3):
    """Blend station-specific trend with government baseline rate."""
    # Get station trend
    station_trend = station_result['linear']['predictions']
    
    # Get government baseline
    gov_result = government_baseline_model(years_train, values_train, years_predict)
    gov_trend = gov_result['predictions']
    
    # Weighted blend
    blended = (1 - weight_gov) * station_trend + weight_gov * gov_trend
    
    # Combine confidence intervals
    station_ci_range = station_result['linear']['ci_upper'] - station_result['linear']['ci_lower']
    gov_ci_range = gov_result['ci_upper'] - gov_result['ci_lower']
    combined_ci_range = np.sqrt((1 - weight_gov)**2 * station_ci_range**2 + 
                                weight_gov**2 * gov_ci_range**2)
    
    ci_lower = blended - combined_ci_range / 2
    ci_upper = blended + combined_ci_range / 2
    
    return {
        'predictions': blended,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'weight_gov': weight_gov
    }

def tune_blended_model_weight(years_train, values_train, holdout_start_year=2015):
    """
    Tune the weight_gov hyperparameter using holdout validation.
    
    Args:
        years_train: Training years
        values_train: Training values
        holdout_start_year: Year to start holdout validation
        
    Returns:
        Best weight_gov value and validation metrics
    """
    # Split data into train and validation sets
    mask = years_train < holdout_start_year
    years_train_split = years_train[mask]
    values_train_split = values_train[mask]
    years_val = years_train[~mask]
    values_val = values_train[~mask]
    
    if len(years_val) == 0:
        print(f"  Not enough data for tuning (holdout starts at {holdout_start_year})")
        # Return default based on data length
        if len(years_train) < 25:
            return 0.4, None
        else:
            return 0.2, None
    
    # Convert to years since start for modeling
    years_train_relative = years_train_split - years_train_split.min()
    years_val_relative = years_val - years_train_split.min()
    
    # Get linear model predictions for validation
    linear_result = linear_model_predict(years_train_relative, values_train_split, years_val_relative)
    
    # Get government baseline predictions for validation
    gov_result = government_baseline_model(years_train_split, values_train_split, years_val)
    
    # Test different weight values
    weight_candidates = np.arange(0.1, 0.6, 0.05)  # Test weights from 0.1 to 0.55
    best_weight = 0.3
    best_rmse = float('inf')
    best_metrics = None
    
    results = []
    
    for weight_gov in weight_candidates:
        # Blend predictions
        blended_preds = (1 - weight_gov) * linear_result['predictions'] + weight_gov * gov_result['predictions']
        
        # Calculate metrics
        rmse = np.sqrt(mean_squared_error(values_val, blended_preds))
        mae = mean_absolute_error(values_val, blended_preds)
        r2 = r2_score(values_val, blended_preds)
        
        results.append({
            'weight_gov': weight_gov,
            'rmse': rmse,
            'mae': mae,
            'r2': r2
        })
        
        if rmse < best_rmse:
            best_rmse = rmse
            best_weight = weight_gov
            best_metrics = {'rmse': rmse, 'mae': mae, 'r2': r2}
    
    return best_weight, best_metrics

def project_station(station_name, annual_data, tune_hyperparameters=True):
    """
    Generate projections for a station using the optimized blended model.
    
    Args:
        station_name: Name of the station
        annual_data: DataFrame with annual water level data
        tune_hyperparameters: If True, tune weight_gov using validation data
    """
    print(f"\n{'='*60}")
    print(f"Projections for {station_name}")
    print(f"{'='*60}")
    
    years = annual_data['years_since_start'].values
    values = annual_data['mean_ft'].values
    actual_years = annual_data['year'].values
    
    # For projection, use years since start of data period
    last_year = actual_years.max()
    years_since_last = TARGET_YEARS - last_year
    
    # Convert target years to years since start
    years_predict = years.max() + years_since_last
    
    print(f"Training period: {actual_years.min()} to {actual_years.max()}")
    print(f"Projection years: {TARGET_YEARS}")
    
    # Get linear model for station trend
    linear_result = linear_model_predict(years, values, years_predict)
    print(f"\nStation Linear Trend: {linear_result['rate_ft_per_year']:.4f} ft/year")
    
    # Tune hyperparameter if requested
    if tune_hyperparameters:
        print("\n--- Hyperparameter Tuning ---")
        best_weight, metrics = tune_blended_model_weight(actual_years, values)
        if metrics:
            print(f"  Best weight_gov: {best_weight:.3f}")
            print(f"  Validation RMSE: {metrics['rmse']:.4f} ft")
            print(f"  Validation MAE: {metrics['mae']:.4f} ft")
            print(f"  Validation R²: {metrics['r2']:.4f}")
        else:
            # Use default based on data length
            if len(years) < 25:
                best_weight = 0.4
            else:
                best_weight = 0.2
            print(f"  Using default weight_gov: {best_weight:.3f} (insufficient data for tuning)")
    else:
        # Use default based on data length
        if len(years) < 25:
            best_weight = 0.4
        else:
            best_weight = 0.2
        print(f"\nUsing default weight_gov: {best_weight:.3f}")
    
    # Create blended model result
    results = {'linear': linear_result}
    blended_result = blend_models_with_government_rate(results, years, values, years_predict, best_weight)
    
    print(f"\n--- Blended Model (Ensemble) ---")
    print(f"  Government weight: {best_weight:.1%}")
    print(f"  Station weight: {1-best_weight:.1%}")
    
    # Store results
    results['blended'] = blended_result
    results['station'] = station_name
    results['train_years'] = actual_years
    results['train_values'] = values
    results['target_years'] = TARGET_YEARS
    results['optimal_weight_gov'] = best_weight
    
    return results

def save_projections(all_results, output_dir='output'):
    """Save projection results to CSV."""
    os.makedirs(output_dir, exist_ok=True)
    
    projection_data = []
    
    for result in all_results:
        station = result['station']
        target_years = result['target_years']
        
        # Only save blended model results
        if 'blended' in result:
            pred_result = result['blended']
            for i, year in enumerate(target_years):
                projection_data.append({
                    'station': station,
                    'year': year,
                    'model': 'blended',
                    'prediction_ft': pred_result['predictions'][i],
                    'ci_lower_ft': pred_result['ci_lower'][i],
                    'ci_upper_ft': pred_result['ci_upper'][i],
                    'optimal_weight_gov': pred_result['weight_gov']
                })
    
    df = pd.DataFrame(projection_data)
    output_file = os.path.join(output_dir, 'water_level_projections.csv')
    df.to_csv(output_file, index=False)
    print(f"\n[OK] Projections saved to: {output_file}")
    
    return df

def main():
    """Main function to generate projections."""
    print("=" * 60)
    print("Long-Term Water Level Projections (2030-2050)")
    print("Using Optimized Blended Ensemble Model")
    print("=" * 60)
    
    # Load annual data
    annual_file = 'output/annual_water_levels.csv'
    if not os.path.exists(annual_file):
        print(f"Error: {annual_file} not found!")
        print("Please run aggregate_data.py first.")
        return
    
    annual_data = pd.read_csv(annual_file)
    
    # Generate projections for each station
    stations = annual_data['station'].unique()
    all_results = []
    
    for station in stations:
        station_data = annual_data[annual_data['station'] == station].copy()
        result = project_station(station, station_data, tune_hyperparameters=True)
        all_results.append(result)
    
    # Save projections
    projection_df = save_projections(all_results)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Projection Summary")
    print("=" * 60)
    
    for result in all_results:
        station = result['station']
        print(f"\n{station}:")
        print(f"  {'Year':<10} {'Prediction (ft)':<20} {'95% CI (ft)':<30}")
        print(f"  {'-'*10} {'-'*20} {'-'*30}")
        
        blended = result['blended']
        for i, year in enumerate(result['target_years']):
            pred = blended['predictions'][i]
            ci_low = blended['ci_lower'][i]
            ci_high = blended['ci_upper'][i]
            print(f"  {year:<10} {pred:>8.3f}{'':10} [{ci_low:>6.3f}, {ci_high:>6.3f}]")
    
    print("\n" + "=" * 60)
    print("Model Type: Weighted Ensemble / Hybrid Model")
    print("Components:")
    print("  1. Linear Regression (station-specific trend)")
    print("  2. Government Baseline Rate (6.2 mm/year)")
    print("  Combined using optimized weight hyperparameter")
    print("=" * 60)

if __name__ == "__main__":
    main()
