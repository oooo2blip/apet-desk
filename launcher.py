import subprocess
import sys
import time
import os
from typing import Optional


class PetLauncher:
    MAX_RESTARTS = 5
    RESTART_DELAY = 2
    WATCHDOG_INTERVAL = 1
    
    def __init__(self):
        self._process: Optional[subprocess.Popen] = None
        self._restart_count: int = 0
        self._is_running: bool = True
        self._script_path: str = self._get_main_script_path()
    
    def _get_main_script_path(self) -> str:
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            main_script = os.path.join(application_path, 'main.py')
            if os.path.exists(main_script):
                return main_script
            return sys.executable
        else:
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    
    def _start_process(self) -> bool:
        try:
            if getattr(sys, 'frozen', False):
                if self._script_path.endswith('.exe'):
                    self._process = subprocess.Popen(
                        [self._script_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                    )
                else:
                    python_exe = sys.executable
                    self._process = subprocess.Popen(
                        [python_exe, self._script_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                    )
            else:
                python_exe = sys.executable
                self._process = subprocess.Popen(
                    [python_exe, self._script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )
            return True
        except Exception as e:
            print(f"Failed to start process: {e}")
            return False
    
    def _stop_process(self):
        if self._process is not None:
            try:
                self._process.terminate()
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    self._process.kill()
                except Exception:
                    pass
            except Exception:
                pass
            finally:
                self._process = None
    
    def _is_process_alive(self) -> bool:
        if self._process is None:
            return False
        return self._process.poll() is None
    
    def _get_exit_code(self) -> Optional[int]:
        if self._process is None:
            return None
        return self._process.poll()
    
    def _should_restart(self, exit_code: Optional[int]) -> bool:
        if exit_code is None:
            return False
        
        if exit_code == 0:
            return False
        
        if self._restart_count >= self.MAX_RESTARTS:
            print(f"Maximum restart count ({self.MAX_RESTARTS}) reached. Giving up.")
            return False
        
        return True
    
    def _wait_for_restart(self):
        print(f"Waiting {self.RESTART_DELAY} seconds before restart...")
        time.sleep(self.RESTART_DELAY)
    
    def run(self):
        print("Starting Desktop Pet Launcher...")
        print(f"Target script: {self._script_path}")
        print("Press Ctrl+C to stop the launcher.")
        print("=" * 50)
        
        try:
            while self._is_running:
                if not self._is_process_alive():
                    exit_code = self._get_exit_code()
                    
                    if exit_code is not None:
                        print(f"\nProcess exited with code: {exit_code}")
                        
                        if self._should_restart(exit_code):
                            self._restart_count += 1
                            print(f"Restarting... (Attempt {self._restart_count}/{self.MAX_RESTARTS})")
                            self._wait_for_restart()
                        else:
                            print("Process exited normally or maximum restarts reached.")
                            self._is_running = False
                            break
                
                if not self._is_process_alive() and self._is_running:
                    print("Starting new process...")
                    if not self._start_process():
                        print("Failed to start process. Retrying...")
                        self._wait_for_restart()
                        self._restart_count += 1
                
                time.sleep(self.WATCHDOG_INTERVAL)
        
        except KeyboardInterrupt:
            print("\nReceived keyboard interrupt. Stopping launcher...")
            self._is_running = False
        
        finally:
            print("Cleaning up...")
            self._stop_process()
            print("Launcher stopped.")


def main():
    launcher = PetLauncher()
    launcher.run()


if __name__ == "__main__":
    main()