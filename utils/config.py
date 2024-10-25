import yaml
from typing import Dict, List, Optional

class ConfigHandler:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.default_settings = self.config.get('exchanges', {}).get('default', {})

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def is_enabled(self, exchange_name: str) -> bool:
        """Check if specific exchange is enabled"""
        exchange_config = self.config.get('exchanges', {}).get(exchange_name, {})
        return exchange_config.get('enabled', self.default_settings.get('enabled', False))

    def get_enabled_exchanges(self) -> List[str]:
        """Get list of all enabled exchanges"""
        return [
            name for name, _ in self.config.get('exchanges', {}).items()
            if name != 'default' and self.is_enabled(name)
        ]

    def get_exchanges(self ):
        return self.config.get('exchanges', {})

    def get_exchange_config(self, exchange_name: str) -> Dict:
        """Get complete config for an exchange (with defaults applied)"""
        exchange_specific = self.config.get('exchanges', {}).get(exchange_name, {})
        # Merge default settings with exchange-specific settings
        return {**self.default_settings, **exchange_specific}

    def get_trading_pairs(self, exchange_name: str) -> List[str]:
        """Get trading pairs for specific exchange"""
        config = self.get_exchange_config(exchange_name)
        return config.get('trading_pairs', [])