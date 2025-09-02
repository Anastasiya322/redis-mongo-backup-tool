import logging
import os
import shutil
import subprocess

from pymongo import MongoClient


logger = logging.getLogger(__name__)


class MongoBackupManager:
    """Manage backup/restore/clear operations for MongoDB databases.

    Uses the database name exactly as provided (no automatic prefixing).
    """

    def __init__(self, mongo_uri: str) -> None:
        self.mongo_uri = mongo_uri

    def clear(self, name: str) -> None:
        db_name = name
        try:
            with MongoClient(self.mongo_uri) as client:
                client.drop_database(db_name)
                logger.info("Dropped database: %s", db_name)
        except Exception as e:
            logger.error("Error dropping database %s: %s", db_name, e)

    def backup(self, name: str, backup_dir: str) -> None:
        db_name = name
        specific_backup_dir = os.path.join(backup_dir, db_name)

        if os.path.exists(specific_backup_dir):
            try:
                shutil.rmtree(specific_backup_dir)
                logger.info("Removed previous backup directory: %s", specific_backup_dir)
            except Exception as e:
                logger.error("Could not remove previous backup dir %s: %s", specific_backup_dir, e)

        os.makedirs(backup_dir, exist_ok=True)

        dump_command = [
            "mongodump",
            "--uri",
            self.mongo_uri,
            "--db",
            db_name,
            "--out",
            backup_dir,
        ]
        try:
            subprocess.run(dump_command, check=True)
            logger.info("Backup of database '%s' completed successfully.", db_name)
        except FileNotFoundError:
            logger.error("'mongodump' not found. Please install MongoDB Database Tools and ensure it's on PATH.")
        except subprocess.CalledProcessError as e:
            logger.error("Error occurred during mongodump: %s", e)

    def restore(self, name: str, backup_dir: str) -> None:
        db_name = self._full_db_name(name)
        specific_backup_dir = os.path.join(backup_dir, db_name)

        if not os.path.exists(specific_backup_dir):
            logger.error("No backup found at '%s'. Restoration aborted.", specific_backup_dir)
            return

        restore_command = [
            "mongorestore",
            "--uri",
            self.mongo_uri,
            "--db",
            db_name,
            "--drop",
            specific_backup_dir,
        ]
        try:
            subprocess.run(restore_command, check=True)
            logger.info("Restoration of database '%s' completed successfully.", db_name)
        except FileNotFoundError:
            logger.error("'mongorestore' not found. Please install MongoDB Database Tools and ensure it's on PATH.")
        except subprocess.CalledProcessError as e:
            logger.error("Error occurred during mongorestore: %s", e)
