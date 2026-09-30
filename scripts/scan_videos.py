import os
import subprocess
import glob

vids_dir = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files"
scratch_dir = r"C:\Users\User\.gemini\antigravity\scratch\video_candidates"
os.makedirs(scratch_dir, exist_ok=True)

# List videos between 2MB and 15MB (prime size for 10-30s garment videos)
all_vids = [
    f for f in os.listdir(vids_dir)
    if f.lower().endswith(('.mp4', '.mov')) and 2 * 1024 * 1024 <= os.path.getsize(os.path.join(vids_dir, f)) <= 15 * 1024 * 1024
]

print(f"Found {len(all_vids)} suitable videos in Telegram export.")

# Sample 20 videos and extract 1s frames
for i, vf in enumerate(all_vids[:25]):
    src = os.path.join(vids_dir, vf)
    out_frame = os.path.join(scratch_dir, f"sample_{i:02d}_{os.path.splitext(vf)[0]}.jpg")
    if not os.path.exists(out_frame):
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:02", "-i", src,
            "-vframes", "1", "-vf", "scale=-1:720", "-q:v", "3", out_frame
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

frames = glob.glob(os.path.join(scratch_dir, "*.jpg"))
print(f"Extracted {len(frames)} sample frames in {scratch_dir}")
for f in frames[:10]:
    print(" -", os.path.basename(f))
