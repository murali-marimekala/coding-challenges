"""
Config loader for algorithm definitions
Handles YAML parsing and configuration management
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any


class AlgorithmConfigLoader:
    """Load and manage algorithm configurations from YAML files"""
    
    def __init__(self, algorithms_dir: str = None):
        """
        Initialize config loader
        
        Args:
            algorithms_dir: Path to algorithms directory (defaults to current structure)
        """
        if algorithms_dir is None:
            # Default to algorithms directory relative to this file
            current_dir = Path(__file__).parent.parent
            algorithms_dir = str(current_dir / "algorithms")
        
        self.algorithms_dir = algorithms_dir
        self.configs = {}
        self._load_all_configs()
    
    def _load_all_configs(self):
        """Scan and load all algorithm configs"""
        if not os.path.exists(self.algorithms_dir):
            return
        
        for algorithm_name in os.listdir(self.algorithms_dir):
            algorithm_path = os.path.join(self.algorithms_dir, algorithm_name)
            config_file = os.path.join(algorithm_path, "config.yaml")
            
            if os.path.isfile(config_file):
                try:
                    with open(config_file, 'r') as f:
                        config = yaml.safe_load(f)
                        self.configs[algorithm_name] = config
                except Exception as e:
                    print(f"Error loading {config_file}: {e}")
    
    def get_config(self, algorithm_id: str) -> Dict[str, Any]:
        """Get configuration for specific algorithm"""
        return self.configs.get(algorithm_id, {})
    
    def list_algorithms(self) -> list:
        """List all available algorithms"""
        return list(self.configs.keys())
    
    def get_difficulty_cases(self, algorithm_id: str, difficulty: str = "easy") -> list:
        """Get test cases for specific difficulty level"""
        config = self.get_config(algorithm_id)
        difficulty_data = config.get("difficulty_levels", {}).get(difficulty, {})
        return difficulty_data.get("test_cases", [])
    
    def get_learning_objectives(self, algorithm_id: str) -> list:
        """Get learning objectives for algorithm"""
        config = self.get_config(algorithm_id)
        return config.get("learning_objectives", [])
    
    def get_complexity(self, algorithm_id: str) -> Dict[str, Any]:
        """Get complexity information"""
        config = self.get_config(algorithm_id)
        return config.get("complexity", {})


# Singleton instance
_loader = None

def get_config_loader(algorithms_dir: str = None) -> AlgorithmConfigLoader:
    """Get or create config loader singleton"""
    global _loader
    if _loader is None:
        _loader = AlgorithmConfigLoader(algorithms_dir)
    return _loader
