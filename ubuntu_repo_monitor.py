#!/usr/bin/env python3
"""
Ubuntu Repository Update Monitor
Tracks when Ubuntu Noble repositories get updated by monitoring Packages.gz timestamps
"""

import requests
import re
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import sys

class UbuntuRepoMonitor:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Repository URLs to monitor
        self.repos = {
            'noble-main': 'https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/',
            'noble-updates': 'https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/',
            'noble-security': 'https://archive.ubuntu.com/ubuntu/dists/noble-security/main/binary-amd64/'
        }
        
        # Log files for each repository
        self.log_files = {
            repo: self.log_dir / f"{repo}_updates.log"
            for repo in self.repos
        }
        
        # Master summary log
        self.summary_log = self.log_dir / "update_summary.log"
        
        # State file to track last known timestamps
        self.state_file = self.log_dir / "last_state.json"
        
        self.load_state()

    def load_state(self):
        """Load the last known state from file"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    self.last_state = json.load(f)
            else:
                self.last_state = {}
        except Exception as e:
            print(f"Error loading state: {e}")
            self.last_state = {}

    def save_state(self):
        """Save current state to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.last_state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")

    def get_packages_timestamp(self, url):
        """Extract the last modified timestamp of Packages.gz from repository HTML"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Look for Packages.gz line in the HTML
            # Example: <td align="right">2025-08-09 08:38  </td><td align="right">1.6M</td></tr>
            pattern = r'<a href="Packages\.gz">Packages\.gz</a>.*?<td align="right">([\d-]+\s+[\d:]+)\s*</td>'
            match = re.search(pattern, response.text, re.DOTALL)
            
            if match:
                timestamp_str = match.group(1).strip()
                # Convert to datetime object
                dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
                return dt.replace(tzinfo=timezone.utc)
            else:
                print(f"Could not find Packages.gz timestamp in {url}")
                return None
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def log_update(self, repo_name, timestamp, is_new_update=False):
        """Log an update to the appropriate files"""
        current_time = datetime.now(timezone.utc)
        
        # Log to individual repository file
        log_entry = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}] "
        if is_new_update:
            log_entry += f"🆕 UPDATE DETECTED! Packages.gz modified: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}"
        else:
            log_entry += f"📊 Check: Packages.gz last modified: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}"
        
        # Write to individual repo log
        with open(self.log_files[repo_name], 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
        
        # Write to summary log if it's an update
        if is_new_update:
            summary_entry = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}] {repo_name}: UPDATE - Packages.gz modified at {timestamp.strftime('%Y-%m-%d %H:%M UTC')}"
            with open(self.summary_log, 'a', encoding='utf-8') as f:
                f.write(summary_entry + '\n')
            print(f"🆕 NEW UPDATE DETECTED in {repo_name}!")
        
        print(f"✓ {repo_name}: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")

    def check_repositories(self):
        """Check all repositories for updates"""
        print(f"\n🔍 Checking repositories at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}...")
        
        for repo_name, repo_url in self.repos.items():
            timestamp = self.get_packages_timestamp(repo_url)
            
            if timestamp:
                # Check if this is a new update
                last_known = self.last_state.get(repo_name)
                is_new_update = False
                
                if last_known:
                    last_dt = datetime.fromisoformat(last_known.replace('Z', '+00:00'))
                    if timestamp > last_dt:
                        is_new_update = True
                else:
                    # First time seeing this repo
                    is_new_update = True
                
                # Log the result
                self.log_update(repo_name, timestamp, is_new_update)
                
                # Update state
                self.last_state[repo_name] = timestamp.isoformat()
            
            # Small delay between requests to be nice to the server
            time.sleep(1)
        
        # Save updated state
        self.save_state()

    def run_continuous(self, check_interval_minutes=30):
        """Run continuous monitoring"""
        print(f"🚀 Starting Ubuntu Repository Monitor")
        print(f"📁 Logs will be saved to: {self.log_dir.absolute()}")
        print(f"⏰ Check interval: {check_interval_minutes} minutes")
        print(f"🎯 Monitoring repositories:")
        for name, url in self.repos.items():
            print(f"   • {name}: {url}")
        
        print("\nPress Ctrl+C to stop...")
        
        try:
            while True:
                self.check_repositories()
                
                # Wait for next check
                next_check = datetime.now(timezone.utc) + timedelta(minutes=check_interval_minutes)
                print(f"⏳ Next check at: {next_check.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                
                time.sleep(check_interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Error in continuous monitoring: {e}")

    def run_single_check(self):
        """Run a single check"""
        print("🔍 Running single check...")
        self.check_repositories()
        print("✅ Check complete!")

if __name__ == "__main__":
    from datetime import timedelta
    
    monitor = UbuntuRepoMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Single check mode
        monitor.run_single_check()
    else:
        # Continuous monitoring mode
        # Default: check every 30 minutes
        interval = 30
        if len(sys.argv) > 1:
            try:
                interval = int(sys.argv[1])
            except ValueError:
                print("Invalid interval, using 30 minutes")
        
        monitor.run_continuous(interval)
