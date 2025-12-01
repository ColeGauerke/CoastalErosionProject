#!/usr/bin/env python3
"""
Create CSV file with predictions for all recorded towns/cities.
This is the main output file for town-level predictions.
"""

import pandas as pd
import os

def create_town_predictions_csv():
    """Create a clean CSV with predictions for all towns."""
    
    print("=" * 80)
    print("CREATING TOWN PREDICTIONS CSV")
    print("=" * 80)
    
    # Load flood risk assessment (has all town data)
    risk_file = 'output/flood_risk_assessment.csv'
    if not os.path.exists(risk_file):
        print(f"Error: {risk_file} not found!")
        print("Please run flood_risk_assessment.py first.")
        return
    
    risk_df = pd.read_csv(risk_file)
    
    # Get unique towns
    towns = sorted(risk_df['city'].unique())
    years = sorted(risk_df['year'].unique())
    
    print(f"\nFound {len(towns)} towns/cities")
    print(f"Projection years: {years}")
    
    # Create town predictions table
    town_predictions = []
    
    for town in towns:
        town_data = risk_df[risk_df['city'] == town].copy()
        
        # Get basic info (same for all years)
        first_row = town_data.iloc[0]
        elevation = first_row['city_elevation_ft']
        lat = first_row['latitude']
        lon = first_row['longitude']
        
        # For each year, get worst case across stations
        for year in years:
            year_data = town_data[town_data['year'] == year]
            
            # Get worst case (highest water level)
            worst_row = year_data.loc[year_data['projected_water_level_ft'].idxmax()]
            
            town_predictions.append({
                'town': town,
                'year': int(year),
                'elevation_ft': elevation,
                'latitude': lat,
                'longitude': lon,
                'projected_water_level_ft': worst_row['projected_water_level_ft'],
                'ci_lower_ft': worst_row['ci_lower_ft'],
                'ci_upper_ft': worst_row['ci_upper_ft'],
                'water_depth_ft': worst_row['water_depth_ft'],
                'flood_status': worst_row['flood_status'],
                'percent_flooded': worst_row['estimated_percent_flooded'],
                'worst_case_status': worst_row['worst_case_status'],
                'worst_case_percent_flooded': worst_row['worst_case_percent_flooded'],
                'source_station': worst_row['station']
            })
    
    predictions_df = pd.DataFrame(town_predictions)
    
    # Save main predictions file
    output_file = 'output/town_predictions.csv'
    predictions_df.to_csv(output_file, index=False)
    print(f"\n[OK] Town predictions saved to: {output_file}")
    
    # Create a simplified version (easier to read)
    simple_df = predictions_df[['town', 'year', 'elevation_ft', 'projected_water_level_ft', 
                                'ci_lower_ft', 'ci_upper_ft', 'water_depth_ft', 'flood_status']].copy()
    simple_file = 'output/town_predictions_simple.csv'
    simple_df.to_csv(simple_file, index=False)
    print(f"[OK] Simplified version saved to: {simple_file}")
    
    # Create summary by town (all years in one row) - MATCHING flood_risk_summary.csv format
    summary_rows = []
    for town in towns:
        town_data = predictions_df[predictions_df['town'] == town].copy()
        first_row = town_data.iloc[0]
        
        row = {
            'city': town,  # Use 'city' to match flood_risk_summary.csv
            'elevation_ft': first_row['elevation_ft']
        }
        
        # Add predictions for each year in the exact format of flood_risk_summary.csv
        for year in years:
            year_data = town_data[town_data['year'] == year]
            if len(year_data) > 0:
                yr = year_data.iloc[0]
                # Match exact column names from flood_risk_summary.csv
                row[f'{year}_status'] = yr['flood_status']
                row[f'{year}_water_level'] = yr['projected_water_level_ft']
                row[f'{year}_worst_case'] = yr['ci_upper_ft']  # Worst case = upper CI
        
        summary_rows.append(row)
    
    summary_df = pd.DataFrame(summary_rows)
    
    # Save as the main town predictions file (matching flood_risk_summary.csv format)
    summary_file = 'output/town_predictions_summary.csv'
    summary_df.to_csv(summary_file, index=False)
    print(f"[OK] Town predictions (matching flood_risk_summary.csv format) saved to: {summary_file}")
    
    # Also save as town_predictions.csv (overwrite the previous one)
    summary_df.to_csv('output/town_predictions.csv', index=False)
    print(f"[OK] Also saved as: output/town_predictions.csv")
    
    # Print preview
    print(f"\n{'='*80}")
    print("PREVIEW: First 5 towns, 2030 predictions")
    print(f"{'='*80}")
    preview = predictions_df[predictions_df['year'] == 2030].head(5)
    print(preview[['town', 'elevation_ft', 'projected_water_level_ft', 
                   'water_depth_ft', 'flood_status']].to_string(index=False))
    
    print(f"\n{'='*80}")
    print("SUMMARY STATISTICS")
    print(f"{'='*80}")
    for year in years:
        year_data = predictions_df[predictions_df['year'] == year]
        underwater = len(year_data[year_data['flood_status'] == 'UNDERWATER'])
        critical = len(year_data[year_data['flood_status'] == 'CRITICAL'])
        high_risk = len(year_data[year_data['flood_status'] == 'HIGH RISK'])
        
        print(f"\n{year}:")
        print(f"  Underwater: {underwater} towns")
        print(f"  Critical: {critical} towns")
        print(f"  High Risk: {high_risk} towns")
    
    return predictions_df

if __name__ == "__main__":
    create_town_predictions_csv()

