#!/usr/bin/env python3
"""
Automated threat validation for MLSecOps threat model.
Validates security controls and detects potential threats.
"""

import yaml
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatValidator:
    def __init__(self, threats_file: str = "threat-model/threats.yaml"):
        """Initialize threat validator with threat definitions."""
        self.threats_file = threats_file
        self.threats = self._load_threats()
        
    def _load_threats(self) -> Dict[str, Any]:
        """Load threat definitions from YAML file."""
        try:
            with open(self.threats_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Threats file not found: {self.threats_file}")
            return {}
    
    def validate_threat_coverage(self) -> Dict[str, Any]:
        """Validate that all threat categories are covered."""
        results = {
            "total_threats": len(self.threats.get('threats', [])),
            "coverage_analysis": {},
            "gaps": [],
            "recommendations": []
        }
        
        stride_categories = ['Spoofing', 'Tampering', 'Repudiation', 
                           'Information Disclosure', 'Denial of Service', 'Elevation of Privilege']
        
        covered_categories = set()
        
        for threat in self.threats.get('threats', []):
            stride_cat = threat.get('stride_category', 'Unknown')
            covered_categories.add(stride_cat)
            
            # Validate threat structure
            required_fields = ['id', 'name', 'likelihood', 'impact', 'business_impact']
            missing_fields = [field for field in required_fields if field not in threat]
            
            if missing_fields:
                results['gaps'].append({
                    'threat_id': threat.get('id', 'Unknown'),
                    'missing_fields': missing_fields
                })
        
        # Check STRIDE coverage
        uncovered_stride = set(stride_categories) - covered_categories
        if uncovered_stride:
            results['gaps'].append({
                'type': 'STRIDE Coverage Gap',
                'missing_categories': list(uncovered_stride)
            })
        
        results['coverage_analysis'] = {
            'covered_stride_categories': list(covered_categories),
            'coverage_percentage': (len(covered_categories) / len(stride_categories)) * 100
        }
        
        return results
    
    def calculate_risk_matrix(self) -> pd.DataFrame:
        """Calculate risk matrix from threat data."""
        threat_data = []
        
        for threat in self.threats.get('threats', []):
            threat_data.append({
                'ID': threat.get('id', ''),
                'Name': threat.get('name', ''),
                'Likelihood': threat.get('likelihood', ''),
                'Impact': threat.get('impact', ''),
                'Risk Score': threat.get('risk_score', 0),
                'Category': threat.get('category', ''),
                'Current Controls': threat.get('current_controls', ''),
                'Estimated Cost': threat.get('estimated_cost', '')
            })
        
        return pd.DataFrame(threat_data)
    
    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        coverage_results = self.validate_threat_coverage()
        risk_matrix = self.calculate_risk_matrix()
        
        # Calculate risk statistics
        high_risk_threats = risk_matrix[risk_matrix['Risk Score'] >= 7]
        medium_risk_threats = risk_matrix[(risk_matrix['Risk Score'] >= 4) & (risk_matrix['Risk Score'] < 7)]
        low_risk_threats = risk_matrix[risk_matrix['Risk Score'] < 4]
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'threat_coverage': coverage_results,
            'risk_statistics': {
                'high_risk_count': len(high_risk_threats),
                'medium_risk_count': len(medium_risk_threats),
                'low_risk_count': len(low_risk_threats),
                'total_estimated_cost': self._calculate_total_cost(),
                'average_risk_score': risk_matrix['Risk Score'].mean()
            },
            'high_priority_threats': high_risk_threats[['ID', 'Name', 'Risk Score', 'Estimated Cost']].to_dict('records'),
            'validation_status': 'PASSED' if not coverage_results['gaps'] else 'FAILED',
            'recommendations': self._generate_recommendations(coverage_results, risk_matrix)
        }
        
        return report
    
    def _calculate_total_cost(self) -> str:
        """Calculate total estimated cost for all security controls."""
        total = 0
        for threat in self.threats.get('threats', []):
            cost_str = threat.get('estimated_cost', '$0K')
            # Extract numeric value from cost string (e.g., '$500K' -> 500000)
            if cost_str.startswith('$') and cost_str.endswith('K'):
                total += int(cost_str[1:-1]) * 1000
        return f"${total:,}"
    
    def _generate_recommendations(self, coverage_results: Dict, risk_matrix: pd.DataFrame) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        if coverage_results['gaps']:
            recommendations.append("Address identified gaps in threat coverage and documentation")
        
        high_risk_count = len(risk_matrix[risk_matrix['Risk Score'] >= 7])
        if high_risk_count > 0:
            recommendations.append(f"Prioritize implementation of controls for {high_risk_count} high-risk threats")
        
        if coverage_results['coverage_analysis']['coverage_percentage'] < 100:
            recommendations.append("Expand threat model to cover all STRIDE categories")
        
        return recommendations

def main():
    """Main function to run threat validation."""
    logger.info("Starting threat validation...")
    
    validator = ThreatValidator()
    report = validator.generate_validation_report()
    
    # Save report to file
    with open('threat-validation-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Validation Status: {report['validation_status']}")
    logger.info(f"Total Threats: {report['threat_coverage']['total_threats']}")
    logger.info(f"High Risk Threats: {report['risk_statistics']['high_risk_count']}")
    logger.info(f"Total Estimated Cost: {report['risk_statistics']['total_estimated_cost']}")
    
    if report['recommendations']:
        logger.info("Recommendations:")
        for rec in report['recommendations']:
            logger.info(f"  - {rec}")
    
    return report['validation_status'] == 'PASSED'

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)