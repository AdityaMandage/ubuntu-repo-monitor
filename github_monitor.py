#!/usr/bin/env python3
"""
GitHub Actions Ubuntu Repository Monitor
Runs in GitHub Actions cloud environment with optional email notifications
"""

import requests
import re
import json
import os
from datetime import datetime, timezone
from pathlib import Path

class GitHubRepoMonitor:
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Repository URLs to monitor
        self.repos = {
            'noble-main': 'https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/',
            'noble-updates': 'https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/',
            'noble-security': 'https://archive.ubuntu.com/ubuntu/dists/noble-security/main/binary-amd64/'
        }
        
        # Log files
        self.log_files = {
            repo: self.log_dir / f"{repo}_updates.log"
            for repo in self.repos
        }
        self.summary_log = self.log_dir / "update_summary.log"
        self.state_file = self.log_dir / "last_state.json"
        
        self.load_state()
        self.updates_detected = []

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
            pattern = r'<a href="Packages\.gz">Packages\.gz</a>.*?<td align="right">([\d-]+\s+[\d:]+)\s*</td>'
            match = re.search(pattern, response.text, re.DOTALL)
            
            if match:
                timestamp_str = match.group(1).strip()
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
        
        # Create log entry
        if is_new_update:
            log_entry = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}] 🆕 UPDATE DETECTED! Packages.gz modified: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}"
            self.updates_detected.append(f"{repo_name}: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
        else:
            log_entry = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}] 📊 Check: Packages.gz last modified: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}"
        
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

    def create_github_issue_if_updates(self):
        """Create a GitHub issue if updates were detected"""
        if not self.updates_detected:
            return
            
        # This would require GitHub token and repo setup
        # For now, just print the notification
        print("\n🚨 NOTIFICATION: Updates detected!")
        for update in self.updates_detected:
            print(f"  - {update}")

    def check_repositories(self):
        """Check all repositories for updates"""
        print(f"🔍 Checking repositories at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} (GitHub Actions)")
        
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
                    # First time seeing this repo (don't count as update in GitHub Actions)
                    pass
                
                # Log the result
                self.log_update(repo_name, timestamp, is_new_update)
                
                # Update state
                self.last_state[repo_name] = timestamp.isoformat()
        
        # Save updated state
        self.save_state()
        
        # Create notification if updates detected
        self.create_github_issue_if_updates()

if __name__ == "__main__":
    monitor = GitHubRepoMonitor()
    monitor.check_repositories()
