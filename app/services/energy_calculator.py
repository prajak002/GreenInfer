from typing import Dict, Any
class EnergyCalculator:
    def __init__(self, region: str = 'us-west-2'):
        self.carbon_intensity = self._get_carbon_intensity(region)
        
    @staticmethod
    def _get_carbon_intensity(region: str) -> float:
        # Source: https://ember-climate.org/data/data-tools/data-explorer/
        intensities = {
            'us-west-2': 350,   # Oregon
            'eu-west-1': 250,    # Ireland
            'ap-southeast-1': 550  # Singapore
        }
        return intensities.get(region, 500)
    
    def calculate_energy(self, hardware_data: Dict) -> Dict:
        # Enhanced energy calculation model
        gpu_power = sum([
            self._get_gpu_power_spec(gpu['type']) * gpu['utilization']
            for gpu in hardware_data.get('gpus', [])
        ])
        
        cpu_power = sum([
            self._get_cpu_power_spec(cpu['type']) * cpu['utilization']
            for cpu in hardware_data.get('cpus', [])
        ])
        
        total_power = gpu_power + cpu_power
        return {
            'power_watts': total_power,
            'carbon_kg': total_power * 0.001 * self.carbon_intensity
        }
    
    @staticmethod
    def _get_gpu_power_spec(gpu_type: str) -> float:
        # Reference: https://www.nvidia.com/en-us/data-center/resources/
        specs = {
            'T4': 70,
            'A10G': 150,
            'V100': 250,
            'A100': 400
        }
        return specs.get(gpu_type, 300)