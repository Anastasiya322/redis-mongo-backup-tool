import os
from pathlib import Path


def get_redis_url() -> str:
    """Return Redis connection URL from environment or default."""
    return os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_mongo_uri() -> str:
    """Return MongoDB connection URI from environment or default."""
    return os.getenv("MONGODB_URI", "mongodb://localhost:27017/")


def get_backup_dir() -> str:
    """Return backup directory path from environment or default."""
    return os.getenv("BACKUP_DIR", "backups")


def ensure_dir(path: str) -> str:
    """Create the directory if it doesn't exist and return the path."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

