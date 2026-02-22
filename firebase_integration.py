"""
Firebase Integration Module for ACDEF
Provides state management, real-time data streaming, and decentralized coordination
"""

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from typing import Dict, Any, List, Optional, Tuple
import logging
import json
import time
from datetime import datetime
from dataclasses import dataclass, asdict
import threading

from config import config, setup_logging

logger = setup_logging(config)

@dataclass
class FirestoreDocument:
    """Base class for Firestore document structure"""
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to Firestore-compatible dictionary"""
        data = asdict(self)
        data['created_at'] = data['created_at'].isoformat()
        data['updated_at'] = data['updated_at'].isoformat()
        return {k: v for k, v in data.items() if v is not None}

class FirebaseManager:
    """
    Manages Firebase connection and operations with robust error handling
    and automatic reconnection capabilities
    """
    
    def __init__(self, credential_path: Optional[str] = None):
        """
        Initialize Firebase connection
        
        Args:
            credential_path: Path to Firebase service account credentials JSON file
        """
        self.credential_path = credential_path or config.FIREBASE_CREDENTIALS_PATH
        self.app: Optional[firebase_admin.App] = None
        self.db: Optional[FirestoreClient] = None
        self._initialized = False
        self._connection_lock = threading.Lock()
        
        # Connection monitoring
        self.last_heartbeat = datetime.utcnow()
        self.connection_attempts = 0
        self.max_retries = config.MAX_RETRIES
        
    def initialize(self) -> bool:
        """
        Initialize Firebase connection with retry logic
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        with self._connection_lock:
            if self._initialized and self.db is not None:
                logger.info("Firebase already initialized")
                return True
            
            try:
                # Check if Firebase app already exists
                if not firebase_admin._apps:
                    if self.cred