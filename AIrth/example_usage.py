from airth_platform import AIrthPlatform, DataCenterModel

def example_1_basic_usage():
    """Example 1: Basic platform usage"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Usage")
    print("="*70 + "\n")
    
    # Create platform instance
    platform = AIrthPlatform()
    
    # Add a single data center
    dc = platform.add_data_center(
        name="Example Data Center",
        location=(37.7749, -122.4194),  # San Francisco
        power_mw=80,
        area_sqm=400000,
        grid_carbon_intensity=0.3,  # California's relatively clean grid
        renewable_percentage=50
    )
    
    print(f"✓ Added data center: {dc.name}")
    print(f"  Power: {dc.power_mw} MW")
    print(f"  Emissions: {dc.carbon_emissions_tons_year:.0f} tons CO₂/year")
    print(f"  Water usage: {dc.water_usage_liters_day/1000000:.2f} million liters/day")


def example_2_multiple_centers():
    """Example 2: Working with multiple data centers"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Multiple Data Centers")
    print("="*70 + "\n")
    
    platform = AIrthPlatform()
    
    # Add multiple data centers
    centers = [
        ("Tokyo DC", (35.6762, 139.6503), 90, 500000, 0.48, 25),
        ("London DC", (51.5074, -0.1278), 75, 450000, 0.28, 60),
        ("Sydney DC", (-33.8688, 151.2093), 65, 380000, 0.82, 20),
    ]
    
    for name, location, power, area, carbon, renewable in centers:
        platform.add_data_center(name, location, power, area, carbon, renewable)
        print(f"✓ Added: {name}")
    
    print(f"\nTotal data centers: {len(platform.data_centers)}")
    
    # Calculate totals
    total_power = sum(dc.power_mw for dc in platform.data_centers)
    total_emissions = sum(dc.carbon_emissions_tons_year for dc in platform.data_centers)
    
    print(f"Total power consumption: {total_power:.1f} MW")
    print(f"Total annual emissions: {total_emissions:.0f} tons CO₂")


def example_3_predictions():
    """Example 3: AI-powered emissions predictions"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Emissions Predictions")
    print("="*70 + "\n")
    
    platform = AIrthPlatform()
    
    # Add data centers
    platform.add_data_center("DC Alpha", (40.7, -74.0), 100, 600000, 0.5, 30)
    platform.add_data_center("DC Beta", (34.0, -118.2), 85, 500000, 0.35, 55)
    platform.add_data_center("DC Gamma", (51.5, -0.1), 95, 550000, 0.25, 70)
    
    # Train model
    print("Training prediction model...")
    platform.train_prediction_model()
    
    # Generate predictions
    print("\nGenerating 10-year emissions forecast for DC Alpha...")
    predictions = platform.generate_emissions_forecast("DC Alpha", years=10)
    
    print(f"\nCurrent emissions: {predictions[0]:.0f} tons CO₂/year")
    print(f"Predicted in 5 years: {predictions[5]:.0f} tons CO₂/year")
    print(f"Predicted in 10 years: {predictions[10]:.0f} tons CO₂/year")
    print(f"Growth: {((predictions[10]/predictions[0] - 1) * 100):.1f}%")


def example_4_sustainability_report():
    """Example 4: Generate sustainability recommendations"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Sustainability Recommendations")
    print("="*70 + "\n")
    
    platform = AIrthPlatform()
    
    # Add a data center with room for improvement
    platform.add_data_center(
        name="Legacy Data Center",
        location=(41.8781, -87.6298),  # Chicago
        power_mw=150,
        area_sqm=800000,
        grid_carbon_intensity=0.6,  # Coal-heavy grid
        renewable_percentage=10  # Low renewable usage
    )
    
    # Generate comprehensive report
    report = platform.generate_sustainability_report("Legacy Data Center")
    
    print("\nKey findings:")
    print(f"  Sustainability Score: {report['sustainability_score']:.1f}/100")
    print(f"  Number of recommendations: {len(report['recommendations'])}")
    print(f"  Potential emission reduction: {report['total_emission_reduction_tons']:.0f} tons CO₂/year")


def example_5_visualizations():
    """Example 5: Generate all visualizations"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Generate Visualizations")
    print("="*70 + "\n")
    
    platform = AIrthPlatform()
    
    # Add diverse data centers
    platform.add_data_center("US East", (38.9, -77.5), 180, 900000, 0.45, 40)
    platform.add_data_center("EU West", (52.5, 13.4), 120, 650000, 0.35, 65)
    platform.add_data_center("Asia Pacific", (1.3, 103.8), 140, 750000, 0.42, 35)
    platform.add_data_center("Nordic", (60.2, 24.9), 100, 550000, 0.15, 90)
    
    print("Generating visualizations...")
    
    # Global map
    platform.generate_global_map('example_map.html')
    print("✓ Global map: example_map.html")
    
    # Dashboard
    platform.generate_summary_dashboard()
    print("✓ Dashboard: airth_dashboard.png")
    
    # Train and forecast
    platform.train_prediction_model()
    platform.generate_emissions_forecast("US East", years=10)
    print("✓ Forecast: emissions_forecast_US_East.png")
    
    print("\nAll visualizations generated successfully!")


def example_6_custom_analysis():
    """Example 6: Custom analysis and metrics"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Custom Analysis")
    print("="*70 + "\n")
    
    platform = AIrthPlatform()
    
    # Add data centers
    platform.add_data_center("Green DC", (60.0, 10.0), 100, 600000, 0.1, 95)
    platform.add_data_center("Standard DC", (40.0, -100.0), 100, 600000, 0.5, 30)
    platform.add_data_center("Coal DC", (35.0, 110.0), 100, 600000, 0.8, 5)
    
    print("Comparing three data centers with same power but different energy sources:\n")
    
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        print(f"{dc.name}:")
        print(f"  Grid carbon intensity: {0.1 if 'Green' in dc.name else 0.5 if 'Standard' in dc.name else 0.8} kg CO₂/kWh")
        print(f"  Renewable energy: {dc.renewable_percentage}%")
        print(f"  Total emissions: {metrics['carbon_emissions_tons_year']:.0f} tons CO₂/year")
        print(f"  Effective emissions: {metrics['effective_emissions']:.0f} tons CO₂/year")
        print(f"  Sustainability score: {platform.recommender.analyze_and_recommend(dc, 0.5)['sustainability_score']:.1f}/100")
        print()
    
    # Calculate impact of going 100% renewable
    print("Impact of switching all to 100% renewable:")
    current_total = sum(dc.get_metrics()['effective_emissions'] for dc in platform.data_centers)
    
    for dc in platform.data_centers:
        dc.set_renewable_percentage(100)
    
    future_total = sum(dc.get_metrics()['effective_emissions'] for dc in platform.data_centers)
    reduction = current_total - future_total
    
    print(f"  Current total: {current_total:.0f} tons CO₂/year")
    print(f"  With 100% renewable: {future_total:.0f} tons CO₂/year")
    print(f"  Reduction: {reduction:.0f} tons CO₂/year ({(reduction/current_total*100):.1f}%)")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("AIrth Platform - Usage Examples")
    print("="*70)
    
    examples = [
        example_1_basic_usage,
        example_2_multiple_centers,
        example_3_predictions,
        example_4_sustainability_report,
        example_5_visualizations,
        example_6_custom_analysis
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n⚠ Error in {example.__name__}: {e}")
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

