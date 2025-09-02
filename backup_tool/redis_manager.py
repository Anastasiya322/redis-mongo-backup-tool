import base64
try:  # Prefer ujson for speed; fallback to stdlib json
    import ujson as json  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - fallback
    import json  # type: ignore[no-redef]
import logging
import os
from typing import Dict, Generator, Iterable, List

import redis


logger = logging.getLogger(__name__)


class RedisBackupManager:
    """Manage backup/restore/clear operations for Redis keys by pattern.

    Pattern is passed directly to SCAN's `match` (supports `*` wildcard, etc.).
    """

    def __init__(self, redis_url: str, decode_responses: bool = True) -> None:
        self.client = redis.Redis.from_url(redis_url, decode_responses=decode_responses)

    def _scan_keys(self, pattern: str) -> Generator[str, None, None]:
        cursor = 0
        while True:
            cursor, keys = self.client.scan(cursor=cursor, match=pattern)
            for key in keys:
                yield key
            if cursor == 0:
                break

    @staticmethod
    def _pattern_to_filename(pattern: str) -> str:
        import re
        import hashlib

        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", pattern).strip("_")
        if not safe:
            safe = "pattern"
        if len(safe) > 64:
            safe = f"{safe[:64]}_{hashlib.sha1(pattern.encode()).hexdigest()[:8]}"
        return f"{safe}.json"

    def backup(self, pattern: str, backup_dir: str) -> List[str]:
        """Backup keys matching the given SCAN pattern to JSON in backup_dir."""
        keys = list(self._scan_keys(pattern))
        logger.info("Found %d keys for pattern '%s'", len(keys), pattern)

        backup_data: Dict[str, Dict[str, object]] = {}

        for key in keys:
            try:
                dumped_value = self.client.dump(key)  # bytes
                ttl = self.client.pttl(key)  # milliseconds, -1 no expire, -2 no key
                ttl = int(ttl) if ttl is not None else -1

                backup_data[str(key)] = {
                    "value": base64.b64encode(dumped_value).decode("utf-8"),
                    "ttl": ttl,
                }
            except Exception as e:
                logger.error("Error dumping key %s: %s", key, e)

        os.makedirs(backup_dir, exist_ok=True)
        out_path = os.path.join(backup_dir, self._pattern_to_filename(pattern))
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                try:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                except TypeError:
                    # Some json backends may not support indent/ensure_ascii
                    json.dump(backup_data, f)
            logger.info("Backup written: %s", out_path)
        except Exception as e:
            logger.error("Error saving backup file %s: %s", out_path, e)

        return keys

    def clear_by_pattern(self, pattern: str) -> int:
        """Delete all keys matching the given pattern. Returns number deleted."""
        keys = list(self._scan_keys(pattern))
        return self.clear_keys(keys)

    def clear_keys(self, keys: Iterable[str]) -> int:
        keys_list = list(keys)
        if not keys_list:
            logger.info("No keys to delete.")
            return 0
        pipe = self.client.pipeline()
        for k in keys_list:
            pipe.delete(k)
        results = pipe.execute()
        deleted = sum(1 for r in results if isinstance(r, int) and r > 0)
        logger.info("Deleted %d/%d keys", deleted, len(keys_list))
        return deleted

    def restore(self, pattern: str, backup_dir: str) -> None:
        """Restore keys from backup file derived from pattern.

        Looks for backup at backup_dir/<sanitized(pattern)>.json
        """
        path = os.path.join(backup_dir, self._pattern_to_filename(pattern))
        if not os.path.exists(path):
            logger.error("Backup file not found: %s", path)
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
        except Exception as e:
            logger.error("Error reading backup file %s: %s", path, e)
            return

        pipe = self.client.pipeline()
        for key, data in backup_data.items():
            try:
                binary_value = base64.b64decode(data["value"])  # bytes
                ttl = int(data.get("ttl", 0))
                ttl = ttl if ttl and ttl > 0 else 0
                pipe.restore(key, ttl, binary_value, replace=True)
            except redis.exceptions.ResponseError as e:
                logger.error("RESTORE error for key %s: %s", key, e)
            except Exception as e:
                logger.error("Error preparing key %s for restore: %s", key, e)

        try:
            pipe.execute()
            logger.info("Restore completed from %s", path)
        except redis.exceptions.ResponseError as e:
            logger.error("Error executing restore pipeline: %s", e)
