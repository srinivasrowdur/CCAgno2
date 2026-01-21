"""
Pre-built templates for common architecture patterns
"""

ARCHITECTURE_TEMPLATES = {
    "Three-Tier Web Application (AWS)": {
        "description": "A scalable three-tier web application with load balancing, application servers, and database",
        "architecture_type": "cloud",
        "cloud_provider": "AWS",
        "components": "ALB, EC2 instances, RDS, S3, CloudFront"
    },
    "Microservices Architecture (Kubernetes)": {
        "description": "Modern microservices architecture with API gateway, multiple services, message queue, and monitoring",
        "architecture_type": "microservices",
        "cloud_provider": "GCP",
        "components": "GKE, Cloud Load Balancer, Cloud SQL, Pub/Sub, Cloud Monitoring"
    },
    "Serverless Application (AWS)": {
        "description": "Serverless architecture using Lambda functions, API Gateway, DynamoDB, and S3",
        "architecture_type": "serverless",
        "cloud_provider": "AWS",
        "components": "API Gateway, Lambda, DynamoDB, S3, CloudWatch, Cognito"
    },
    "Data Pipeline (AWS)": {
        "description": "Data processing pipeline with ingestion, transformation, storage, and analytics",
        "architecture_type": "data",
        "cloud_provider": "AWS",
        "components": "S3, Kinesis, Lambda, Glue, Redshift, Athena, QuickSight"
    },
    "Event-Driven Architecture (Azure)": {
        "description": "Event-driven system with event hub, functions, and storage",
        "architecture_type": "event-driven",
        "cloud_provider": "Azure",
        "components": "Event Hub, Azure Functions, Cosmos DB, Storage Account, Service Bus"
    },
    "Machine Learning Pipeline (GCP)": {
        "description": "ML pipeline with training, deployment, and inference components",
        "architecture_type": "ml",
        "cloud_provider": "GCP",
        "components": "Vertex AI, Cloud Storage, BigQuery, Cloud Run, Pub/Sub"
    },
    "Multi-Region High Availability (AWS)": {
        "description": "Multi-region architecture with failover, replication, and global load balancing",
        "architecture_type": "cloud",
        "cloud_provider": "AWS",
        "components": "Route 53, CloudFront, ALB, EC2 Auto Scaling, RDS Multi-AZ, S3 Cross-Region Replication"
    },
    "CI/CD Pipeline": {
        "description": "Complete CI/CD pipeline with source control, build, test, and deployment stages",
        "architecture_type": "devops",
        "cloud_provider": "AWS",
        "components": "GitHub, CodePipeline, CodeBuild, CodeDeploy, ECS, CloudWatch"
    }
}


def get_template_names() -> list[str]:
    """Get list of available template names"""
    return list(ARCHITECTURE_TEMPLATES.keys())


def get_template(name: str) -> dict:
    """Get a specific template by name"""
    return ARCHITECTURE_TEMPLATES.get(name, {})
