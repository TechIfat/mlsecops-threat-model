# System Architecture

## Overview
The ML-based fraud detection system operates in real-time, processing credit card transactions and assigning risk scores to determine if transactions should be approved, declined, or flagged for manual review.

## Components

### 1. Data Ingestion Layer
- **Transaction Stream:** Real-time credit card transaction data
- **Feature Engineering:** Customer behavior, transaction patterns, merchant data
- **Data Validation:** Input sanitization and anomaly detection

### 2. ML Pipeline
- **Model Training:** Supervised learning using historical fraud data
- **Model Serving:** Real-time inference API
- **Model Monitoring:** Performance metrics and drift detection

### 3. Decision Engine
- **Risk Scoring:** ML model output combined with business rules
- **Action Determination:** Approve, decline, or flag for review
- **Audit Logging:** All decisions tracked for compliance

### 4. Security Controls
- **Input Validation:** Adversarial input detection
- **Model Protection:** Anti-extraction measures
- **Monitoring:** Real-time security event detection

## Attack Surface Analysis

### External Attack Vectors
1. **Transaction API Endpoints:** Direct model queries
2. **Data Sources:** External merchant/customer data
3. **Model Updates:** Training data injection points

### Internal Attack Vectors
1. **Model Development:** Compromised training pipelines
2. **Deployment:** Model replacement attacks
3. **Monitoring:** Alert suppression or manipulation

## Data Flow

```mermaid
graph TD
    A[Transaction Input] --> B[Feature Engineering]
    B --> C[ML Model]
    C --> D[Risk Score]
    D --> E[Decision Engine]
    E --> F[Action: Approve/Decline/Flag]
    
    G[Training Data] --> H[Model Training]
    H --> I[Model Validation]
    I --> J[Model Deployment]
    J --> C
    
    K[Security Monitoring] --> L[Threat Detection]
    L --> M[Incident Response]

    ## Infrastructure
- **Cloud Platform:** AWS/Azure/GCP
- **Container Orchestration:** Kubernetes
- **ML Platform:** MLflow, Kubeflow
- **Monitoring:** Prometheus, Grafana
- **Security:** SIEM integration, audit logging

   
