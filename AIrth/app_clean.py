"""
AIrth Web Application - Clean Professional Edition
Fixed layout, working comparisons, beautiful scope emissions chart
"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from airth_platform import AIrthPlatform

# Initialize platform
platform = AIrthPlatform()

# Add data centers
data_centers = [
    ("Google Council Bluffs Iowa", (41.2619, -95.8608), 180, 850000, 0.52, 75),
    ("AWS US-East Virginia", (38.9072, -77.0369), 200, 900000, 0.45, 45),
    ("Microsoft Azure Virginia", (38.8816, -77.1045), 175, 820000, 0.45, 50),
    ("Facebook Prineville Oregon", (44.2999, -120.8342), 160, 780000, 0.28, 80),
    ("Apple Mesa Arizona", (33.4152, -111.8315), 140, 700000, 0.42, 85),
    ("Google Hamina Finland", (60.5695, 27.1978), 120, 750000, 0.15, 95),
    ("Azure Netherlands", (52.3676, 4.9041), 95, 600000, 0.35, 65),
    ("AWS Frankfurt Germany", (50.1109, 8.6821), 110, 650000, 0.38, 55),
    ("OVH Roubaix France", (50.6942, 3.1746), 85, 520000, 0.32, 60),
    ("Equinix London", (51.5074, -0.1278), 100, 580000, 0.28, 70),
    ("China Telecom Inner Mongolia", (40.8414, 111.7519), 150, 1000000, 0.65, 15),
    ("Meta Singapore", (1.3521, 103.8198), 110, 700000, 0.42, 30),
    ("AWS Tokyo Japan", (35.6762, 139.6503), 130, 720000, 0.48, 35),
    ("Alibaba Hangzhou China", (30.2741, 120.1551), 145, 850000, 0.62, 20),
    ("NTT Mumbai India", (19.0760, 72.8777), 105, 640000, 0.72, 25),
    ("AWS Sydney Australia", (-33.8688, 151.2093), 95, 580000, 0.82, 22),
    ("Azure São Paulo Brazil", (-23.5505, -46.6333), 88, 550000, 0.48, 40),
    ("Equinix Dubai UAE", (25.2048, 55.2708), 92, 560000, 0.55, 28),
    ("AWS Seoul South Korea", (37.5665, 126.9780), 115, 680000, 0.52, 32),
    ("Microsoft Johannesburg", (-26.2041, 28.0473), 78, 480000, 0.88, 18),
]

for name, location, power, area, carbon, renewable in data_centers:
    platform.add_data_center(name, location, power, area, carbon, renewable)

platform.train_prediction_model()

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = "AIrth - Sustainable Energy Platform"

# Colors
COLORS = {'primary': '#00FFA3', 'secondary': '#7C3AED', 'accent': '#F59E0B', 
          'danger': '#EF4444', 'success': '#10B981', 'info': '#3B82F6'}

# Stats
total_power = sum(dc.power_mw for dc in platform.data_centers)
total_emissions = sum(dc.carbon_emissions_tons_year for dc in platform.data_centers)
total_water = sum(dc.water_usage_liters_day for dc in platform.data_centers)
avg_renewable = np.mean([dc.renewable_percentage for dc in platform.data_centers])

# Functions
def create_map():
    fig = go.Figure()
    for dc in platform.data_centers:
        metrics = dc.get_metrics()
        color = '#10B981' if metrics['effective_emissions'] < 50000 else '#F59E0B' if metrics['effective_emissions'] < 150000 else '#EF4444'
        fig.add_trace(go.Scattergeo(
            lon=[dc.location[1]], lat=[dc.location[0]],
            text=f"<b>{dc.name}</b><br>Power: {dc.power_mw:.0f} MW<br>Emissions: {metrics['effective_emissions']:.0f} tons",
            hoverinfo='text', mode='markers',
            marker=dict(size=max(10, dc.power_mw / 12), color=color, line=dict(width=2, color='white')),
            showlegend=False
        ))
    fig.update_layout(
        geo=dict(projection_type='natural earth', showland=True, landcolor='#2a2a2a',
                 oceancolor='#1a1a1a', bgcolor='#0a0a0a'),
        paper_bgcolor='#0a0a0a', margin=dict(l=0, r=0, t=0, b=0), height=450
    )
    return fig

def create_scope_chart(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return go.Figure()
    
    scope = dc.calculate_scope_emissions()
    
    # Create beautiful bar chart instead of pie
    fig = go.Figure()
    
    scopes = ['Scope 1<br>(Direct)', 'Scope 2<br>(Electricity)', 'Scope 3<br>(Other)']
    values = [scope['scope1_tons'], scope['scope2_tons'], scope['scope3_tons']]
    colors = ['#EF4444', '#F59E0B', '#10B981']
    
    fig.add_trace(go.Bar(
        x=scopes,
        y=values,
        marker=dict(
            color=colors,
            line=dict(color='white', width=2)
        ),
        text=[f"{v:.0f} tons" for v in values],
        textposition='outside',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{x}</b><br>%{y:.0f} tons CO₂<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f'<b>Emissions by Scope</b><br><sub>Total: {scope["total_tons"]:.0f} tons CO₂/year</sub>',
            font=dict(size=18, color='white')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        height=400,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False
        ),
        yaxis=dict(
            title='CO₂ Emissions (tons/year)',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=False,
            zeroline=False
        ),
        margin=dict(t=80, b=60, l=60, r=40)
    )
    
    return fig

def create_comparison(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("Select a data center", style={'color': 'white', 'padding': '2rem', 'textAlign': 'center'})
    
    # Get all data centers sorted by emissions
    all_dcs_with_metrics = [(d, d.get_metrics()) for d in platform.data_centers]
    sorted_dcs = sorted(all_dcs_with_metrics, key=lambda x: x[1]['effective_emissions'])
    
    best_dc, best_metrics = sorted_dcs[0]
    worst_dc, worst_metrics = sorted_dcs[-1]
    current_metrics = dc.get_metrics()
    
    def create_card(dc_obj, metrics, label, color, icon):
        return html.Div([
            html.Div([
                html.I(className=f"fas {icon}", style={'fontSize': '2rem', 'color': color, 'marginRight': '1rem'}),
                html.Div([
                    html.H6(label, style={'color': color, 'marginBottom': '0.25rem', 'fontWeight': '700'}),
                    html.H5(dc_obj.name, style={'marginBottom': '0', 'fontSize': '1.1rem'})
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1rem'}),
            html.Div([
                html.Div([
                    html.P("Emissions", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.6)', 'marginBottom': '0.25rem'}),
                    html.H4(f"{metrics['effective_emissions']:,.0f}", style={'color': color, 'marginBottom': '0', 'fontSize': '1.5rem'}),
                    html.P("tons CO₂/year", style={'fontSize': '0.7rem', 'color': 'rgba(255,255,255,0.5)'})
                ], style={'flex': '1', 'textAlign': 'center'}),
                html.Div([
                    html.P("Renewable", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.6)', 'marginBottom': '0.25rem'}),
                    html.H4(f"{dc_obj.renewable_percentage:.0f}%", style={'color': color, 'marginBottom': '0', 'fontSize': '1.5rem'}),
                    html.P("clean energy", style={'fontSize': '0.7rem', 'color': 'rgba(255,255,255,0.5)'})
                ], style={'flex': '1', 'textAlign': 'center'}),
                html.Div([
                    html.P("Power", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.6)', 'marginBottom': '0.25rem'}),
                    html.H4(f"{dc_obj.power_mw:.0f}", style={'color': color, 'marginBottom': '0', 'fontSize': '1.5rem'}),
                    html.P("MW capacity", style={'fontSize': '0.7rem', 'color': 'rgba(255,255,255,0.5)'})
                ], style={'flex': '1', 'textAlign': 'center'})
            ], style={'display': 'flex', 'gap': '1rem'})
        ], style={
            'padding': '1.5rem',
            'background': f"linear-gradient(135deg, {color}15 0%, {color}05 100%)",
            'borderRadius': '16px',
            'border': f'2px solid {color}40',
            'marginBottom': '1rem'
        })
    
    return html.Div([
        html.H4("Industry Benchmarking", style={'marginBottom': '1.5rem', 'color': 'white'}),
        create_card(best_dc, best_metrics, "🏆 Best Performer", '#10B981', 'fa-trophy'),
        create_card(dc, current_metrics, "📍 Your Selection", '#F59E0B', 'fa-building'),
        create_card(worst_dc, worst_metrics, "⚠️ Needs Improvement", '#EF4444', 'fa-exclamation-triangle')
    ])

def create_efficiency_metrics(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("Select a data center")
    
    metrics = dc.get_metrics()
    
    def create_metric_card(title, value, unit, target, icon, color):
        return html.Div([
            html.I(className=f"fas {icon}", style={'fontSize': '2.5rem', 'color': color, 'marginBottom': '1rem'}),
            html.H2(f"{value:.2f}", style={'color': color, 'fontWeight': '800', 'marginBottom': '0.25rem'}),
            html.P(unit, style={'fontSize': '0.875rem', 'color': 'rgba(255,255,255,0.6)', 'marginBottom': '0.5rem'}),
            html.P(title, style={'fontSize': '1rem', 'fontWeight': '600', 'marginBottom': '0.5rem'}),
            html.P(f"Target: {target}", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.5)'})
        ], style={
            'textAlign': 'center',
            'padding': '2rem 1rem',
            'background': f"linear-gradient(135deg, {color}20 0%, {color}05 100%)",
            'borderRadius': '16px',
            'border': f'2px solid {color}40'
        })
    
    pue = metrics['pue']
    pue_color = '#10B981' if pue < 1.3 else '#F59E0B' if pue < 1.7 else '#EF4444'
    
    wue = metrics['wue']
    wue_color = '#10B981' if wue < 1.8 else '#F59E0B' if wue < 3.0 else '#EF4444'
    
    cue = metrics['cue']
    cue_color = '#10B981' if cue < 0.3 else '#F59E0B' if cue < 0.5 else '#EF4444'
    
    return dbc.Row([
        dbc.Col(create_metric_card("Power Usage Effectiveness", pue, "PUE", "<1.3", "fa-plug", pue_color), md=4),
        dbc.Col(create_metric_card("Water Usage Effectiveness", wue, "L/kWh", "<1.8", "fa-tint", wue_color), md=4),
        dbc.Col(create_metric_card("Carbon Usage Effectiveness", cue, "kg/kWh", "<0.3", "fa-smog", cue_color), md=4),
    ])

def create_cost_analysis(dc_name):
    dc = next((d for d in platform.data_centers if d.name == dc_name), None)
    if not dc:
        return html.Div("Select a data center")
    
    metrics = dc.get_metrics()
    roi = dc.calculate_roi_renewable(5000000)
    
    return html.Div([
        html.H4("Financial Analysis", style={'marginBottom': '1.5rem', 'color': 'white'}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-bolt", style={'fontSize': '2rem', 'color': '#F59E0B'}),
                    html.H3(f"${metrics['energy_cost_usd']/1000000:.1f}M", style={'color': '#F59E0B', 'marginTop': '0.5rem'}),
                    html.P("Energy Cost/year", style={'fontSize': '0.875rem', 'color': 'rgba(255,255,255,0.6)'})
                ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(245,158,11,0.1)', 'borderRadius': '12px'})
            ], md=3),
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-tint", style={'fontSize': '2rem', 'color': '#3B82F6'}),
                    html.H3(f"${metrics['water_cost_usd']/1000000:.1f}M", style={'color': '#3B82F6', 'marginTop': '0.5rem'}),
                    html.P("Water Cost/year", style={'fontSize': '0.875rem', 'color': 'rgba(255,255,255,0.6)'})
                ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(59,130,246,0.1)', 'borderRadius': '12px'})
            ], md=3),
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-smog", style={'fontSize': '2rem', 'color': '#EF4444'}),
                    html.H3(f"${metrics['carbon_cost_usd']/1000000:.1f}M", style={'color': '#EF4444', 'marginTop': '0.5rem'}),
                    html.P("Carbon Cost/year", style={'fontSize': '0.875rem', 'color': 'rgba(255,255,255,0.6)'})
                ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(239,68,68,0.1)', 'borderRadius': '12px'})
            ], md=3),
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-chart-line", style={'fontSize': '2rem', 'color': '#10B981'}),
                    html.H3(f"${roi['annual_savings_usd']/1000000:.1f}M", style={'color': '#10B981', 'marginTop': '0.5rem'}),
                    html.P("Potential Savings", style={'fontSize': '0.875rem', 'color': 'rgba(255,255,255,0.6)'})
                ], style={'textAlign': 'center', 'padding': '1.5rem', 'background': 'rgba(16,185,129,0.1)', 'borderRadius': '12px'})
            ], md=3),
        ]),
        html.Div([
            html.H5("ROI Analysis", style={'color': 'white', 'marginTop': '2rem', 'marginBottom': '1rem'}),
            html.P([html.Strong("Investment: "), f"${roi['investment_usd']:,.0f}"], style={'marginBottom': '0.5rem'}),
            html.P([html.Strong("Payback Period: "), html.Span(roi['payback_period'], style={'color': '#10B981', 'fontSize': '1.2rem', 'fontWeight': '700'})]),
        ], style={'padding': '1.5rem', 'background': 'rgba(255,255,255,0.05)', 'borderRadius': '12px', 'marginTop': '1.5rem'})
    ])

# Layout
app.layout = dbc.Container([
    # Header
    html.Div([
        html.H1("AIrth", style={'fontSize': '4rem', 'fontWeight': '900', 'background': 'linear-gradient(135deg, #00FFA3, #7C3AED)', 
                               'WebkitBackgroundClip': 'text', 'WebkitTextFillColor': 'transparent', 'marginBottom': '0.5rem'}),
        html.P("AI-Powered Sustainable Energy Platform", style={'fontSize': '1.25rem', 'color': 'rgba(255,255,255,0.7)'}),
        html.Div([
            dbc.Badge([html.I(className="fas fa-leaf me-2"), "SDG 7"], color="success", className="me-2"),
            dbc.Badge([html.I(className="fas fa-globe me-2"), "SDG 13"], color="info", className="me-2"),
            dbc.Badge([html.I(className="fas fa-database me-2"), f"{len(platform.data_centers)} Centers"], color="warning"),
        ], style={'marginTop': '1rem'})
    ], style={'textAlign': 'center', 'padding': '3rem 0 2rem 0'}),
    
    # Stats
    dbc.Row([
        dbc.Col([dbc.Card([dbc.CardBody([html.I(className="fas fa-bolt fa-2x mb-2", style={'color': '#F59E0B'}),
                 html.H3(f"{total_power:.0f} MW"), html.P("Total Power")])], color="dark")], md=3),
        dbc.Col([dbc.Card([dbc.CardBody([html.I(className="fas fa-smog fa-2x mb-2", style={'color': '#EF4444'}),
                 html.H3(f"{total_emissions/1000:.1f}k tons"), html.P("CO₂ Emissions")])], color="dark")], md=3),
        dbc.Col([dbc.Card([dbc.CardBody([html.I(className="fas fa-tint fa-2x mb-2", style={'color': '#3B82F6'}),
                 html.H3(f"{total_water/1000000:.1f}M L"), html.P("Water Usage")])], color="dark")], md=3),
        dbc.Col([dbc.Card([dbc.CardBody([html.I(className="fas fa-leaf fa-2x mb-2", style={'color': '#10B981'}),
                 html.H3(f"{avg_renewable:.1f}%"), html.P("Renewable")])], color="dark")], md=3),
    ], className="mb-4"),
    
    # Map
    dbc.Card([dbc.CardHeader(html.H5("🌍 Global Data Center Network")), 
              dbc.CardBody([dcc.Graph(figure=create_map(), config={'displayModeBar': False})])], color="dark", className="mb-4"),
    
    # Selector
    dbc.Card([dbc.CardHeader(html.H5("🔍 Select Data Center for Analysis")),
              dbc.CardBody([dbc.Select(id='dc-selector', options=[{'label': dc.name, 'value': dc.name} for dc in platform.data_centers],
                                      value=platform.data_centers[0].name)])], color="dark", className="mb-4"),
    
    # Efficiency Metrics
    dbc.Card([dbc.CardHeader(html.H5("⚡ Efficiency Metrics")), 
              dbc.CardBody([html.Div(id='efficiency-metrics')])], color="dark", className="mb-4"),
    
    # Scope & Comparison
    dbc.Row([
        dbc.Col([dbc.Card([dbc.CardHeader(html.H5("📊 Emissions by Scope")),
                          dbc.CardBody([dcc.Graph(id='scope-chart', config={'displayModeBar': False})])], color="dark")], md=6, className="mb-4"),
        dbc.Col([dbc.Card([dbc.CardHeader(html.H5("🏆 Industry Benchmarking")),
                          dbc.CardBody([html.Div(id='comparison')])], color="dark")], md=6, className="mb-4"),
    ]),
    
    # Cost Analysis
    dbc.Card([dbc.CardHeader(html.H5("💰 Financial Analysis")),
              dbc.CardBody([html.Div(id='cost-analysis')])], color="dark", className="mb-4"),
    
    # Footer
    html.Div([
        html.P([html.I(className="fas fa-leaf me-2", style={'color': '#10B981'}),
               "AIrth - Supporting UN SDG 7 & 13 | Made with Bob"],
              style={'textAlign': 'center', 'color': 'rgba(255,255,255,0.5)', 'marginTop': '3rem'})
    ])
], fluid=True, style={'backgroundColor': '#0a0a0a', 'minHeight': '100vh', 'padding': '2rem'})

# Callback
@app.callback(
    [Output('efficiency-metrics', 'children'),
     Output('scope-chart', 'figure'),
     Output('comparison', 'children'),
     Output('cost-analysis', 'children')],
    [Input('dc-selector', 'value')]
)
def update_all(dc_name):
    return (create_efficiency_metrics(dc_name),
            create_scope_chart(dc_name),
            create_comparison(dc_name),
            create_cost_analysis(dc_name))

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌍 AIrth - Clean Professional Edition")
    print("="*70)
    print(f"\n✓ {len(platform.data_centers)} data centers loaded")
    print("✓ Fixed: Industry comparison working")
    print("✓ Fixed: Beautiful scope emissions chart")
    print("✓ Fixed: Clean, organized layout")
    print("\n📱 Open: http://127.0.0.1:8050")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=8050)

