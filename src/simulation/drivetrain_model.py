import numpy as np

class DrivetrainSimulator:
    """Simulates tractor vehicle dynamics, speed charts, and drawbar performance."""
    def __init__(self, specs: dict):
        self.specs = specs
        self.mass = specs['chassis']['total_mass_kg']
        self.g = 9.81
        self.r_tyre = specs['chassis']['rear_tyre_radius_m']
        
    def generate_speed_chart(self, engine_speeds: np.ndarray) -> dict:
        """Calculates vehicle speed (km/h) across gears and engine RPM layout."""
        gears = self.specs['transmission']['gear_ratios']
        speed_chart = {}
        
        for idx, ratio in enumerate(gears, start=1):
            # Speed (km/h) = (RPM * 2 * pi * r * 60) / (ratio * 1000)
            speeds = (engine_speeds * 2 * np.pi * self.r_tyre * 60) / (ratio * 1000)
            speed_chart[f"Gear {idx}"] = speeds
        return speed_chart

    def estimate_drawbar_performance(self, engine_torque: float, gear_ratio: float, slip: float) -> dict:
        """Estimates tractive effort, drawbar pull, and power limits considering slip."""
        eff_mech = self.specs['transmission']['mechanical_efficiency']
        
        # Wheel Torque & Gross Tractive Effort
        wheel_torque = engine_torque * gear_ratio * eff_mech
        gross_tractive_effort = wheel_torque / self.r_tyre
        
        # Simplified soil-tyre interaction (Barger traction prediction equations fraction)
        max_tractive_force = self.mass * self.g * self.specs['chassis']['static_rear_weight_fraction'] * (1 - np.exp(-10 * slip))
        
        actual_drawbar_pull = min(gross_tractive_effort, max_tractive_force)
        return {
            "gross_tractive_effort_n": gross_tractive_effort,
            "actual_drawbar_pull_n": actual_drawbar_pull,
            "motion_resistance_n": gross_tractive_effort - actual_drawbar_pull
        }
      
