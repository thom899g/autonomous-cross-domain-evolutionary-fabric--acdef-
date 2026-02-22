"""
ACDEF Configuration Module
Centralized configuration management for the Autonomous Cross-Domain Evolutionary Fabric
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

@dataclass
class ACDEFConfig:
    """Configuration container for ACDEF system"""
    
    # System Configuration
    SYSTEM_NAME: str = "ACDEF"
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    
    # Firebase Configuration
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_PROJECT_ID: str = "acdef-evolution"
    FIRESTORE_COLLECTION_PREFIX: str = "acdef_"
    
    # RL Configuration
    RL_EXPLORATION_RATE: float = 0.3
    RL_LEARNING_RATE: float = 0.01
    RL_DISCOUNT_FACTOR: float = 0.95
    
    # Evolutionary Configuration
    EVOLUTION_POPULATION_SIZE: int = 50
    EVOLUTION_MUTATION_RATE: float = 0.1
    EVOLUTION_CROSSOVER_RATE: float = 0.7
    EVOLUTION_ELITISM_COUNT: int = 5
    
    # Domain Integration
    DOMAIN_SYNC_INTERVAL_SECONDS: int = 60
    MAX_DOMAIN_CONNECTIONS: int = 10
    
    # Performance Monitoring
    MONITORING_ENABLED: bool = True
    PERFORMANCE_WINDOW_SIZE: int = 100
    DECISION_THRESHOLD: float = 0.7
    
    # Network Configuration
    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: float = 1.0
    TIMEOUT_SECONDS: float = 30.0
    
    # Path Configuration
    DATA_DIR: str = "./data"
    LOGS_DIR: str = "./logs"
    MODELS_DIR: str = "./models"
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_config()
        
    def _validate_config(self) -> None:
        """Validate configuration values"""
        if not 0 <= self.RL_EXPLORATION_RATE <= 1:
            raise ValueError(f"RL_EXPLORATION_RATE must be between 0 and 1, got {self.RL_EXPLORATION_RATE}")
        
        if not 0 <= self.EVOLUTION_MUTATION_RATE <= 1:
            raise ValueError(f"EVOLUTION_MUTATION_RATE must be between 0 and 1, got {self.EVOLUTION_MUTATION_RATE}")
        
        if self.EVOLUTION_POPULATION_SIZE < 10:
            raise ValueError(f"EVOLUTION_POPULATION_SIZE must be at least 10, got {self.EVOLUTION_POPULATION_SIZE}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    def setup_directories(self) -> None:
        """Create necessary directories"""
        directories = [self.DATA_DIR, self.LOGS_DIR, self.MODELS_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# Global configuration instance
config = ACDEFConfig()

# Setup logging configuration
def setup_logging(config: ACDEFConfig) -> logging.Logger:
    """Configure and return logger instance"""
    log_level = getattr(logging, config.LOG_LEVEL)
    
    # Create logs directory if it doesn't exist
    os.makedirs(config.LOGS_DIR, exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{config.LOGS_DIR}/acdef.log"),
            logging.StreamHandler()
        ]
    )
    
    # Create module logger
    logger = logging.getLogger(config.SYSTEM_NAME)
    logger.info(f"{config.SYSTEM_NAME} v{config.VERSION} initialized")
    logger.info(f"Configuration loaded: {config.to_dict()}")
    
    return logger