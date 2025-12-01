#!/usr/bin/env python3
"""
Master script to run the complete water level projection analysis pipeline.
Runs all phases: aggregation, trend analysis, projections, and flood assessment.
Main output: output/flood_risk_summary.csv
"""

import os
import sys

def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print("\n" + "=" * 60)
    print(description)
    print("=" * 60)
    
    if not os.path.exists(script_name):
        print(f"Error: {script_name} not found!")
        return False
    
    try:
        # Import and run the script
        module_name = script_name.replace('.py', '').replace('/', '.').replace('\\', '.')
        if module_name.startswith('.'):
            module_name = module_name[1:]
        
        # Use exec to run the script
        with open(script_name, 'r') as f:
            code = f.read()
        
        exec(compile(code, script_name, 'exec'), {'__name__': '__main__'})
        
        return True
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the complete analysis pipeline."""
    
    print("=" * 60)
    print("Water Level Projection Analysis Pipeline")
    print("=" * 60)
    print("\nThis script will run the complete analysis:")
    print("1. Data aggregation (hourly to annual)")
    print("2. Trend analysis")
    print("3. Optimized blended ensemble model projections")
    print("4. Flood risk assessment")
    
    scripts = [
        ('data_cleaning/aggregate_data.py', 'Phase 1: Data Aggregation'),
        ('models/trend_analysis.py', 'Phase 2: Trend Analysis'),
        ('models/projection_models.py', 'Phase 3: Projection Models'),
        ('models/flood_risk_assessment.py', 'Phase 4: Flood Risk Assessment')
    ]
    
    success_count = 0
    for script, description in scripts:
        success = run_script(script, description)
        if success:
            success_count += 1
        else:
            print(f"\nFailed at {description}. Stopping pipeline.")
            break
    
    print("\n" + "=" * 60)
    print("Pipeline Summary")
    print("=" * 60)
    print(f"Completed: {success_count}/{len(scripts)} phases")
    
    if success_count == len(scripts):
        print("\n[SUCCESS] All phases completed successfully!")
        print("\nMain Output File:")
        print(" output/flood_risk_summary.csv - Main predictions file")
        print("\nOther Output Files:")
        print("  - output/annual_water_levels.csv")
        print("  - output/trend_analysis_summary.csv")
        print("  - output/water_level_projections.csv")
        print("  - output/flood_risk_assessment.csv")
        print("  - output/trend_analysis.png")
    else:
        print("\n[WARNING] Pipeline incomplete. Check errors above.")

if __name__ == "__main__":
    main()







