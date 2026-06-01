"""
Battle-Theater Geospatial Logistics & Strategic Wargaming Engine (v5.0 Enterprise)
Core Mathematical Routing, Tactical Formations, and Monte Carlo Wargaming Simulation Core.
Author: Principal Systems Architect (25+ Years Experience)
"""

from typing import Dict, List, Tuple, Any, Optional
import math
import random
import numpy as np

class Coordinate:
    """Represents a geographic point with latitude, longitude, and elevation."""
    def __init__(self, lat: float, lon: float, elevation: float = 0.0):
        self.lat: float = lat
        self.lon: float = lon
        self.elevation: float = elevation

    def distance_to(self, other: 'Coordinate') -> float:
        """Calculates Haversine distance in kilometers to another coordinate."""
        R = 6371.0  # Earth's radius in km
        lat1_rad = math.radians(self.lat)
        lon1_rad = math.radians(self.lon)
        lat2_rad = math.radians(other.lat)
        lon2_rad = math.radians(other.lon)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

class LogisticsConvoy:
    """Models a tactical vehicle convoy with payloads, fuel burn rates, and velocities."""
    def __init__(self, vehicle_type: str, fleet_size: int, payload_per_vehicle: float):
        self.vehicle_type: str = vehicle_type
        self.fleet_size: int = fleet_size
        self.payload_per_vehicle: float = payload_per_vehicle
        self.total_payload: float = fleet_size * payload_per_vehicle

        # Establish engineering profiles based on platform type
        self.profiles: Dict[str, Dict[str, float]] = {
            "Heavy Logistics Vehicle (HLV)": {"speed": 25.0, "fuel_rate": 0.45, "slope_max": 14.0},
            "4x4 Utility Truck": {"speed": 40.0, "fuel_rate": 0.25, "slope_max": 20.0},
            "Tracked APC Carrier": {"speed": 18.0, "fuel_rate": 0.65, "slope_max": 25.0},
            "High-Altitude Pack Animal": {"speed": 5.0, "fuel_rate": 0.02, "slope_max": 30.0}
        }

        profile = self.profiles.get(vehicle_type, self.profiles["4x4 Utility Truck"])
        self.base_speed: float = profile["speed"]
        self.fuel_burn_per_km: float = profile["fuel_rate"]
        self.max_slope_capacity: float = profile["slope_max"]

    def calculate_actual_speed(self, weather: str, max_altitude: float, formation: str) -> float:
        """Computes speed penalty multipliers based on weather, altitude, and tactical formation."""
        weather_multipliers = {
            "Clear & Dry": 1.0,
            "Heavy Snow / Alpine Winter": 0.45,
            "Severe Heat & Sandstorms": 0.65,
            "Monsoon / Landslides": 0.50,
            "High-Altitude Blizzard": 0.25
        }
        
        mult = weather_multipliers.get(weather, 1.0)
        
        # Formation multipliers
        formation_multipliers = {
            "Column Formation (Max Speed)": 1.15,
            "Vee Formation (Balanced Defense)": 0.90,
            "Line Formation (Wide Coverage)": 0.70
        }
        mult *= formation_multipliers.get(formation, 1.0)
        
        # Altitude hypoxia carburetor air-thinning engine power reduction (above 2500m)
        if max_altitude > 2500.0:
            alt_penalty = 1.0 - ((max_altitude - 2500.0) / 10000.0)
            mult *= max(0.5, alt_penalty)
            
        return self.base_speed * mult

class CombatSimEngine:
    """High-fidelity operations wargamer simulating mission success indices."""
    def __init__(self, ambush_threat: str, peak_altitude: float, escorts: bool, mine_sweepers: bool, air_support: bool, posture: str):
        self.ambush_threat: str = ambush_threat
        self.peak_altitude: float = peak_altitude
        self.escorts: bool = escorts
        self.mine_sweepers: bool = mine_sweepers
        self.air_support: bool = air_support
        self.posture: str = posture

        # Base strategic probabilities
        threat_levels = {"LOW": 0.06, "MEDIUM": 0.20, "HIGH": 0.55, "CRITICAL": 0.88}
        self.base_ambush_prob: float = threat_levels.get(ambush_threat, 0.06)
        
        # High altitude terrain hazard factor (above 3000m)
        self.alpine_risk: float = 0.25 if peak_altitude > 3000.0 else 0.05

    def run_monte_carlo(self, convoy: LogisticsConvoy, distance: float, speed: float, iterations: int = 100) -> Dict[str, Any]:
        """Runs 100-run simulation of convoy transits returning detailed metrics."""
        success_runs = 0
        combat_aborts = 0
        alpine_aborts = 0
        fuel_aborts = 0
        ammo_depleted_aborts = 0
        total_delivered_payload = 0
        durations = []
        fuel_usages = []

        # Adjust threat and speed depending on combat posture
        # "Aggressive Breakthrough", "Stealth Movement", "Standard Recon Cover"
        posture_modifiers = {
            "Aggressive Breakthrough": {"threat": 1.2, "speed": 1.25, "fuel": 1.3},
            "Stealth Movement": {"threat": 0.45, "speed": 0.7, "fuel": 0.85},
            "Standard Recon Cover": {"threat": 1.0, "speed": 1.0, "fuel": 1.0}
        }
        posture_mod = posture_modifiers.get(self.posture, posture_modifiers["Standard Recon Cover"])

        # Deployed protection multipliers
        ambush_prob = self.base_ambush_prob * posture_mod["threat"]
        if self.escorts:
            ambush_prob *= 0.5
        if self.air_support:
            ambush_prob *= 0.3
            
        alpine_fail_prob = self.alpine_risk
        if self.mine_sweepers:
            alpine_fail_prob *= 0.6

        for _ in range(iterations):
            # 1. Roll for combat ambush interception
            intercepted = random.random() < ambush_prob
            if intercepted:
                escaped = random.random() < (0.85 if self.escorts else 0.25)
                if not escaped:
                    combat_aborts += 1
                    continue
                # Combat engagement consumes ammunition. Roll for ammo depletion
                if not self.escorts and random.random() < 0.35:
                    ammo_depleted_aborts += 1
                    continue

            # 2. Roll for high altitude structural landslips/avalanches
            landslip = random.random() < alpine_fail_prob
            if landslip and random.random() < 0.45:
                alpine_aborts += 1
                continue

            # 3. Simulate Fuel Depreciation Curve
            # Base fuel capacity is 80 liters per vehicle. High altitude increases fuel burn by 25%
            burn_rate = convoy.fuel_burn_per_km * posture_mod["fuel"] * (1.25 if self.peak_altitude > 3000.0 else 1.0)
            fuel_needed = distance * burn_rate
            
            if fuel_needed > 100.0:  # Out of range limit
                fuel_aborts += 1
                continue

            # Successful trip
            success_runs += 1
            fuel_usages.append(fuel_needed)
            
            # Winding traffic friction delays
            delay = random.uniform(1.0, 1.4)
            durations.append((distance / (speed * posture_mod["speed"])) * delay)
            
            # Simulated cargo yield delivery
            total_delivered_payload += convoy.total_payload * random.uniform(0.9, 1.0)

        avg_dur = np.mean(durations) if durations else 0.0
        avg_fuel = np.mean(fuel_usages) if fuel_usages else 0.0
        yield_rate = (delivered_supplies := total_delivered_payload) / (convoy.total_payload * iterations) * 100 if iterations else 0.0

        return {
            "success_rate": success_runs,
            "combat_aborts": combat_aborts,
            "alpine_aborts": alpine_aborts,
            "fuel_aborts": fuel_aborts,
            "ammo_depleted_aborts": ammo_depleted_aborts,
            "avg_duration": avg_dur,
            "avg_fuel_usage": avg_fuel,
            "total_delivered_tons": delivered_supplies,
            "yield_rate": yield_rate
        }
