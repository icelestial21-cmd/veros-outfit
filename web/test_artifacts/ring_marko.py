import subprocess
import time
import re
import xml.etree.ElementTree as ET

ADB = r"C:\Users\User\AppData\Local\Android\Sdk\platform-tools\adb.exe"
DEVICE = "192.168.50.185:5555"

def adb_cmd(args):
    cmd = [ADB, "-s", DEVICE] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

print("Phase 1: Tapping Voice call option at (560, 160)...")
adb_cmd(["shell", "input", "tap", "560", "160"])
time.sleep(1.0)

# Check if a confirmation dialog is present
adb_cmd(["shell", "uiautomator", "dump", "/sdcard/confirm_ui.xml"])
xml_data = adb_cmd(["shell", "cat", "/sdcard/confirm_ui.xml"])

call_btn = None
if xml_data:
    try:
        root = ET.fromstring(xml_data)
        for node in root.iter("node"):
            text = node.attrib.get("text", "")
            res_id = node.attrib.get("resource-id", "")
            if text.lower() == "call" or ("call" in text.lower() and len(text) < 12) or res_id.endswith("button1"):
                bounds = node.attrib.get("bounds", "")
                m = re.findall(r"\[(\d+),(\d+)\]", bounds)
                if len(m) == 2:
                    x = (int(m[0][0]) + int(m[1][0])) // 2
                    y = (int(m[0][1]) + int(m[1][1])) // 2
                    call_btn = (x, y, text)
                    break
    except Exception as e:
        print(f"XML parse note: {e}")

if call_btn:
    print(f"Confirmation dialog detected. Tapping '{call_btn[2]}' at ({call_btn[0]}, {call_btn[1]})...")
    adb_cmd(["shell", "input", "tap", str(call_btn[0]), str(call_btn[1])])
    time.sleep(1.5)
else:
    print("Direct dialing initiated without additional confirmation dialog.")

# At t=2.5s, capture in-progress screenshot
print("Phase 2: Verifying live call connection...")
time.sleep(1.5)
adb_cmd(["shell", "screencap", "-p", "/sdcard/call_in_progress.png"])
adb_cmd(["pull", "/sdcard/call_in_progress.png", r"c:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\test_artifacts\call_in_progress.png"])

# Let it ring through t=6.5s (sufficient to vibrate and alert Baku showroom handset)
print("Phase 3: Ringing showroom handset (4.0 additional seconds)...")
time.sleep(4.0)

# Phase 4: Disconnect
print("Phase 4: Executing call termination...")
adb_cmd(["shell", "input", "keyevent", "6"]) # KEYCODE_ENDCALL
# Red hangup button on Android VoIP UI (typically center bottom around 360, 1420 or 360, 1380)
adb_cmd(["shell", "input", "tap", "360", "1420"])
adb_cmd(["shell", "input", "tap", "360", "1380"])
adb_cmd(["shell", "input", "keyevent", "6"])
time.sleep(1.5)

# Verify whether call activity has finished or if still in call
focus = adb_cmd(["shell", "dumpsys", "window", "|", "grep", "-E", "'mCurrentFocus'"])
print(f"Current window focus after hangup: {focus}")

# Capture final chat history proof
print("Phase 5: Capturing post-call chat ledger proof...")
adb_cmd(["shell", "screencap", "-p", "/sdcard/call_ended_receipt.png"])
adb_cmd(["pull", "/sdcard/call_ended_receipt.png", r"c:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\test_artifacts\call_ended_receipt.png"])
print("Ring execution sequence completed.")
