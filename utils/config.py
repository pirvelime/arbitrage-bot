import yaml
import os
from typing import Any, Dict, List, Optional


class ConfigHandler:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self._apply_env_overrides()

    def get_exchanges(self ):
        return self.config.get('exchanges', {})

    def is_enabled(self, exchange_name: str) -> bool:
        """Check if specific exchange is enabled"""
        exchange_config = self.config.get('exchanges', {}).get(exchange_name, {})
        return exchange_config.get('enabled')

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides for exchange status"""
        for exchange in self.config.get('exchanges', {}):
            if exchange == 'default':
                continue
            env_var = f"{exchange.upper()}_ENABLED"
            if env_var in os.environ:
                enabled = os.environ[env_var].lower() == 'true'
                self.config['exchanges'][exchange]['enabled'] = enabled

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation path
        Examples:
            - get('exchanges.binance.enabled')
            - get('trading.min_order_size', 0.0001)
            - get('exchanges.binance.trading_pairs', [])
        """
        keys = path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default

        return value if value is not None else default

    def is_exchange_enabled(self, exchange: str) -> bool:
        """Check if specific exchange is enabled"""
        if exchange == 'default':
            return False

        default_enabled = self.get('exchanges.default.enabled', False)
        return self.get(f'exchanges.{exchange}.enabled', default_enabled)

    def get_enabled_exchanges(self) -> List[str]:
        """Get list of enabled exchanges"""
        return [
            name for name in self.get('exchanges', {}).keys()
            if name != 'default' and self.is_exchange_enabled(name)
        ]

    def get_exchange_config(self, exchange: str) -> Dict:
        """Get complete exchange config with defaults applied"""
        default_config = self.get('exchanges.default', {})
        exchange_config = self.get(f'exchanges.{exchange}', {})
        return {**default_config, **exchange_config}

    def __getitem__(self, path: str) -> Any:
        """Allow dictionary-like access using square brackets"""
        return self.get(path)