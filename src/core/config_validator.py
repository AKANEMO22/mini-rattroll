from typing import Dict, Any

class ConfigValidator:
    """Validates YAML configs before system bootstrap."""
    @staticmethod
    def validate_main_config(config: Dict[str, Any]) -> bool:
        required_keys = ['data', 'model', 'adaptation']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config section: {key}")
        return True
