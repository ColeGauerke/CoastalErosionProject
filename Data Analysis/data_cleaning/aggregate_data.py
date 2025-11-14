#!/usr/bin/env python3
"""
Aggregate hourly water level data to annual statistics for long-term trend analysis.
Handles different data periods for each station.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# Government baseline rate: 6.2 mm/year = 0.0203 ft/year (2.03 ft per 100 years)
GOVERNMENT_SLR_RATE_MM_YEAR = 6.2
GOVERNMENT_SLR_RATE_FT_YEAR = 0.0203
GOVERNMENT_SLR_RATE_FT_100YEAR = 2.03

def aggregate_station_data(filepath, station_name):
    """
    Aggregate hourly water level data to annual statistics.
    
    Args:
        filepath: Path to cleaned CSV file
        station_name: Name of the station
        
    Returns:
        DataFrame with annual statistics
    """
    print(f"\nProcessing {station_name}...")
    
    if not os.path.exists(filepath):
        print(f"Warning: File '{filepath}' not found!")
        return None
    
    # Load data with low_memory=False to handle mixed types
    df = pd.read_csv(filepath, low_memory=False)
    
    # Convert Verified_ft to numeric, handling any non-numeric values
    df['Verified_ft'] = pd.to_numeric(df['Verified_ft'], errors='coerce')
    
    # Filter out rows with invalid data
    df = df.dropna(subset=['Verified_ft'])
    
    # Try to parse datetime - handle different formats
    # First try standard format: YYYY/MM/DD HH:MM
    try:
        df['datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), 
                                        format='%Y/%m/%d %H:%M', errors='coerce')
    except:
        df['datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), 
                                        errors='coerce')
    
    # Filter out rows where datetime parsing failed
    df = df.dropna(subset=['datetime'])
    
    # Extract year
    df['year'] = df['datetime'].dt.year
    
    # Filter out invalid years (should be between 1980 and 2100)
    df = df[(df['year'] >= 1980) & (df['year'] <= 2100)]
    
    # Group by year and calculate statistics
    annual_stats = df.groupby('year').agg({
        'Verified_ft': [
            'mean',      # Annual mean water level
            'median',    # Annual median
            'std',       # Annual standard deviation
            'min',       # Annual minimum
            'max',       # Annual maximum
            'count'      # Number of observations per year
        ]
    }).reset_index()
    
    # Flatten column names
    annual_stats.columns = ['year', 'mean_ft', 'median_ft', 'std_ft', 'min_ft', 'max_ft', 'count']
    
    # Add station name
    annual_stats['station'] = station_name
    
    # Calculate years since start of data period
    start_year = annual_stats['year'].min()
    annual_stats['years_since_start'] = annual_stats['year'] - start_year
    
    # Calculate years since 1980 (for comparison across stations)
    annual_stats['years_since_1980'] = annual_stats['year'] - 1980
    
    print(f"  Date range: {annual_stats['year'].min()} to {annual_stats['year'].max()}")
    print(f"  Number of years: {len(annual_stats)}")
    print(f"  Mean water level range: {annual_stats['mean_ft'].min():.2f} to {annual_stats['mean_ft'].max():.2f} ft")
    
    return annual_stats

def calculate_decadal_stats(annual_df):
    """
    Calculate decadal statistics for trend analysis.
    
    Args:
        annual_df: DataFrame with annual statistics
        
    Returns:
        DataFrame with decadal statistics
    """
    annual_df = annual_df.copy()
    annual_df['decade'] = (annual_df['year'] // 10) * 10
    
    decadal_stats = annual_df.groupby('decade').agg({
        'mean_ft': ['mean', 'std'],
        'year': 'count'
    }).reset_index()
    
    decadal_stats.columns = ['decade', 'decadal_mean_ft', 'decadal_std_ft', 'num_years']
    
    return decadal_stats

def main():
    """Main function to aggregate all station data."""
    
    print("=" * 60)
    print("Water Level Data Aggregation for Long-Term Trend Analysis")
    print("=" * 60)
    
    # Define stations and their data files
    stations = {
        'Grand Isle': 'output/cleaned_grandisle@data_water_levels.csv',
        'New Canal Station': 'output/cleaned_new_canal_station_water_levels.csv',
        'Port Fourchon': 'output/cleaned_port_fourchan_water_levels.csv'
    }
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    all_annual_data = []
    
    # Process each station
    for station_name, filepath in stations.items():
        annual_data = aggregate_station_data(filepath, station_name)
        if annual_data is not None:
            all_annual_data.append(annual_data)
    
    if not all_annual_data:
        print("No data was processed!")
        return
    
    # Combine all stations
    combined_annual = pd.concat(all_annual_data, ignore_index=True)
    
    # Save combined annual data
    output_file = 'output/annual_water_levels.csv'
    combined_annual.to_csv(output_file, index=False)
    print(f"\n[OK] Combined annual data saved to: {output_file}")
    
    # Save station-specific files
    for station_name in stations.keys():
        station_data = combined_annual[combined_annual['station'] == station_name]
        station_file = f"output/annual_{station_name.lower().replace(' ', '_')}_water_levels.csv"
        station_data.to_csv(station_file, index=False)
        print(f"[OK] {station_name} annual data saved to: {station_file}")
    
    # Calculate decadal statistics
    print("\n" + "=" * 60)
    print("Decadal Statistics Summary")
    print("=" * 60)
    
    for station_name in stations.keys():
        station_data = combined_annual[combined_annual['station'] == station_name]
        if len(station_data) > 0:
            decadal_stats = calculate_decadal_stats(station_data)
            print(f"\n{station_name}:")
            for _, row in decadal_stats.iterrows():
                print(f"  {row['decade']}s: Mean = {row['decadal_mean_ft']:.2f} ft "
                      f"(±{row['decadal_std_ft']:.2f} ft, {int(row['num_years'])} years)")
    
    print("\n" + "=" * 60)
    print("Government Baseline Rate Reference")
    print("=" * 60)
    print(f"SLR Rate: {GOVERNMENT_SLR_RATE_MM_YEAR} mm/year (±0.97 mm/year)")
    print(f"Equivalent: {GOVERNMENT_SLR_RATE_FT_YEAR:.4f} ft/year")
    print(f"100-year projection: {GOVERNMENT_SLR_RATE_FT_100YEAR:.2f} ft")
    print(f"Baseline period: 1982-2024")
    
    print("\nDone!")

if __name__ == "__main__":
    main()

