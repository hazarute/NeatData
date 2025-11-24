"""
Security Module
===============
API Key authentication ve authorization yönetimi.
"""

from fastapi import HTTPException, Header, Depends
from typing import Optional
from datetime import datetime, timedelta
import uuid
import json
from pathlib import Path

# API Keys storage dosyası
KEYS_FILE = Path("api_keys.json")


class APIKey:
    """API Key yönetimi."""
    
    def __init__(self, key: str, name: str, created_at: str, expires_at: Optional[str] = None):
        self.key = key
        self.name = name
        self.created_at = created_at
        self.expires_at = expires_at
        self.active = True
    
    def is_valid(self) -> bool:
        """Key'in geçerli olup olmadığını kontrol et."""
        if not self.active:
            return False
        
        if self.expires_at:
            expires = datetime.fromisoformat(self.expires_at)
            if datetime.utcnow() > expires:
                return False
        
        return True
    
    def to_dict(self) -> dict:
        """Serialize to dict."""
        return {
            "key": self.key,
            "name": self.name,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "active": self.active
        }


class APIKeyManager:
    """API Key manager - persistent storage."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._keys = {}
        self._load_keys()
        self._initialized = True
    
    def _load_keys(self):
        """Dosyadan key'leri yükle veya default key'ler oluştur."""
        if KEYS_FILE.exists():
            try:
                with open(KEYS_FILE, 'r') as f:
                    data = json.load(f)
                    for key_str, key_data in data.items():
                        self._keys[key_str] = APIKey(**key_data)
            except Exception as e:
                print(f"Error loading keys: {e}. Creating default keys...")
                self._create_default_keys()
        else:
            self._create_default_keys()
    
    def _create_default_keys(self):
        """Default test key'leri oluştur."""
        # Test key 1: Never expires
        test_key_1 = str(uuid.uuid4())
        self._keys[test_key_1] = APIKey(
            key=test_key_1,
            name="test-key-1",
            created_at=datetime.utcnow().isoformat(),
            expires_at=None
        )
        
        # Test key 2: Expires in 1 year
        expires = datetime.utcnow() + timedelta(days=365)
        test_key_2 = str(uuid.uuid4())
        self._keys[test_key_2] = APIKey(
            key=test_key_2,
            name="test-key-2",
            created_at=datetime.utcnow().isoformat(),
            expires_at=expires.isoformat()
        )
        
        self._save_keys()
        print(f"Default API keys created:")
        print(f"  Key 1 (no expiry): {test_key_1}")
        print(f"  Key 2 (expires {expires.date()}): {test_key_2}")
    
    def _save_keys(self):
        """Key'leri dosyaya kaydet."""
        try:
            with open(KEYS_FILE, 'w') as f:
                data = {key: key_obj.to_dict() for key, key_obj in self._keys.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving keys: {e}")
    
    def get_key(self, key: str) -> Optional[APIKey]:
        """Key'i al."""
        return self._keys.get(key)
    
    def create_key(self, name: str, expires_in_days: Optional[int] = None) -> str:
        """Yeni key oluştur."""
        new_key = str(uuid.uuid4())
        expires_at = None
        
        if expires_in_days:
            expires = datetime.utcnow() + timedelta(days=expires_in_days)
            expires_at = expires.isoformat()
        
        self._keys[new_key] = APIKey(
            key=new_key,
            name=name,
            created_at=datetime.utcnow().isoformat(),
            expires_at=expires_at
        )
        
        self._save_keys()
        return new_key
    
    def revoke_key(self, key: str) -> bool:
        """Key'i devre dışı bırak."""
        if key in self._keys:
            self._keys[key].active = False
            self._save_keys()
            return True
        return False
    
    def list_keys(self) -> dict:
        """Tüm key'leri listele."""
        return {key: key_obj.to_dict() for key, key_obj in self._keys.items()}


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    API Key'i doğrula.
    
    Args:
        x_api_key: Request header'dan alınan API Key
    
    Returns:
        Valid API key string
    
    Raises:
        HTTPException: Key geçersiz, süresi dolmuş veya eksik
    """
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Please provide X-API-Key header."
        )
    
    manager = APIKeyManager()
    api_key = manager.get_key(x_api_key)
    
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key."
        )
    
    if not api_key.is_valid():
        raise HTTPException(
            status_code=401,
            detail="API key is invalid or expired."
        )
    
    return x_api_key


# Dependency for optional API key (public endpoints)
async def verify_api_key_optional(x_api_key: Optional[str] = Header(None)) -> Optional[str]:
    """
    API Key'i isteğe bağlı doğrula.
    
    Args:
        x_api_key: Request header'dan alınan API Key (opsiyonel)
    
    Returns:
        Valid API key string or None
    """
    if not x_api_key:
        return None
    
    manager = APIKeyManager()
    api_key = manager.get_key(x_api_key)
    
    if api_key and api_key.is_valid():
        return x_api_key
    
    return None
