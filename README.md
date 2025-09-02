# Redis & Mongo Backup Tool

A small, modular CLI to back up, restore, and clear Redis keyspaces (by pattern) and MongoDB databases. It wraps Redis operations in Python and shells out to MongoDB Database Tools (`mongodump`/`mongorestore`).

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

## Features
- Backup and restore Redis keys by pattern (supports `*` wildcard)
- Drop/backup/restore MongoDB databases by exact name
- Environment-based configuration (no secrets in code)
- Simple, readable structure with clear entrypoint

## Requirements
- Python 3.9+
- Redis server (for Redis operations)
- MongoDB Database Tools installed and on PATH for Mongo operations:
  - `mongodump`
  - `mongorestore`

## Installation
```
# clone the repo
git clone https://github.com/dibbed/redis-mongo-backup-tool.git
cd redis-mongo-backup-tool

# optional: create a virtual environment
python -m venv .venv
# Windows
. .venv\\Scripts\\activate
# Linux/macOS
# source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Usage
```
python main.py --help
```

### Redis
```
# Backup keys matching pattern (use * wildcard). Always quote patterns in shell.
python main.py redis backup --pattern "myapp:*" --backup-dir backups --redis-url redis://localhost:6379/0

# Clear all keys matching pattern (quoted)
python main.py redis clear --pattern "myapp:*" --redis-url redis://localhost:6379/0

# Restore from backups/<sanitized-pattern>.json (quoted)
python main.py redis restore --pattern "myapp:*" --backup-dir backups --redis-url redis://localhost:6379/0
```

### MongoDB
Uses the database name exactly as provided. Avoid spaces in DB names. If you must include spaces, wrap the value in quotes.
```
# Backup database `my app` into ./backups (quoted)
python main.py mongo backup --name "my app" --backup-dir backups --mongo-uri mongodb://localhost:27017/

# Drop database `myapp`
python main.py mongo clear --name myapp --mongo-uri mongodb://localhost:27017/

# Restore from ./backups/my app (quoted)
python main.py mongo restore --name "my app" --backup-dir backups --mongo-uri mongodb://localhost:27017/
```

## Configuration
This project does not require a `.env` file. You can optionally set environment variables to configure connections and locations:
- `REDIS_URL` (default: `redis://localhost:6379/0`)
- `MONGODB_URI` (default: `mongodb://localhost:27017/`)
- `BACKUP_DIR` (default: `backups`)
- `LOG_LEVEL` (default: `INFO`)
- `LOG_FILE` (default: `debug.log`, logs also go to console)

Use CLI flags to override per command if preferred.

## Project Structure
```
.
├─ backup_tool/
│  ├─ config.py            # Env-based configuration helpers
│  ├─ mongo_manager.py     # Mongo backup/restore/clear
│  ├─ redis_manager.py     # Redis backup/restore/clear
│  └─ utils.py             # Logging + exception helpers
├─ main.py                 # CLI entrypoint
├─ requirements.txt        # Python dependencies
├─ .gitignore              # Ignore common Python artifacts
├─ LICENSE                 # MIT license
└─ README.md               # This file
```

## Contributing
- Open an issue to discuss planned changes
- Keep PRs focused and small
- Follow existing code style and structure

## License
MIT. See `LICENSE` for details.

## Contact
- GitHub: https://github.com/dibbed
