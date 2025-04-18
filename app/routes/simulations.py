from flask import Blueprint, jsonify, request
from app.services.carbon_calculator import CarbonCalculator

simulation_bp = Blueprint('simulation', __name__)

@simulation_bp.route('/simulate', methods=['POST'])
def run_simulation():
    config = request.json
    calculator = CarbonCalculator(config['cloud_provider'])
    
    # Base scenario
    baseline = calculator.calculate(config['workload'])
    
    # Optimized scenario
    optimized_config = apply_optimizations(config)
    optimized = calculator.calculate(optimized_config)
    
    return jsonify({
        'baseline': baseline,
        'optimized': optimized,
        'savings': {
            'emissions': baseline['emissions'] - optimized['emissions'],
            'energy': baseline['energy_consumed'] - optimized['energy_consumed'],
            'cost': calculate_cost_savings(baseline, optimized)
        }
    })

def apply_optimizations(config):
    # Apply optimization rules based on recommendations
    optimized = config.copy()
    if 'instance_type' in config:
        optimized['instance_type'] = get_optimized_instance(config['instance_type'])
    if 'region' in config:
        optimized['region'] = get_green_region(config['region'])
    return optimized