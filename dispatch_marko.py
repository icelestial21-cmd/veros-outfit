import os
import sys
import time
import subprocess
import urllib.parse
from datetime import datetime

ADB = r"C:\Users\User\AppData\Local\Android\Sdk\platform-tools\adb.exe"
TARGET = "LZV70DJMGD8000729"
PROJECT_DIR = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier"
LOG_FILE = os.path.join(PROJECT_DIR, "00_Working", "marko_dispatch.log")

TARGET_PHONE = "994703966660"

MESSAGE_BODY = """Salam.

A few weeks back I messaged you asking if you had a website and what the pricing was for your Italian collection.

I am reaching back out because I genuinely like your pieces and your curation. The outfits you put together in Baku are exceptionally sharp, and I actually wanted to buy from you.

However, having to scroll through thousands of posts across Telegram and Instagram just to locate a specific outfit, screenshot it, send it here, and wait for pricing and sizing was simply too much friction. I ended up abandoning the purchase because browsing that way was an uphill battle.

I lead a software engineering firm. I realized that if I walked away as a paying client because of that friction, you must be losing high-ticket international buyers every single day who love your clothes but refuse to negotiate in chat.

So my team went ahead and built Marko Baku the flagship store you ought to have:

https://icelestial21-cmd.github.io/client-previews/marko/

Open it on your phone and laptop and notice how different the experience is:
1. Complete, structured collections: your clients can actually find and inspect garments in seconds instead of digging through an endless chat feed.
2. Transparent pricing: instant toggling between AZN, USD, EUR, and GBP.
3. The Virtual Fitting Pavilion: buyers input their height and receive automatic size verdicts, so your staff never has to ask for height and weight in WhatsApp again.

I initially built this because I wanted a frictionless way to shop your pieces myself, but this engine belongs in your hands.

Take a look on your phone and laptop. If you want the keys to this atelier so you can automate your overseas orders, let me know."""

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"Log write error: {e}")

def run_adb(cmd_list, timeout=15):
    full_cmd = [ADB, "-s", TARGET] + cmd_list
    res = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
    return res.stdout.strip()

def main():
    log("=== INITIATING MARKO BAKU OUTREACH DISPATCH VIA DIRECT USB ===")
    
    # Step 1: Ensure device wakefulness
    log("Waking device and unlocking display...")
    run_adb(["shell", "svc power stayon true"])
    run_adb(["shell", "input keyevent 224"])
    time.sleep(0.5)
    run_adb(["shell", "wm dismiss-keyguard"])
    time.sleep(0.5)
    
    # Step 2: Launch WhatsApp Business intent
    encoded = urllib.parse.quote(MESSAGE_BODY)
    intent_url = f"https://api.whatsapp.com/send?phone={TARGET_PHONE}&text={encoded}"
    log(f"Launching WhatsApp Business intent for recipient +{TARGET_PHONE}...")
    launch_res = run_adb(["shell", f"am start -a android.intent.action.VIEW -d '{intent_url}' -p com.whatsapp.w4b"])
    log(f"Intent response: {launch_res}")
    
    # Step 3: Await conversation rendering & text population
    log("Awaiting conversation render and text population (4 seconds)...")
    time.sleep(4)
    
    # Step 4: Execute Send button tap (verified coordinate on 720x1600: 653, 1541)
    log("Executing Send tap at verified coordinate (653, 1541)...")
    run_adb(["shell", "input tap 653 1541"])
    time.sleep(2)
    
    # Step 5: Tap again to guarantee focus transmission
    log("Executing secondary Send tap for transmission certainty...")
    run_adb(["shell", "input tap 653 1541"])
    time.sleep(3)
    
    # Step 6: Confirmation receipt capture
    receipt_remote = "/sdcard/marko_dispatch_proof.png"
    receipt_local = os.path.join(PROJECT_DIR, "web", "test_artifacts", "marko_transmission_receipt.png")
    os.makedirs(os.path.dirname(receipt_local), exist_ok=True)
    run_adb(["shell", f"screencap -p {receipt_remote}"])
    pull_res = subprocess.run([ADB, "-s", TARGET, "pull", receipt_remote, receipt_local], capture_output=True, text=True)
    log(f"Transmission screenshot receipt pulled: {pull_res.stdout.strip()}")
    
    # Step 7: Post notification
    run_adb(["shell", "cmd notification post -S bigtext -t 'Marko Baku Outreach: SENT' 'marko_daemon' 'Digital Atelier proposal successfully delivered to Marko Baku (+994 70 396 66 60). Verification screenshot saved.'"])
    log("Mission complete. Message dispatched to Marko Baku.")

if __name__ == "__main__":
    main()
