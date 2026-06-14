import subprocess
import time

import pyperclip


class TextInjector:
    def inject(self, text):
        pyperclip.copy(text)
        time.sleep(0.08)
        script = '''
            tell application "System Events"
                keystroke "v" using command down
            end tell
        '''
        subprocess.run(["osascript", "-e", script], capture_output=True)
