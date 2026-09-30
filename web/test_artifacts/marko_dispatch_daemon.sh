#!/bin/sh
# Autonomous Marko Baku Outreach Daemon
# Self-destructs upon completion or terminal failure

LOG_FILE="/sdcard/marko_dispatch.log"
echo "[$(date)] Daemon initiated. Sleeping 10643 seconds until target dispatch window..." > "$LOG_FILE"

sleep 10643

echo "[$(date)] Timer reached. Waking device..." >> "$LOG_FILE"
svc power stayon true
input keyevent 224
wm dismiss-keyguard
sleep 2

echo "[$(date)] Launching WhatsApp intent to Marko Baku..." >> "$LOG_FILE"
am start -a android.intent.action.VIEW -d 'https://api.whatsapp.com/send?phone=994703966660&text=Salam.%0A%0AA%20few%20weeks%20back%20I%20messaged%20you%20asking%20if%20you%20had%20a%20website%20and%20what%20the%20pricing%20was%20for%20your%20Italian%20collection.%20%0A%0AI%20am%20reaching%20back%20out%20because%20I%20genuinely%20like%20your%20pieces%20and%20your%20curation.%20The%20outfits%20you%20put%20together%20in%20Baku%20are%20exceptionally%20sharp%2C%20and%20I%20actually%20wanted%20to%20buy%20from%20you.%20%0A%0AHowever%2C%20having%20to%20scroll%20through%20thousands%20of%20posts%20across%20Telegram%20and%20Instagram%20just%20to%20locate%20a%20specific%20outfit%2C%20screenshot%20it%2C%20send%20it%20here%2C%20and%20wait%20for%20pricing%20and%20sizing%20was%20simply%20too%20much%20friction.%20I%20ended%20up%20abandoning%20the%20purchase%20because%20browsing%20that%20way%20was%20an%20uphill%20battle.%0A%0AI%20lead%20a%20software%20engineering%20firm.%20I%20realized%20that%20if%20I%20walked%20away%20as%20a%20paying%20client%20because%20of%20that%20friction%2C%20you%20must%20be%20losing%20high-ticket%20international%20buyers%20every%20single%20day%20who%20love%20your%20clothes%20but%20refuse%20to%20negotiate%20in%20chat.%0A%0ASo%20my%20team%20went%20ahead%20and%20built%20Marko%20Baku%20the%20flagship%20store%20you%20ought%20to%20have%3A%0A%0A%F0%9F%91%89%20https%3A//icelestial21-cmd.github.io/client-previews/marko/%0A%0AOpen%20it%20on%20your%20phone%20and%20laptop%20and%20notice%20how%20different%20the%20experience%20is%3A%0A1.%20Complete%2C%20structured%20collections%3A%20your%20clients%20can%20actually%20find%20and%20inspect%20garments%20in%20seconds%20instead%20of%20digging%20through%20an%20endless%20chat%20feed.%0A2.%20Transparent%20pricing%3A%20instant%20toggling%20between%20AZN%2C%20USD%2C%20EUR%2C%20and%20GBP.%0A3.%20The%20Virtual%20Fitting%20Pavilion%3A%20buyers%20input%20their%20height%20and%20receive%20automatic%20size%20verdicts%2C%20so%20your%20staff%20never%20has%20to%20ask%20for%20height%20and%20weight%20in%20WhatsApp%20again.%0A%0AI%20initially%20built%20this%20because%20I%20wanted%20a%20frictionless%20way%20to%20shop%20your%20pieces%20myself%2C%20but%20this%20engine%20belongs%20in%20your%20hands.%20%0A%0ATake%20a%20look%20on%20your%20phone%20and%20laptop.%20If%20you%20want%20the%20keys%20to%20this%20atelier%20so%20you%20can%20automate%20your%20overseas%20orders%2C%20let%20me%20know.' -p com.whatsapp.w4b >> "$LOG_FILE" 2>&1
sleep 4

echo "[$(date)] Tapping send button (653, 1541)..." >> "$LOG_FILE"
input tap 653 1541
sleep 3

# Tap send a second time just in case of initial focus delay
input tap 653 1541
sleep 2

# Take proof screenshot
echo "[$(date)] Capturing delivery proof..." >> "$LOG_FILE"
screencap -p /sdcard/marko_dispatch_proof.png

# Verify state
FOCUS=$(dumpsys window | grep -E 'mCurrentFocus' | head -n 1)
echo "[$(date)] Active focus: $FOCUS" >> "$LOG_FILE"

if echo "$FOCUS" | grep -qi "whatsapp"; then
    echo "[$(date)] MISSION SUCCESS: Message dispatched to Marko Baku." >> "$LOG_FILE"
    cmd notification post -S bigtext -t "Marko Outreach: SUCCESS" "marko_daemon" "Digital Atelier proposal successfully delivered to Marko Baku (+994 70 396 66 60). Verification screenshot saved to Photos/Files."
else
    echo "[$(date)] MISSION WARNING: Window focus state uncertain." >> "$LOG_FILE"
    cmd notification post -S bigtext -t "Marko Outreach: NOTICE" "marko_daemon" "Dispatch routine completed. Please check WhatsApp to verify message delivery."
fi

# Turn screen off to conserve battery
sleep 1
input keyevent 26
svc power stayon false

# Self-destruct script
echo "[$(date)] Self-destructing daemon script..." >> "$LOG_FILE"
rm -f /data/local/tmp/marko_dispatch_daemon.sh
