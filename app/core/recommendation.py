from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np

class RecommendationSystem:
    """Generates tailored sustainability recommendations for AI infrastructure."""
    
    def __init__(self, assessment_data: Dict = None):
        """Initialize the recommendation system.
        
        Args:
            assessment_data: Data from the assessment engine
        """
        self.assessment_data = assessment_data
        self.recommendations = []
        
        # Define recommendation categories
        self.categories = [
            'Model Selection',
            'Model Optimization',
            'Resource Management',
            'Hardware Configuration',
            'Scheduling & Workload',
            'Infrastructure Location'
        ]
        
    def set_assessment_data(self, assessment_data: Dict):
        """Set assessment data for generating recommendations.
        
        Args:
            assessment_data: Data from the assessment engine
        """
        self.assessment_data = assessment_data
        
    def _get_model_recommendations(self) -> List[Dict]:
        """Generate recommendations related to model selection.
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Check if large models can be downsized
        if self.assessment_data and 'models' in self.assessment_data:
            models = self.assessment_data['models']
            
            for model_name, specs in models.items():
                # If model is large (>10B params), recommend distillation
                if specs.get('parameters', 0) > 10e9:
                    recommendations.append({
                        'id': 'model-01',
                        'title': f'Consider model distillation for {model_name}',
                        'description': f'Model {model_name} has {specs["parameters"]/1e9:.1f}B parameters. ' 
                                      f'Consider using knowledge distillation to create a smaller model that maintains accuracy.',
                        'impact': 'high',
                        'effort': 'medium',
                        'category': 'Model Selection',
                        'estimated_savings': {
                            'energy_percent': 40,
                            'carbon_kg_per_month': self.assessment_data.get('energy_data', {}).get('monthly_carbon_kg', 0) * 0.4
                        }
                    })
                
                # If model using FP32, recommend quantization
                if specs.get('precision') == 'fp32':
                    recommendations.append({
                        'id': 'model-02',
                        'title': f'Quantize {model_name} from FP32 to FP16 or INT8',
                        'description': f'Model {model_name} is using FP32 precision. Quantizing to FP16 could reduce '
                                      f'memory usage and computation with minimal accuracy impact.',
                        'impact': 'medium',
                        'effort': 'low',
                        'category': 'Model Optimization',
                        'estimated_savings': {
                            'energy_percent': 25,
                            'carbon_kg_per_month': self.assessment_data.get('energy_data', {}).get('monthly_carbon_kg', 0) * 0.25
                        }
                    })
        
        return recommendations
    
    def _get_hardware_recommendations(self) -> List[Dict]:
        """Generate recommendations related to hardware configuration.
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        if self.assessment_data and 'hardware_metrics' in self.assessment_data:
            metrics = self.assessment_data['hardware_metrics']
            
            # Check GPU utilization
            gpu_util_values = list(metrics['gpu_utilization'].values())
            avg_gpu_util = np.mean(gpu_util_values)
            
            if avg_gpu_util < 0.5:
                recommendations.append({
                    'id': 'hw-01',
                    'title': 'Low GPU utilization detected',
                    'description': f'Average GPU utilization is {avg_gpu_util:.1%}, which suggests potential ' 
                                  f'over-provisioning. Consider consolidating workloads or downsizing GPU resources.',
                    'impact': 'high',
                    'effort': 'medium',
                    'category': 'Hardware Configuration',
                    'estimated_savings': {
                        'energy_percent': 30,
                        'carbon_kg_per_month': self.assessment_data.get('energy_data', {}).get('monthly_carbon_kg', 0) * 0.3
                    }
                })
                
            # Recommend more energy-efficient GPUs
            recommendations.append({
                'id': 'hw-02',
                'title': 'Evaluate newer GPU generations for inference',
                'description': 'Newer GPU architectures often provide better energy efficiency. '
                              'Consider using purpose-built inference hardware like NVIDIA T4 or AWS Inferentia.',
                'impact': 'medium',
                'effort': 'high',
                'category': 'Hardware Configuration',
                'estimated_savings': {
                    'energy_percent': 35,
                    'carbon_kg_per_month': self.assessment_data.get('energy_data', {}).get('monthly_carbon_kg', 0) * 0.35
                }
            })
        
        return recommendations
    
    def _get_scheduling_recommendations(self) -> List[Dict]:
        """Generate recommendations related to workload scheduling.
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        recommendations.append({
            'id': 'sched-01',
            'title': 'Implement carbon-aware scheduling',
            'description': 'Schedule non-urgent batch processing jobs during times when the grid has '
                          'higher renewable energy mix or lower carbon intensity.',
            'impact': 'medium',
            'effort': 'medium',
            'category': 'Scheduling & Workload',
            'estimated_savings': {
                'energy_percent': 0, # Energy use is the same, but carbon impact is lower
                'carbon_kg_per_month': self.assessment_data.get('energy_data', {}).get('monthly_carbon_kg', 0) * 0.2
            }
        })
        
        return recommendations
    
    def _get_location_recommendations(self) -> List[Dict]:
        """Generate recommendations related to infrastructure location.
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        recommendations.append({
            'id': 'loc-01',
            'title': 'Consider region with lower carbon intensity',
            'description': 'Moving compute to regions with cleaner energy grids can reduce carbon footprint. '
                          'Cloud regions in Nordics, Canada, and certain US states have lower carbon intensity.',
            'impact': 'high',
            'effort': 'high',
            'category': 'Infrastructure Location',
            'estimated_savings': {
                'energy_percent': 0, # Energy use is the same, but carbon impact is lower
                'carbon_kg_per_month': self.assessment_data.get('energy_data', {}).get('monthly_carbon_kg', 0) * 0.6
            }
        })
        
        return recommendations
    
    def generate_recommendations(self) -> List[Dict]:
        """Generate all recommendations based on assessment data.
        
        Returns:
            List of recommendation dictionaries
        """
        if not self.assessment_data:
            return []
            
        self.recommendations = []
        
        # Collect recommendations from different categories
        self.recommendations.extend(self._get_model_recommendations())
        self.recommendations.extend(self._get_hardware_recommendations())
        self.recommendations.extend(self._get_scheduling_recommendations())
        self.recommendations.extend(self._get_location_recommendations())
        
        # Sort recommendations by impact
        impact_order = {'high': 0, 'medium': 1, 'low': 2}
        self.recommendations.sort(key=lambda x: impact_order.get(x.get('impact'), 99))
        
        return self.recommendations
    
    def get_roi_estimates(self) -> Dict:
        """Calculate return on investment for implementing recommendations.
        
        Returns:
            Dictionary with ROI information
        """
        if not self.recommendations:
            self.generate_recommendations()
            
        total_carbon_savings = sum(rec.get('estimated_savings', {}).get('carbon_kg_per_month', 0) 
                                 for rec in self.recommendations)
        
        # Estimate cost savings based on energy reduction
        # Assuming $0.15 per kWh average electricity cost
        energy_cost_per_kwh = 0.15
        
        if 'energy_data' in self.assessment_data:
            monthly_energy_kwh = self.assessment_data['energy_data'].get('monthly_energy_kwh', 0)
            
            # Calculate total percentage energy reduction from all recommendations
            total_energy_percent_reduction = min(
                sum(rec.get('estimated_savings', {}).get('energy_percent', 0) / 100 
                    for rec in self.recommendations),
                0.9  # Cap at 90% to be realistic
            )
            
            energy_savings_kwh = monthly_energy_kwh * total_energy_percent_reduction
            cost_savings_monthly = energy_savings_kwh * energy_cost_per_kwh
            cost_savings_yearly = cost_savings_monthly * 12
            
            return {
                'monthly_carbon_savings_kg': total_carbon_savings,
                'yearly_carbon_savings_kg': total_carbon_savings * 12,
                'monthly_energy_savings_kwh': energy_savings_kwh,
                'yearly_energy_savings_kwh': energy_savings_kwh * 12,
                'monthly_cost_savings_usd': cost_savings_monthly,
                'yearly_cost_savings_usd': cost_savings_yearly,
                'trees_equivalent': total_carbon_savings * 12 / 21,  # One tree absorbs ~21kg CO2 per year
            }
        
        return {
            'monthly_carbon_savings_kg': total_carbon_savings,
            'yearly_carbon_savings_kg': total_carbon_savings * 12
        }

