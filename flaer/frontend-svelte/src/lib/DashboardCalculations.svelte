<script>
  import { onMount } from 'svelte';

  let metrics = [
    {
      category: 'Core Data Center Metrics',
      items: [
        { name: 'PUE', formula: 'PUE = Total Facility Energy / IT Equipment Energy' },
        { name: 'WUE', formula: 'WUE = Total Water Usage / IT Equipment Energy' },
        { name: 'CUE', formula: 'CUE = Total CO2e Emissions / IT Equipment Energy' },
        { name: 'ERE', formula: 'ERE = Total Facility Energy / IT Equipment Energy' },
        { name: 'ERF', formula: 'ERF = Reused Energy / Total Facility Energy' },
        { name: 'ERE (Alternative)', formula: 'ERE = PUE × (1 - ERF)' }
      ]
    },
    {
      category: 'Emissions Calculations',
      items: [
        { name: 'Total CO2e Emissions', formula: 'Total CO2e Emissions = Scope 1 Emissions + Scope 2 Emissions + Scope 3 Emissions' },
        { name: 'Scope 1 Emissions', formula: 'Scope 1 Emissions = Fuel Consumption × Fuel Emission Factor' },
        { name: 'Scope 2 Location-Based Emissions', formula: 'Scope 2 Location-Based Emissions = Electricity Consumption × Grid Average Emission Factor' },
        { name: 'Scope 2 Market-Based Emissions', formula: 'Scope 2 Market-Based Emissions = Electricity Consumption × Supplier or Contractual Emission Factor' },
        { name: 'Scope 3 Emissions', formula: 'Scope 3 Emissions = Sum of Upstream and Downstream Activity Emissions' },
        { name: 'Activity Emissions', formula: 'Activity Emissions = Activity Data × Emission Factor' }
      ]
    },
    {
      category: 'Carbon Metrics',
      items: [
        { name: 'CUE Location-Based', formula: 'CUE Location-Based = Location-Based CO2e Emissions / IT Equipment Energy' },
        { name: 'CUE Market-Based', formula: 'CUE Market-Based = Market-Based CO2e Emissions / IT Equipment Energy' },
        { name: 'Carbon Intensity of Energy', formula: 'Carbon Intensity of Energy = CO2e Emissions / Energy Consumption' },
        { name: 'Carbon Intensity of Compute', formula: 'Carbon Intensity of Compute = CO2e Emissions / Compute Output' },
        { name: 'CIC', formula: 'CIC = kgCO2e / Compute Unit' },
        { name: 'Examples', formula: 'kgCO2e per VM-hour, kgCO2e per API request, kgCO2e per training job, kgCO2e per TB stored' }
      ]
    },
    {
      category: 'Time-Aware Carbon Metrics',
      items: [
        { name: 'Time-Aware Emissions', formula: 'Time-Aware Emissions = Sum of Energy at Time t × Carbon Intensity at Time t' },
        { name: 'TACE', formula: 'TACE = Sum(Energy_t × CarbonIntensity_t) / Total Compute Output' },
        { name: 'Carbon Savings from Load Shifting', formula: 'Carbon Savings from Load Shifting = Baseline Emissions - Shifted Emissions' },
        { name: 'Baseline Emissions', formula: 'Baseline Emissions = Energy_baseline × CarbonIntensity_baseline' },
        { name: 'Shifted Emissions', formula: 'Shifted Emissions = Energy_shifted × CarbonIntensity_shifted' }
      ]
    },
    {
      category: 'Water Metrics',
      items: [
        { name: 'WUE', formula: 'WUE = Water Liters / IT Energy kWh' },
        { name: 'Water-Stress Weighted WUE', formula: 'WW-WUE = WUE × Water Stress Index' },
        { name: 'Total Water Impact', formula: 'Total Water Impact = Water Usage × Water Stress Index' }
      ]
    },
    {
      category: 'Energy Reuse Metrics',
      items: [
        { name: 'ERF', formula: 'ERF = Reused Energy / Total Facility Energy' },
        { name: 'ERE', formula: 'ERE = (Total Facility Energy - Reused Energy) / IT Energy' },
        { name: 'Heat Reuse Rate', formula: 'Heat Reuse Rate = Useful Reused Heat / Total Waste Heat' },
        { name: 'Heat Recovery Effectiveness', formula: 'Heat Recovery Effectiveness = Useful Reused Heat / Recoverable Waste Heat' }
      ]
    },
    {
      category: 'Lifecycle and Hardware Metrics',
      items: [
        { name: 'Embodied Carbon Ratio', formula: 'ECR = Embodied CO2e / Total CO2e' },
        { name: 'Annualized Embodied Emissions', formula: 'Annualized Embodied Emissions = Total Embodied Emissions / Expected Asset Lifetime' },
        { name: 'Hardware Lifecycle Emissions', formula: 'Hardware Lifecycle Emissions = Manufacturing Emissions + Transport Emissions + Maintenance Emissions + End-of-Life Emissions' },
        { name: 'Total Lifecycle Emissions', formula: 'Total Lifecycle Emissions = Operational Emissions + Embodied Emissions' }
      ]
    },
    {
      category: 'Utilization Metrics',
      items: [
        { name: 'Utilization Efficiency Factor', formula: 'UEF = Actual Compute Used / Provisioned Compute Capacity' },
        { name: 'Idle Capacity', formula: 'Idle Capacity = Provisioned Compute Capacity - Actual Compute Used' },
        { name: 'Idle Capacity Percentage', formula: 'Idle Capacity Percentage = Idle Capacity / Provisioned Compute Capacity' }
      ]
    },
    {
      category: 'Business and Financial Metrics',
      items: [
        { name: 'Carbon ROI', formula: 'C-ROI = Revenue / kgCO2e' },
        { name: 'Marginal Abatement Efficiency', formula: 'MAE = Delta CO2e / Cost' },
        { name: 'Cost per tCO2e Saved', formula: 'Cost per tCO2e Saved = Project Cost / Avoided tCO2e' },
        { name: 'Payback Period', formula: 'Payback Period = Initial Investment / Annual Cost Savings' },
        { name: 'Sustainability Payback', formula: 'Sustainability Payback = Initial Investment / Annual Sustainability Savings' },
        { name: 'Annual Sustainability Savings', formula: 'Annual Sustainability Savings = Energy Cost Savings + Carbon Cost Savings + Water Cost Savings' },
        { name: 'Carbon Cost Savings', formula: 'Carbon Cost Savings = Avoided tCO2e × Carbon Price' }
      ]
    },
    {
      category: 'Recommendation Scoring',
      items: [
        { name: 'Recommendation Score', formula: 'Recommendation Score = Emissions Reduction Potential × Confidence × Urgency / Implementation Cost' },
        { name: 'Priority Score', formula: 'Priority Score = Impact Score + Cost Score + Risk Score + Compliance Score' },
        { name: 'Avoidable Emissions Index', formula: 'AEI = Avoidable CO2e / Current CO2e' }
      ]
    },
    {
      category: 'Location and Site Planning Metrics',
      items: [
        { name: 'Location Efficiency Score', formula: 'LES = w1 × Grid Carbon Score + w2 × Water Score + w3 × Climate Score + w4 × Renewable Score + w5 × Regulation Score' },
        { name: 'Expansion Suitability Score', formula: 'Expansion Suitability Score = Carbon Score + Water Score + Energy Price Score + Land/Capacity Score + Regulation Score' }
      ]
    },
    {
      category: 'Portfolio Metrics',
      items: [
        { name: 'Portfolio PUE', formula: 'Portfolio PUE = Total Facility Energy Across All Sites / Total IT Energy Across All Sites' },
        { name: 'Portfolio CUE', formula: 'Portfolio CUE = Total Portfolio CO2e / Total Portfolio IT Energy' },
        { name: 'Portfolio WUE', formula: 'Portfolio WUE = Total Portfolio Water Usage / Total Portfolio IT Energy' },
        { name: 'Portfolio Emissions', formula: 'Portfolio Emissions = Sum of All Site Emissions' },
        { name: 'Portfolio Risk Score', formula: 'Portfolio Risk Score = Weighted average of site risk scores' },
        { name: 'Weighted Site Risk', formula: 'Weighted Site Risk = Site Risk Score × Site Capacity Share' },
        { name: 'Capacity Share', formula: 'Capacity Share = Site IT Capacity / Total Portfolio IT Capacity' }
      ]
    }
  ];
</script>

<div class="calculations-panel">
  <h2>FLAER Calculations & Metrics</h2>
  <p class="description">Comprehensive list of data center carbon, energy, water, and financial metrics used in FLAER analysis.</p>

  {#each metrics as category}
    <div class="category">
      <h3>{category.category}</h3>
      <div class="metrics-grid">
        {#each category.items as item}
          <div class="metric-card">
            <h4>{item.name}</h4>
            <code>{item.formula}</code>
          </div>
        {/each}
      </div>
    </div>
  {/each}
</div>

<style>
  .calculations-panel {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }

  h2 {
    color: #2c3e50;
    margin-bottom: 10px;
  }

  .description {
    color: #7f8c8d;
    margin-bottom: 30px;
  }

  .category {
    margin-bottom: 40px;
  }

  .category h3 {
    color: #34495e;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 20px;
  }

  .metric-card {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 15px;
    transition: box-shadow 0.2s;
  }

  .metric-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }

  .metric-card h4 {
    color: #495057;
    margin: 0 0 10px 0;
    font-size: 1.1em;
  }

  .metric-card code {
    background: #ffffff;
    padding: 8px 12px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    color: #2c3e50;
    display: block;
    border: 1px solid #dee2e6;
  }
</style></content>
<parameter name="filePath">c:\Users\Locaccio\Desktop\Flaer\flaer\frontend-svelte\src\lib\DashboardCalculations.svelte