from flask import Blueprint, jsonify, request
from app.models.models import Assessment, Recommendation
from app.services.analyzer import WorkloadAnalyzer
from app.services.recommender import RecommendationEngine

bp = Blueprint('api', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze_workload():
    data = request.json
    analyzer = WorkloadAnalyzer(data.get('cloud_provider', 'aws'))
    results = analyzer.analyze_workload()
    
    assessment = Assessment(
        cloud_provider=data['cloud_provider'],
        instance_type=data['instance_type'],
        region=data['region'],
        cpu_util=results['cpu_util'],
        gpu_util=0,  # Placeholder for GPU monitoring
        emissions=results['emissions']
    )
    
    db.session.add(assessment)
    db.session.commit()
    
    recommender = RecommendationEngine()
    recommendations = recommender.generate(results)
    
    for rec in recommendations:
        recommendation = Recommendation(
            assessment_id=assessment.id,
            text=rec['text'],
            impact=rec['impact'],
            effort=rec['effort']
        )
        db.session.add(recommendation)
    
    db.session.commit()
    
    return jsonify({
        'assessment_id': assessment.id,
        'emissions': results['emissions'],
        'recommendations': recommendations
    })