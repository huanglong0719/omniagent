import os
from typing import Optional, Dict, Any

class Config:
    """
    Configuration manager for OmniAgent.
    """
    def __init__(self):
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables and defaults."""
        return {
            'ENCRYPTION_KEY': os.getenv('ENCRYPTION_KEY', None),
            'LLM_PROVIDER': os.getenv('LLM_PROVIDER', 'google'),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY', None),
            'LONGCAT_API_KEY': os.getenv('LONGCAT_API_KEY', None),
            'PROXY_URL': os.getenv('HTTP_PROXY', None),
            'DB_PATH': os.getenv('DB_PATH', 'omniagent.db'),
            'VECTOR_DB_URL': os.getenv('VECTOR_DB_URL', 'http://localhost:6333'),
            'L1_MAX_SIZE': int(os.getenv('L1_MAX_SIZE', '100')),
            'L2_MAX_SIZE': int(os.getenv('L2_MAX_SIZE', '1000')),
            'PAGE_SIZE': int(os.getenv('PAGE_SIZE', '5')),
            'PREFETCH_LIMIT': int(os.getenv('PREFETCH_LIMIT', '3'))
        }

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value

    def update(self, config_dict: Dict[str, Any]) -> None:
        """Update multiple configuration values."""
        self._config.update(config_dict)

# Create a global config instance
config = Config()
