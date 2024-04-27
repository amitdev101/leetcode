import psutil
import subprocess
import time
import threading
import re
import datetime
from shellit import execute_cmd

# Event to signal the detection of a wake event
wake_event = threading.Event()

def monitor_wake_events_shellit():
    last_wake_time = None
    while True:
        cmd = "log show --predicate 'eventMessage contains \"Wake\"' --last 1m"
        returncode, output = execute_cmd(cmd, shell=True)
        if returncode == 0 and output:
            line = output
            match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
            if match:
                wake_time = datetime.datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
                if last_wake_time != wake_time:
                    print(f"WakeEvent detected: {wake_time}")
                    last_wake_time = wake_time
                    wake_event.set()
                    
            

def find_and_kill_process(process_name):
    """
    Finds and kills processes with the specified name.

    :param process_name: The name of the process to search for and kill.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"{proc.info['name']}")
        if proc.info['name'].lower() == process_name:
            try:
                psutil.Process(proc.info['pid']).kill()
                print(f"Killed process {proc.info['name']} with PID {proc.info['pid']}")
            except psutil.NoSuchProcess:
                pass

def open_app(app_name):
    """
    Opens the specified application.

    :param app_name: The name of the application to open.
    """
    try:
        subprocess.run(["open", "-a", app_name])
        print(f"{app_name} has been opened. {time.ctime()}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to open {app_name}: {e}")

def main():
    # Example usage
    process_name = "ubar"  # Replace with the process name
    app_name = "ubar"  # Replace with the app name to restart

    find_and_kill_process(process_name)
    # time.sleep(1)  # Wait for 2 seconds to ensure the process is terminated
    open_app(app_name)


if __name__=='__main__':
    # Start the wake event monitoring in a separate thread
    threading.Thread(target=monitor_wake_events_shellit, daemon=True).start()

    try:
        while True:
            
            main()
            # Wait for a wake event or timeout after 280 seconds
            wake_event.wait(timeout=280)
            wake_event.clear()  # Reset the event after handling
    except KeyboardInterrupt:
        print("Program terminated by user.")
        