import argparse
import logging

from backup_tool.config import (
    ensure_dir,
    get_backup_dir,
    get_mongo_uri,
    get_redis_url,
)
from backup_tool.mongo_manager import MongoBackupManager
from backup_tool.redis_manager import RedisBackupManager
from backup_tool.utils import setup_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Redis & MongoDB backup/restore/clear utility",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )

    subparsers = parser.add_subparsers(dest="service", required=True)

    # Redis commands
    redis_parser = subparsers.add_parser("redis", help="Redis operations")
    redis_sub = redis_parser.add_subparsers(dest="action", required=True)

    r_common = [
        dict(
            name=["--pattern", "--prefix"],
            kwargs=dict(
                dest="pattern",
                required=True,
                help=(
                    "Key pattern for SCAN (supports *). Quote in shell, e.g. "
                    "'myapp:*'"
                ),
            ),
        ),
        dict(
            name="--backup-dir",
            kwargs=dict(default=get_backup_dir(), help="Backup directory"),
        ),
        dict(
            name="--redis-url",
            kwargs=dict(default=get_redis_url(), help="Redis connection URL"),
        ),
    ]

    r_backup = redis_sub.add_parser("backup", help="Backup Redis keys by prefix")
    for arg in r_common:
        name = arg["name"]
        if isinstance(name, list):
            r_backup.add_argument(*name, **arg["kwargs"])  # type: ignore[arg-type]
        else:
            r_backup.add_argument(name, **arg["kwargs"])  # type: ignore[arg-type]

    r_clear = redis_sub.add_parser("clear", help="Delete Redis keys by prefix")
    for arg in r_common:
        # clear doesn't need backup dir but harmless to accept
        name = arg["name"]
        if isinstance(name, list):
            r_clear.add_argument(*name, **arg["kwargs"])  # type: ignore[arg-type]
        else:
            r_clear.add_argument(name, **arg["kwargs"])  # type: ignore[arg-type]

    r_restore = redis_sub.add_parser("restore", help="Restore Redis keys from backup")
    for arg in r_common:
        name = arg["name"]
        if isinstance(name, list):
            r_restore.add_argument(*name, **arg["kwargs"])  # type: ignore[arg-type]
        else:
            r_restore.add_argument(name, **arg["kwargs"])  # type: ignore[arg-type]

    # Mongo commands
    mongo_parser = subparsers.add_parser("mongo", help="MongoDB operations")
    mongo_sub = mongo_parser.add_subparsers(dest="action", required=True)

    m_common = [
        dict(
            name="--name",
            kwargs=dict(
                required=True,
                help="Database name (exact). Avoid spaces; quote if needed.",
            ),
        ),
        dict(
            name="--backup-dir",
            kwargs=dict(default=get_backup_dir(), help="Backup directory"),
        ),
        dict(
            name="--mongo-uri",
            kwargs=dict(default=get_mongo_uri(), help="MongoDB connection URI"),
        ),
    ]

    m_backup = mongo_sub.add_parser("backup", help="Backup MongoDB database")
    for arg in m_common:
        m_backup.add_argument(arg["name"], **arg["kwargs"])  # type: ignore[arg-type]

    m_clear = mongo_sub.add_parser("clear", help="Drop MongoDB database")
    for arg in m_common:
        # clear doesn't need backup dir but harmless to accept
        m_clear.add_argument(arg["name"], **arg["kwargs"])  # type: ignore[arg-type]

    m_restore = mongo_sub.add_parser("restore", help="Restore MongoDB database from backup")
    for arg in m_common:
        m_restore.add_argument(arg["name"], **arg["kwargs"])  # type: ignore[arg-type]

    return parser


def handle_redis(args: argparse.Namespace) -> None:
    mgr = RedisBackupManager(args.redis_url)
    if args.action == "backup":
        ensure_dir(args.backup_dir)
        keys = mgr.backup(args.pattern, args.backup_dir)
        logging.info("Backed up %d keys for pattern '%s'", len(keys), args.pattern)
    elif args.action == "clear":
        deleted = mgr.clear_by_pattern(args.pattern)
        logging.info("Deleted %d keys for pattern '%s'", deleted, args.pattern)
    elif args.action == "restore":
        mgr.restore(args.pattern, args.backup_dir)
    else:
        raise ValueError(f"Unknown redis action: {args.action}")


def handle_mongo(args: argparse.Namespace) -> None:
    mgr = MongoBackupManager(args.mongo_uri)
    if args.action == "backup":
        ensure_dir(args.backup_dir)
        mgr.backup(args.name, args.backup_dir)
    elif args.action == "clear":
        mgr.clear(args.name)
    elif args.action == "restore":
        mgr.restore(args.name, args.backup_dir)
    else:
        raise ValueError(f"Unknown mongo action: {args.action}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    setup_logging(args.log_level)

    if args.service == "redis":
        handle_redis(args)
    elif args.service == "mongo":
        handle_mongo(args)
    else:
        parser.error("Unknown service")


if __name__ == "__main__":
    main()
