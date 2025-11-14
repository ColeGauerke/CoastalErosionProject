#!/usr/bin/env python3
"""
Statistical trend analysis for water level data.
Detects linear, quadratic, exponential patterns and calculates rates of change.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import os

# Government baseline rate: 6.2 mm/year = 0.0203 ft/year
GOVERNMENT_SLR_RATE_FT_YEAR = 0.0203
GOVERNMENT_SLR_RATE_FT_YEAR_STD = 0.0032  # 0.97 mm/year = 0.0032 ft/year

def linear_trend(x, a, b):
    """Linear model: y = a + b*x"""
    return a + b * x

def quadratic_trend(x, a, b, c):
    """Quadratic model: y = a + b*x + c*x^2"""
    return a + b * x + c * x**2

def exponential_trend(x, a, b):
    """Exponential model: y = a * exp(b*x)"""
    return a * np.exp(b * x)

def calculate_linear_rate(years, values):
    """Calculate linear rate of change using least squares."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(years, values)
    return {
        'slope_ft_per_year': slope,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
        'std_err': std_err,
        'rate_mm_per_year': slope * 304.8  # Convert feet to mm
    }

def calculate_polynomial_fit(years, values, degree=2):
    """Fit polynomial model and return coefficients."""
    coeffs = np.polyfit(years, values, degree)
    poly = np.poly1d(coeffs)
    
    # Calculate R-squared
    y_pred = poly(years)
    ss_res = np.sum((values - y_pred) ** 2)
    ss_tot = np.sum((values - np.mean(values)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    
    return {
        'coefficients': coeffs,
        'polynomial': poly,
        'r_squared': r_squared,
        'degree': degree
    }

def detect_acceleration(years, values):
    """Detect if sea level rise is accelerating."""
    results = {}
    
    # Linear trend
    linear_result = calculate_linear_rate(years, values)
    results['linear'] = linear_result
    
    # Quadratic trend (detects acceleration)
    quad_result = calculate_polynomial_fit(years, values, degree=2)
    results['quadratic'] = quad_result
    
    # Compare linear vs quadratic
    # If quadratic has significantly better fit, there's acceleration
    improvement = quad_result['r_squared'] - linear_result['r_squared']
    
    # Extract acceleration coefficient (coefficient of x^2)
    acceleration_coeff = quad_result['coefficients'][0]  # Highest degree coefficient
    
    results['acceleration_detected'] = improvement > 0.01  # Threshold for significant improvement
    results['acceleration_coefficient'] = acceleration_coeff
    
    return results

def calculate_decadal_rates(years, values):
    """Calculate rate of change for each decade."""
    df = pd.DataFrame({'year': years, 'value': values})
    df['decade'] = (df['year'] // 10) * 10
    
    decadal_rates = []
    for decade in sorted(df['decade'].unique()):
        decade_data = df[df['decade'] == decade]
        if len(decade_data) >= 3:  # Need at least 3 years
            decade_years = decade_data['year'].values
            decade_values = decade_data['value'].values
            rate = calculate_linear_rate(decade_years, decade_values)
            rate['decade'] = int(decade)
            rate['num_years'] = len(decade_data)
            decadal_rates.append(rate)
    
    return decadal_rates

def compare_with_government_rate(calculated_rate, std_err):
    """Compare calculated rate with government baseline rate."""
    diff = calculated_rate - GOVERNMENT_SLR_RATE_FT_YEAR
    std_diff = np.sqrt(std_err**2 + GOVERNMENT_SLR_RATE_FT_YEAR_STD**2)
    z_score = diff / std_diff if std_diff > 0 else 0
    
    return {
        'calculated_rate_ft_per_year': calculated_rate,
        'government_rate_ft_per_year': GOVERNMENT_SLR_RATE_FT_YEAR,
        'difference_ft_per_year': diff,
        'z_score': z_score,
        'within_confidence_interval': abs(diff) < 2 * std_diff  # 95% CI
    }

def analyze_station(station_name, annual_data):
    """Perform comprehensive trend analysis for a station."""
    print(f"\n{'='*60}")
    print(f"Trend Analysis: {station_name}")
    print(f"{'='*60}")
    
    years = annual_data['years_since_start'].values
    values = annual_data['mean_ft'].values
    actual_years = annual_data['year'].values
    
    print(f"\nData Period: {actual_years.min()} to {actual_years.max()} ({len(years)} years)")
    print(f"Mean water level range: {values.min():.2f} to {values.max():.2f} ft")
    
    # Linear trend analysis
    print(f"\n--- Linear Trend Analysis ---")
    linear_result = calculate_linear_rate(years, values)
    print(f"Rate of change: {linear_result['slope_ft_per_year']:.4f} ft/year")
    print(f"  = {linear_result['rate_mm_per_year']:.2f} mm/year")
    print(f"R-squared: {linear_result['r_squared']:.4f}")
    print(f"P-value: {linear_result['p_value']:.6f}")
    print(f"Standard error: {linear_result['std_err']:.4f} ft/year")
    
    # Compare with government rate
    print(f"\n--- Comparison with Government Baseline Rate ---")
    gov_comparison = compare_with_government_rate(
        linear_result['slope_ft_per_year'], 
        linear_result['std_err']
    )
    print(f"Government rate: {gov_comparison['government_rate_ft_per_year']:.4f} ft/year")
    print(f"Calculated rate: {gov_comparison['calculated_rate_ft_per_year']:.4f} ft/year")
    print(f"Difference: {gov_comparison['difference_ft_per_year']:.4f} ft/year")
    if gov_comparison['within_confidence_interval']:
        print("Status: Within government confidence interval")
    else:
        print("Status: Outside government confidence interval")
    
    # Acceleration detection
    print(f"\n--- Acceleration Detection ---")
    accel_result = detect_acceleration(years, values)
    print(f"Linear R-squared: {accel_result['linear']['r_squared']:.4f}")
    print(f"Quadratic R-squared: {accel_result['quadratic']['r_squared']:.4f}")
    if accel_result['acceleration_detected']:
        print("Acceleration detected: YES")
        print(f"Acceleration coefficient: {accel_result['acceleration_coefficient']:.6f}")
    else:
        print("Acceleration detected: NO (linear trend sufficient)")
    
    # Decadal rates
    print(f"\n--- Decadal Rate Analysis ---")
    decadal_rates = calculate_decadal_rates(actual_years, values)
    for rate in decadal_rates:
        print(f"{rate['decade']}s: {rate['slope_ft_per_year']:.4f} ft/year "
              f"({rate['rate_mm_per_year']:.2f} mm/year, R²={rate['r_squared']:.3f}, "
              f"n={rate['num_years']})")
    
    # Store results
    results = {
        'station': station_name,
        'data_period': f"{actual_years.min()}-{actual_years.max()}",
        'linear_trend': linear_result,
        'acceleration': accel_result,
        'decadal_rates': decadal_rates,
        'government_comparison': gov_comparison,
        'years': years,
        'values': values,
        'actual_years': actual_years
    }
    
    return results

def plot_trends(all_results, output_dir='output'):
    """Create visualization plots for all stations."""
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(len(all_results), 1, figsize=(12, 5*len(all_results)))
    if len(all_results) == 1:
        axes = [axes]
    
    for idx, result in enumerate(all_results):
        ax = axes[idx]
        station = result['station']
        years = result['actual_years']
        values = result['values']
        
        # Plot data points
        ax.scatter(years, values, alpha=0.6, s=50, label='Annual mean water level')
        
        # Plot linear trend
        linear = result['linear_trend']
        years_sorted = np.sort(years)
        linear_fit = linear_trend(years_sorted - years.min(), linear['intercept'], linear['slope_ft_per_year'])
        ax.plot(years_sorted, linear_fit, 'r--', linewidth=2, 
                label=f"Linear trend: {linear['slope_ft_per_year']:.4f} ft/yr")
        
        # Plot quadratic trend if acceleration detected
        if result['acceleration']['acceleration_detected']:
            quad = result['acceleration']['quadratic']
            quad_fit = quad['polynomial'](years_sorted - years.min())
            ax.plot(years_sorted, quad_fit, 'g--', linewidth=2, 
                    label=f"Quadratic trend (acceleration)")
        
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Water Level (ft)', fontsize=12)
        ax.set_title(f'{station} - Water Level Trends', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'trend_analysis.png')
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"\n[OK] Trend plots saved to: {plot_file}")
    plt.close()

def main():
    """Main function to perform trend analysis."""
    print("=" * 60)
    print("Water Level Trend Analysis")
    print("=" * 60)
    
    # Load annual data
    annual_file = 'output/annual_water_levels.csv'
    if not os.path.exists(annual_file):
        print(f"Error: {annual_file} not found!")
        print("Please run aggregate_data.py first.")
        return
    
    annual_data = pd.read_csv(annual_file)
    
    # Analyze each station
    stations = annual_data['station'].unique()
    all_results = []
    
    for station in stations:
        station_data = annual_data[annual_data['station'] == station].copy()
        result = analyze_station(station, station_data)
        all_results.append(result)
    
    # Create visualizations
    plot_trends(all_results)
    
    # Save results summary
    summary_data = []
    for result in all_results:
        summary_data.append({
            'station': result['station'],
            'data_period': result['data_period'],
            'rate_ft_per_year': result['linear_trend']['slope_ft_per_year'],
            'rate_mm_per_year': result['linear_trend']['rate_mm_per_year'],
            'r_squared': result['linear_trend']['r_squared'],
            'p_value': result['linear_trend']['p_value'],
            'acceleration_detected': result['acceleration']['acceleration_detected'],
            'within_gov_interval': result['government_comparison']['within_confidence_interval']
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_file = 'output/trend_analysis_summary.csv'
    summary_df.to_csv(summary_file, index=False)
    print(f"\n[OK] Trend analysis summary saved to: {summary_file}")
    
    print("\n" + "=" * 60)
    print("Trend Analysis Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()







