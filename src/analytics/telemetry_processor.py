import pandas as pd
import numpy as np

class TelemetryAnalyzer:
    """Processes field test data to perform root-cause analysis on power losses."""
    def __init__(self, df_telemetry: pd.DataFrame):
        self.df = df_telemetry

    def calculate_power_losses(self, hyd_loss_constant: float) -> pd.DataFrame:
        """Quantifies power distributions across vehicle subsystems."""
        # Engine Mechanical Power: P = (Torque * RPM) / 9550
        self.df['engine_power_kw'] = (self.df['engine_torque_nm'] * self.df['engine_speed_rpm']) / 9550
        
        # PTO Power Output
        self.df['pto_power_kw'] = (self.df['pto_torque_nm'] * self.df['pto_speed_rpm']) / 9550
        
        # Subsystem losses calculation
        self.df['hydraulic_loss_kw'] = hyd_loss_constant
        self.df['drivetrain_loss_kw'] = self.df['engine_power_kw'] * 0.12 # Assuming 12% baseline drivetrain loss
        
        # Remaining power available for Drawbar work
        self.df['residual_drawbar_power_kw'] = (
            self.df['engine_power_kw'] - self.df['pto_power_kw'] - 
            self.df['hydraulic_loss_kw'] - self.df['drivetrain_loss_kw']
        )
        return self.df

    def identify_performance_gaps(self) -> pd.DataFrame:
        """Flags operations with poor fuel economy or excessive slip anomalies."""
        # High Engine load combined with drop in efficiency
        anomalies = self.df[
            (self.df['engine_speed_rpm'] < 1300) & 
            (self.df['fuel_rate_lph'] > 18.0)
        ]
        return anomalies
      
