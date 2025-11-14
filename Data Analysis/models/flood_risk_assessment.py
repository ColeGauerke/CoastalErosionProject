#!/usr/bin/env python3
"""
Flood risk assessment for Louisiana coastal cities.
Maps projected water levels to city elevations to determine flood risk.
"""

import pandas as pd
import numpy as np
import os

# Louisiana coastal cities with approximate average elevations (feet above sea level)
# Data from various sources - may need adjustment based on actual elevation data
COASTAL_CITIES = {
    'New Orleans': {'elevation_ft': 1.5, 'latitude': 29.9511, 'longitude': -90.0715},
    'Grand Isle': {'elevation_ft': 2.0, 'latitude': 29.2369, 'longitude': -89.9867},
    'Port Fourchon': {'elevation_ft': 3.0, 'latitude': 29.1056, 'longitude': -90.1994},
    'Lafitte': {'elevation_ft': 1.0, 'latitude': 29.6902, 'longitude': -90.1015},
    'Cocodrie': {'elevation_ft': 1.5, 'latitude': 29.2469, 'longitude': -90.6615},
    'Golden Meadow': {'elevation_ft': 2.5, 'latitude': 29.3877, 'longitude': -90.2612},
    'Gallo': {'elevation_ft': 1.0, 'latitude': 29.4522, 'longitude': -90.3023},
    'Montegut': {'elevation_ft': 2.0, 'latitude': 29.4744, 'longitude': -90.5565},
    'Dulac': {'elevation_ft': 1.5, 'latitude': 29.3888, 'longitude': -90.7131},
    'Chauvin': {'elevation_ft': 1.0, 'latitude': 29.4333, 'longitude': -90.5967},
    'Cut Off': {'elevation_ft': 3.0, 'latitude': 29.5333, 'longitude': -90.3333},
    'Larose': {'elevation_ft': 2.5, 'latitude': 29.5667, 'longitude': -90.3667},
    'Lockport': {'elevation_ft': 2.0, 'latitude': 29.6500, 'longitude': -90.5333},
    'Galliano': {'elevation_ft': 2.5, 'latitude': 29.4500, 'longitude': -90.3000},
    'Houma': {'elevation_ft': 10.0, 'latitude': 29.5958, 'longitude': -90.7195},
    'Morgan City': {'elevation_ft': 5.0, 'latitude': 29.6994, 'longitude': -91.2067},
    'Thibodaux': {'elevation_ft': 12.0, 'latitude': 29.7958, 'longitude': -90.8228},
    'Raceland': {'elevation_ft': 7.0, 'latitude': 29.7333, 'longitude': -90.5833},
    'Mathews': {'elevation_ft': 5.0, 'latitude': 29.6833, 'longitude': -90.5333},
    'Bayou Cane': {'elevation_ft': 9.0, 'latitude': 29.6244, 'longitude': -90.7511},
}

def calculate_flood_risk(projected_water_level, city_elevation):
    """
    Calculate flood risk metrics.
    
    Args:
        projected_water_level: Projected water level in feet (relative to baseline)
        city_elevation: City elevation in feet above sea level
        
    Returns:
        Dictionary with flood risk metrics
    """
    # Water level is relative to baseline, so we need to add it to sea level
    # Assuming baseline is at sea level (0 ft), projected water level represents
    # the water level relative to that baseline
    
    # If water level exceeds elevation, city is flooded
    water_depth = projected_water_level - city_elevation
    
    if water_depth > 0:
        flood_status = "UNDERWATER"
        percent_flooded = min(100, (water_depth / city_elevation) * 100) if city_elevation > 0 else 100
    elif water_depth > -1:
        flood_status = "CRITICAL"  # Within 1 foot of flooding
        percent_flooded = abs(water_depth) * 50  # Estimate based on proximity
    elif water_depth > -3:
        flood_status = "HIGH RISK"  # Within 3 feet
        percent_flooded = abs(water_depth) * 25
    elif water_depth > -5:
        flood_status = "MODERATE RISK"
        percent_flooded = abs(water_depth) * 10
    else:
        flood_status = "LOW RISK"
        percent_flooded = 0
    
    return {
        'water_level_ft': projected_water_level,
        'city_elevation_ft': city_elevation,
        'water_depth_ft': water_depth,
        'flood_status': flood_status,
        'estimated_percent_flooded': max(0, min(100, percent_flooded))
    }

def assess_all_cities(projections_df, output_dir='output'):
    """Assess flood risk for all cities at each projection year."""
    
    print("=" * 60)
    print("Flood Risk Assessment for Louisiana Coastal Cities")
    print("=" * 60)
    
    # Use projections (all should be from blended model now)
    projections = projections_df.copy()
    
    if len(projections) == 0:
        print("Error: No projections found!")
        return None
    
    risk_assessments = []
    
    for _, proj_row in projections.iterrows():
        station = proj_row['station']
        year = int(proj_row['year'])
        water_level = proj_row['prediction_ft']
        ci_lower = proj_row['ci_lower_ft']
        ci_upper = proj_row['ci_upper_ft']
        
        # For each city, assess flood risk
        for city_name, city_info in COASTAL_CITIES.items():
            elevation = city_info['elevation_ft']
            
            # Use mean projection (could also use upper CI for worst case)
            risk = calculate_flood_risk(water_level, elevation)
            
            # Also calculate worst case using upper CI
            worst_case = calculate_flood_risk(ci_upper, elevation)
            
            risk_assessments.append({
                'station': station,
                'year': year,
                'city': city_name,
                'city_elevation_ft': elevation,
                'projected_water_level_ft': water_level,
                'ci_lower_ft': ci_lower,
                'ci_upper_ft': ci_upper,
                'water_depth_ft': risk['water_depth_ft'],
                'flood_status': risk['flood_status'],
                'estimated_percent_flooded': risk['estimated_percent_flooded'],
                'worst_case_status': worst_case['flood_status'],
                'worst_case_percent_flooded': worst_case['estimated_percent_flooded'],
                'latitude': city_info['latitude'],
                'longitude': city_info['longitude']
            })
    
    risk_df = pd.DataFrame(risk_assessments)
    
    # Save results
    output_file = os.path.join(output_dir, 'flood_risk_assessment.csv')
    risk_df.to_csv(output_file, index=False)
    print(f"\n[OK] Flood risk assessment saved to: {output_file}")
    
    # Generate summary by year
    print("\n" + "=" * 60)
    print("Flood Risk Summary by Year")
    print("=" * 60)
    
    for year in sorted(risk_df['year'].unique()):
        year_data = risk_df[risk_df['year'] == year]
        
        # Count cities by risk status
        underwater = len(year_data[year_data['flood_status'] == 'UNDERWATER'])
        critical = len(year_data[year_data['flood_status'] == 'CRITICAL'])
        high_risk = len(year_data[year_data['flood_status'] == 'HIGH RISK'])
        
        print(f"\n{year}:")
        print(f"  Underwater: {underwater} cities")
        print(f"  Critical (<1 ft margin): {critical} cities")
        print(f"  High Risk (<3 ft margin): {high_risk} cities")
        
        # Show cities at highest risk
        if underwater > 0 or critical > 0:
            print(f"\n  Cities at highest risk:")
            high_risk_cities = year_data[year_data['flood_status'].isin(['UNDERWATER', 'CRITICAL'])].copy()
            high_risk_cities = high_risk_cities.sort_values('water_depth_ft', ascending=False)
            
            for _, city_row in high_risk_cities.head(10).iterrows():
                status = city_row['flood_status']
                depth = city_row['water_depth_ft']
                station = city_row['station']
                print(f"    {city_row['city']:20s} ({station:20s}): {status:12s} "
                      f"Depth: {depth:>6.2f} ft")
    
    # Generate station-specific summaries
    print("\n" + "=" * 60)
    print("Flood Risk by Station")
    print("=" * 60)
    
    for station in sorted(risk_df['station'].unique()):
        print(f"\n{station}:")
        station_data = risk_df[risk_df['station'] == station]
        
        for year in sorted(station_data['year'].unique()):
            year_data = station_data[station_data['year'] == year]
            underwater = len(year_data[year_data['flood_status'] == 'UNDERWATER'])
            critical = len(year_data[year_data['flood_status'] == 'CRITICAL'])
            
            if underwater > 0 or critical > 0:
                print(f"  {year}: {underwater} underwater, {critical} critical")
    
    return risk_df

def create_risk_summary_table(risk_df, output_dir='output'):
    """Create a summary table of cities at risk."""
    
    # Group by city and year, get worst case across stations
    summary_data = []
    
    for city in sorted(risk_df['city'].unique()):
        city_data = risk_df[risk_df['city'] == city]
        elevation = city_data['city_elevation_ft'].iloc[0]
        
        city_summary = {'city': city, 'elevation_ft': elevation}
        
        for year in sorted(city_data['year'].unique()):
            year_data = city_data[city_data['year'] == year]
            
            # Get worst case (highest water level)
            max_water_level = year_data['projected_water_level_ft'].max()
            max_ci_upper = year_data['ci_upper_ft'].max()
            
            worst_case = calculate_flood_risk(max_ci_upper, elevation)
            
            city_summary[f'{year}_status'] = worst_case['flood_status']
            city_summary[f'{year}_water_level'] = max_water_level
            city_summary[f'{year}_worst_case'] = max_ci_upper
        
        summary_data.append(city_summary)
    
    summary_df = pd.DataFrame(summary_data)
    
    output_file = os.path.join(output_dir, 'flood_risk_summary.csv')
    summary_df.to_csv(output_file, index=False)
    print(f"\n[OK] Risk summary table saved to: {output_file}")
    
    return summary_df

def main():
    """Main function for flood risk assessment."""
    
    # Load projections
    projections_file = 'output/water_level_projections.csv'
    if not os.path.exists(projections_file):
        print(f"Error: {projections_file} not found!")
        print("Please run projection_models.py first.")
        return
    
    projections_df = pd.read_csv(projections_file)
    
    # Assess flood risk
    risk_df = assess_all_cities(projections_df)
    
    if risk_df is not None:
        # Create summary table
        summary_df = create_risk_summary_table(risk_df)
        
        print("\n" + "=" * 60)
        print("Flood Risk Assessment Complete")
        print("=" * 60)
        
        # Print final summary
        print("\nKey Findings:")
        print("-" * 60)
        
        for year in [2030, 2035, 2040, 2045, 2050]:
            year_data = risk_df[risk_df['year'] == year]
            underwater = len(year_data[year_data['flood_status'] == 'UNDERWATER'])
            critical = len(year_data[year_data['flood_status'] == 'CRITICAL'])
            
            if underwater > 0:
                cities = year_data[year_data['flood_status'] == 'UNDERWATER']['city'].unique()
                print(f"{year}: {underwater} cities projected underwater: {', '.join(cities[:5])}")

if __name__ == "__main__":
    main()







