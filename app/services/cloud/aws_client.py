import boto3
from typing import Dict, Any

class AWSClient:
    def __init__(self, access_key: str, secret_key: str):
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
    def get_compute_instances(self) -> Dict[str, Any]:
        ec2 = self.session.client('ec2')
        response = ec2.describe_instances()
        return self._parse_ec2_data(response)
    
    def _parse_ec2_data(self, data: Dict) -> Dict:
        # Process raw AWS data into standardized format
        instances = []
        for reservation in data['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'instance_id': instance['InstanceId'],
                    'instance_type': instance['InstanceType'],
                    'state': instance['State']['Name'],
                    'launch_time': instance['LaunchTime'],
                    'tags': instance.get('Tags', [])
                })
        return {'instances': instances}