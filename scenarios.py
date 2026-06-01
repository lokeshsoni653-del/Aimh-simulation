"""
Tactical Scenarios Database (v5.0 Enterprise)
Provides pre-populated historic battle-theater coordinates, winding indices, and terrain data.
Author: Principal Systems Architect (25+ Years Experience)
"""

from typing import Dict, List, Any

SCENARIOS: Dict[str, Dict[str, Any]] = {
    "🎖️ Operation Zojila (Kashmir - 1948)": {
        "title": "Passage of the Tanks — Zojila Pass Breakthrough",
        "intro": "The historic strategic deployment of light tanks by the Pakistan Army at an extreme altitude of 11,578 feet, breaking through heavily entrenched positions over the Himalayan ridge. Critical focus: high-altitude alpine logistics, narrow tracks, and extreme weather constraints.",
        "nodes": {
            "Main Logistic Base (Skardu)": {"lat": 35.2975, "lon": 75.6333, "type": "HQ", "desc": "Sector Logistics Command Center."},
            "Chillum Checkpost": {"lat": 35.0833, "lon": 75.1167, "type": "Checkpost", "desc": "High altitude valley security transit checkpoint."},
            "FOB Minimarg": {"lat": 34.7878, "lon": 75.1436, "type": "FOB", "desc": "Forward alpine logistical assembly area at the base of the pass."},
            "Zojila Pass FDL (Ambush Zone)": {"lat": 34.2831, "lon": 75.4686, "type": "FDL", "desc": "Critical mountain bottleneck. High ambush threat."}
        },
        "path_coords": [
            [35.2975, 75.6333],
            [35.15, 75.40],
            [35.0833, 75.1167],
            [34.90, 75.05],
            [34.7878, 75.1436],
            [34.55, 75.25],
            [34.2831, 75.4686]
        ],
        "road_winding": 1.62,
        "base_elev": 2200.0,
        "peak_elev": 3530.0,
        "hazard_radius": 15000,
        "hazard_center": [34.7878, 75.1436],
        "hazard_desc": "Avalanche / Snow Drift Zone"
    },
    "🏜️ Thar Desert Campaign (Chhor Sector)": {
        "title": "Operation Sandwind — Water & Fuel Pipelines",
        "intro": "Long-range supply operations across shifting sand dunes, requiring absolute tracking of water distribution, fuel expenditure, and wheel traction modeling. Critical focus: dehydration risk and mobility in sand-dunes.",
        "nodes": {
            "Chhor Logistics Base": {"lat": 25.5134, "lon": 69.7573, "type": "HQ", "desc": "Strategic railhead and main desert logistics depot."},
            "Water Depot (Khipro)": {"lat": 25.8286, "lon": 69.7831, "type": "Checkpost", "desc": "Primary bore-well water distribution depot."},
            "FOB Umerkot": {"lat": 25.3614, "lon": 69.7381, "type": "FOB", "desc": "Forward combat command base monitoring sand tracks."},
            "Thar Border Outpost": {"lat": 25.8000, "lon": 70.3500, "type": "FDL", "desc": "Deep desert border patrol observation outpost."}
        },
        "path_coords": [
            [25.5134, 69.7573],
            [25.65, 69.85],
            [25.8286, 69.7831],
            [25.60, 70.00],
            [25.3614, 69.7381],
            [25.55, 70.15],
            [25.8000, 70.3500]
        ],
        "road_winding": 1.32,
        "base_elev": 50.0,
        "peak_elev": 190.0,
        "hazard_radius": 22000,
        "hazard_center": [25.60, 70.00],
        "hazard_desc": "High Heat Dehydration Zone"
    },
    "🗻 Karakoram Highway Strategic Logistics Corridor": {
        "title": "Operation Khunjerab — High-Altitude Deep Corridor",
        "intro": "The world's highest paved international border crossing at 15,397 feet. Modeling structural corridor connectivity, rockfall hazards, and extreme vehicle transmission climbs. Critical focus: landslide closures and road winding multipliers.",
        "nodes": {
            "Rawalpindi Command HQ": {"lat": 33.5973, "lon": 73.0479, "type": "HQ", "desc": "General Logistics Command Headquarters."},
            "Abbottabad Base": {"lat": 34.1688, "lon": 73.2215, "type": "Checkpost", "desc": "Intermediate logistical staging base."},
            "Chilas Logistics Node": {"lat": 35.4216, "lon": 74.0950, "type": "FOB", "desc": "Logistics hub monitoring Indus River gorge terrain."},
            "Khunjerab Border Post": {"lat": 36.8486, "lon": 75.4292, "type": "FDL", "desc": "High altitude alpine international border crossing."}
        },
        "path_coords": [
            [33.5973, 73.0479],
            [33.90, 73.15],
            [34.1688, 73.2215],
            [34.80, 73.50],
            [35.4216, 74.0950],
            [36.10, 74.30],
            [36.8486, 75.4292]
        ],
        "road_winding": 1.85,
        "base_elev": 500.0,
        "peak_elev": 4693.0,
        "hazard_radius": 28000,
        "hazard_center": [35.4216, 74.0950],
        "hazard_desc": "Critical Landslide Gorge Zone"
    }
}
