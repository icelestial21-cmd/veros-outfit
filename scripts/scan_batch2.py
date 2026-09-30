import os
import glob
import subprocess

vids_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files"
scratch_dir = r"C:\Users\User\.gemini\antigravity\scratch\video_candidates"

# Let's inspect another batch of videos from Telegram export
all_vids = [
    f for f in os.listdir(vids_dir)
    if f.lower().endswith(('.mp4', '.mov')) and 1.5 * 1024 * 1024 <= os.path.getsize(os.path.join(vids_dir, f)) <= 25 * 1024 * 1024
]

for i, vf in enumerate(all_vids[25:50], start=25):
    src = os.path.join(vids_dir, vf)
    out_frame = os.path.join(scratch_dir, f"sample_{i:02d}_{os.path.splitext(vf)[0]}.jpg")
    if not os.path.exists(out_frame):
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:03", "-i", src,
            "-vframes", "1", "-vf", "scale=-1:720", "-q:v", "3", out_frame
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

frames = sorted(glob.glob(os.path.join(scratch_dir, "sample_*.jpg")))
print(f"Total candidate frames: {len(frames)}")
for f in frames[25:40]:
    print(" -", os.path.basename(f))
