# Console implementation added by decoder
import sys
import os
import time

class Console:
    @staticmethod
    def write(text):
        """Write text without newline"""
        sys.stdout.write(str(text))
        sys.stdout.flush()
    
    @staticmethod
    def write_line(text=""):
        """Write text with newline"""
        print(text)
    
    @staticmethod
    def read_line():
        """Read line from input"""
        return input()
    
    @staticmethod
    def read_key():
        """Read single key"""
        try:
            # Try Windows
            import msvcrt
            return msvcrt.getch().decode()
        except:
            try:
                # Try Unix
                import tty, termios
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    return sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except:
                # Fallback
                return input()[0] if input() else ''
    
    @staticmethod
    def clear():
        """Clear console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def set_title(title):
        """Set window title"""
        if os.name == 'nt':
            os.system(f'title {title}')
        else:
            sys.stdout.write(f'\033]0;{title}\007')
            sys.stdout.flush()
    
    @staticmethod
    def set_color(color):
        """Set text color (ANSI)"""
        if os.name != 'nt':
            sys.stdout.write(f'\033[{color}m')
    
    @staticmethod
    def reset_color():
        """Reset colors"""
        if os.name != 'nt':
            sys.stdout.write('\033[0m')
    
    @staticmethod
    def beep():
        """Play beep sound"""
        sys.stdout.write('\a')
        sys.stdout.flush()
    
    @staticmethod
    def sleep(seconds):
        """Sleep for seconds"""
        time.sleep(seconds)

# Create console instance
console = Console()

#!/usr/bin/env python3
import os
import sys
import time
import random
import requests

# ---------------------------------------
# Auto-install cfonts if missing
# ---------------------------------------
try:
    from cfonts import render
except ImportError:
    os.system('pip install python-cfonts >nul 2>&1' if os.name == 'nt' else 'pip install python-cfonts -q')
    from cfonts import render

# ---------------------------------------
# ANSI Colors
# ---------------------------------------
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ---------------------------------------
# API CONFIG
# ---------------------------------------
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?ts={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Referer": "https://hgnice.biz"
}

# ---------------------------------------
# Typewriter animation
# ---------------------------------------
def type_writer(text, delay=0.001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ---------------------------------------
# Banner Display
# ---------------------------------------
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    output = render(
        'SCRIPT',
        colors=['yellow', 'green'],
        align='center',
        font='block',
        space=True
    )
    for line in output.split("\n"):
        type_writer(line, delay=0.0007)

    type_writer("\033[93m-----------------------------------------------------------\033[0m", 0.0007)
    type_writer("\033[92m  BOSS SHIKAARI | ADVANCE PYTHON SCRIPT \033[0m", 0.001)
    type_writer("\033[93m-----------------------------------------------------------\033[0m\n", 0.0007)

# ---------------------------------------
# Prediction Logic (Stable System)
# ---------------------------------------
def stable_prediction(period_number, last_results, prev_prediction=None):
    if not last_results:
        return random.choice(["BIG", "SMALL"])

    recent = last_results[-10:]
    labeled = ["BIG" if int(r) >= 5 else "SMALL" for r in recent]

    big_count = labeled.count("BIG")
    small_count = labeled.count("SMALL")

    # History-based logic
    if big_count > small_count:
        history_pred = "BIG"
    elif small_count > big_count:
        history_pred = "SMALL"
    else:
        history_pred = "BIG" if int(period_number[-1]) >= 5 else "SMALL"

    # Period-based pattern
    last3_period = int(period_number[-3:]) if period_number.isdigit() else 0
    digit_sum = sum(int(d) for d in str(last3_period))
    period_pred = "BIG" if digit_sum % 2 == 0 else "SMALL"

    # Merge both systems
    if history_pred == period_pred:
        base_pred = history_pred
    else:
        base_pred = random.choice([history_pred, period_pred])

    # Prevent repeating same result twice
    if prev_prediction and base_pred == prev_prediction:
        base_pred = "BIG" if base_pred == "SMALL" else "SMALL"

    # Add small randomness for variation
    if random.random() < 0.2:
        base_pred = "BIG" if base_pred == "SMALL" else "SMALL"

    return base_pred

# ---------------------------------------
# Helper Functions
# ---------------------------------------
def get_big_small(number):
    try:
        return "BIG" if int(number) >= 5 else "SMALL"
    except ValueError:
        return "Unknown"

def fetch_latest():
    try:
        ts = int(time.time() * 1000)
        response = requests.get(API_URL.format(ts), headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get("data", {}).get("list", [])
    except requests.RequestException:
        return []

def print_prediction(period, prediction):
    print(f"{CYAN}  Period  {YELLOW}{period}{RESET}")
    print(f"{CYAN}  Prediction  {YELLOW}{prediction}{RESET}")
    sys.stdout.write(f"{CYAN}  Result  {RESET}")
    sys.stdout.flush()

def print_result(win):
    if win:
        sys.stdout.write(GREEN + BOLD + " VICTORY!\n\n" + RESET)
    else:
        sys.stdout.write(RED + BOLD + " LOSS!\n\n" + RESET)
    sys.stdout.flush()

# ---------------------------------------
# Main Prediction Runner
# ---------------------------------------
def run_console():
    seen_periods = set()
    prediction = None
    last_results = []
    prev_prediction = None

    banner()
    type_writer("\033[96mInitializing AI Prediction Engine...\033[0m", 0.008)
    time.sleep(1)
    type_writer("\033[92mSystem Ready \033[0m\n", 0.008)
    time.sleep(1)

    while True:
        data = fetch_latest()
        if not data:
            time.sleep(2)
            continue

        latest = data[0]
        current_period = latest.get("issueNumber", "")
        result_number = latest.get("number", "")

        try:
            last_results.append(int(result_number))
            if len(last_results) > 50:
                last_results.pop(0)
        except ValueError:
            pass

        # Check result against last prediction
        if prediction and prediction["period"] == current_period:
            win = prediction["prediction"] == get_big_small(result_number)
            print_result(win)
            prev_prediction = prediction["prediction"]
            prediction = None

        # Generate new prediction
        if not prediction and current_period not in seen_periods:
            seen_periods.add(current_period)
            next_period = str(int(current_period) + 1) if current_period.isdigit() else ""
            next_prediction = stable_prediction(current_period, last_results, prev_prediction)

            prediction = {"period": next_period, "prediction": next_prediction}
            show_period = next_period[-5:] if len(next_period) >= 5 else next_period
            print_prediction(show_period, next_prediction)

        time.sleep(3)

# ---------------------------------------
# Entry Point
# ---------------------------------------
if __name__ == "__main__":
    run_console()