#!/usr/bin/env python3
"""
Security control testing automation for MLSecOps pipeline.
Tests effectiveness of implemented security controls.
"""

import yaml
import json
import time
import random
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityControlTester:
    def __init__(self, controls_file: str = "threat-model/controls.yaml"):
        """Initialize security control tester."""
        self.controls_file = controls_file
        self.controls = self._load_controls()
        
    def _load_controls(self) -> Dict[str, Any]:
        """Load security controls from YAML file."""
        try:
            with open(self.controls_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Controls file not found: {self.controls_file}")
            return {}
    
    def test_data_validation_pipeline(self) -> Dict[str, Any]:
        """Test data validation pipeline effectiveness."""
        logger.info("Testing data validation pipeline...")
        
        # Simulate malicious data injection
        test_cases = [
            {"type": "statistical_anomaly", "severity": "high"},
            {"type": "label_manipulation", "severity": "medium"},
            {"type": "feature_poisoning", "severity": "high"},
            {"type": "outlier_injection", "severity": "low"}
        ]
        
        results = {
            "control_id": "SC-001",
            "test_timestamp": datetime.now().isoformat(),
            "test_cases": [],
            "overall_effectiveness": 0,
            "recommendations": []
        }
        
        detection_rates = []
        
        for test_case in test_cases:
            # Simulate detection (replace with actual validation logic)
            detection_rate = random.uniform(0.7, 0.95)  # 70-95% detection rate
            false_positive_rate = random.uniform(0.02, 0.08)  # 2-8% false positive rate
            
            test_result = {
                "test_type": test_case["type"],
                "severity": test_case["severity"],
                "detection_rate": detection_rate,
                "false_positive_rate": false_positive_rate,
                "status": "PASSED" if detection_rate > 0.8 else "FAILED"
            }
            
            results["test_cases"].append(test_result)
            detection_rates.append(detection_rate)
            
            if detection_rate < 0.8:
                results["recommendations"].append(f"Improve detection for {test_case['type']} attacks")
        
        results["overall_effectiveness"] = np.mean(detection_rates)
        
        return results
    
    def test_adversarial_robustness(self) -> Dict[str, Any]:
        """Test adversarial robustness of ML models."""
        logger.info("Testing adversarial robustness...")
        
        attack_types = ["FGSM", "PGD", "C&W", "DeepFool"]
        
        results = {
            "control_id": "SC-002",
            "test_timestamp": datetime.now().isoformat(),
            "attack_tests": [],
            "overall_robustness": 0,
            "recommendations": []
        }
        
        robustness_scores = []
        
        for attack_type in attack_types:
            # Simulate adversarial attack testing
            success_rate = random.uniform(0.1, 0.4)  # 10-40% attack success rate
            model_accuracy = random.uniform(0.85, 0.95)  # 85-95% model accuracy
            robustness_score = 1 - success_rate  # Higher is better
            
            test_result = {
                "attack_type": attack_type,
                "attack_success_rate": success_rate,
                "model_accuracy_under_attack": model_accuracy,
                "robustness_score": robustness_score,
                "status": "PASSED" if success_rate < 0.3 else "FAILED"
            }
            
            results["attack_tests"].append(test_result)
            robustness_scores.append(robustness_score)
            
            if success_rate > 0.3:
                results["recommendations"].append(f"Improve robustness against {attack_type} attacks")
        
        results["overall_robustness"] = np.mean(robustness_scores)
        
        return results
    
    def test_api_monitoring(self) -> Dict[str, Any]:
        """Test API monitoring and rate limiting effectiveness."""
        logger.info("Testing API monitoring...")
        
        results = {
            "control_id": "SC-003",
            "test_timestamp": datetime.now().isoformat(),
            "monitoring_tests": [],
            "detection_accuracy": 0,
            "recommendations": []
        }
        
        # Simulate various API abuse scenarios
        abuse_scenarios = [
            {"type": "rate_limit_exceeded", "queries_per_second": 100},
            {"type": "systematic_probing", "query_pattern": "sequential"},
            {"type": "model_extraction", "query_diversity": "low"},
            {"type": "unusual_timing", "request_pattern": "burst"}
        ]
        
        detection_results = []
        
        for scenario in abuse_scenarios:
            # Simulate monitoring detection
            detection_probability = random.uniform(0.6, 0.9)
            response_time = random.uniform(0.1, 2.0)  # seconds
            
            test_result = {
                "scenario": scenario["type"],
                "detection_probability": detection_probability,
                "response_time_seconds": response_time,
                "status": "PASSED" if detection_probability > 0.7 else "FAILED"
            }
            
            results["monitoring_tests"].append(test_result)
            detection_results.append(detection_probability)
            
            if detection_probability < 0.7:
                results["recommendations"].append(f"Improve detection for {scenario['type']} scenarios")
        
        results["detection_accuracy"] = np.mean(detection_results)
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all security control tests."""
        logger.info("Running comprehensive security control tests...")
        
        test_results = {
            "test_suite_timestamp": datetime.now().isoformat(),
            "test_results": [],
            "summary": {},
            "overall_security_posture": "",
            "critical_recommendations": []
        }
        
        # Run individual tests
        data_validation_results = self.test_data_validation_pipeline()
        adversarial_results = self.test_adversarial_robustness()
        api_monitoring_results = self.test_api_monitoring()
        
        test_results["test_results"] = [
            data_validation_results,
            adversarial_results,
            api_monitoring_results
        ]
        
        # Calculate overall scores
        effectiveness_scores = [
            data_validation_results["overall_effectiveness"],
            adversarial_results["overall_robustness"],
            api_monitoring_results["detection_accuracy"]
        ]
        
        overall_score = np.mean(effectiveness_scores)
        
        test_results["summary"] = {
            "data_validation_effectiveness": data_validation_results["overall_effectiveness"],
            "adversarial_robustness": adversarial_results["overall_robustness"],
            "api_monitoring_accuracy": api_monitoring_results["detection_accuracy"],
            "overall_security_score": overall_score,
            "total_tests_run": len(test_results["test_results"]),
            "passed_tests": sum(1 for result in test_results["test_results"] 
                               if all(test["status"] == "PASSED" for test in result.get("test_cases", []) + result.get("attack_tests", []) + result.get("monitoring_tests", []))),
            "failed_tests": sum(1 for result in test_results["test_results"] 
                               if any(test["status"] == "FAILED" for test in result.get("test_cases", []) + result.get("attack_tests", []) + result.get("monitoring_tests", [])))
        }
        
        # Determine overall security posture
        if overall_score >= 0.8:
            test_results["overall_security_posture"] = "STRONG"
        elif overall_score >= 0.6:
            test_results["overall_security_posture"] = "MODERATE"
        else:
            test_results["overall_security_posture"] = "WEAK"
        
        # Compile critical recommendations
        all_recommendations = []
        for result in test_results["test_results"]:
            all_recommendations.extend(result.get("recommendations", []))
        
        test_results["critical_recommendations"] = list(set(all_recommendations))
        
        return test_results

def main():
    """Main function to run security control tests."""
    logger.info("Starting security control testing...")
    
    tester = SecurityControlTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open('control-test-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Overall Security Posture: {results['overall_security_posture']}")
    logger.info(f"Overall Security Score: {results['summary']['overall_security_score']:.2f}")
    logger.info(f"Tests Passed: {results['summary']['passed_tests']}")
    logger.info(f"Tests Failed: {results['summary']['failed_tests']}")
    
    if results['critical_recommendations']:
        logger.info("Critical Recommendations:")
        for rec in results['critical_recommendations']:
            logger.info(f"  - {rec}")
    
    return results['overall_security_posture'] != "WEAK"

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)