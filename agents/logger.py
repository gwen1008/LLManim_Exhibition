# agents/logger.py
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

class SessionLogger:
    """
    Session-based logging system.
    Creates a new log file for each EMA run with timestamp and topic name.
    Automatically cleans up old logs.
    """
    def __init__(self, log_dir="logs", max_age_days=7, max_files=50):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.max_age_days = max_age_days
        self.max_files = max_files
        
        self.log_file = None
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        
    def start_session(self, topic="unknown"):
        """Start a new logging session with timestamped file."""
        # Clean up old logs first
        self._cleanup_old_logs()
        
        # Create log filename with timestamp and sanitized topic
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_topic = self._sanitize_filename(topic)
        log_filename = f"{timestamp}_{safe_topic}.log"
        log_path = self.log_dir / log_filename
        
        # Open log file
        self.log_file = open(log_path, 'w', encoding='utf-8')
        
        # Redirect stdout and stderr
        sys.stdout = TeeOutput(self.original_stdout, self.log_file)
        sys.stderr = TeeOutput(self.original_stderr, self.log_file)
        
        print(f"📝 Session log: {log_path}")
        return log_path
    
    def end_session(self):
        """End the current logging session and restore original streams."""
        if self.log_file:
            # Restore original streams
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr
            
            # Close log file
            self.log_file.close()
            self.log_file = None
    
    def _sanitize_filename(self, topic):
        """Convert topic to safe filename."""
        # Remove or replace unsafe characters
        safe = topic.replace(" ", "_").replace("/", "_").replace("\\", "_")
        safe = "".join(c for c in safe if c.isalnum() or c in "._-+")
        # Limit length
        return safe[:50]
    
    def _cleanup_old_logs(self):
        """Remove log files older than max_age_days or keep only max_files recent logs."""
        log_files = sorted(self.log_dir.glob("*.log"), key=os.path.getmtime, reverse=True)
        
        cutoff_date = datetime.now() - timedelta(days=self.max_age_days)
        
        removed_count = 0
        for i, log_file in enumerate(log_files):
            # Remove if too old
            file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            if file_time < cutoff_date:
                log_file.unlink()
                removed_count += 1
            # Remove if exceeds max_files (keep only the most recent max_files)
            elif i >= self.max_files:
                log_file.unlink()
                removed_count += 1
        
        if removed_count > 0:
            print(f"🧹 Cleaned up {removed_count} old log file(s)")


class TeeOutput:
    """Helper class to write to multiple streams simultaneously."""
    def __init__(self, *streams):
        self.streams = streams
    
    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()
    
    def flush(self):
        for stream in self.streams:
            stream.flush()
