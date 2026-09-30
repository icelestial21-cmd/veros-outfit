import os
import subprocess
from PIL import Image

video_path = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov'
output_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_micro_scan'
os.makedirs(output_dir, exist_ok=True)

# Extract frames between 0.0 and 3.0 seconds at 20 fps (every 0.05s)
cmd = [
    'ffmpeg', '-y',
    '-ss', '0.0',
    '-t', '3.0',
    '-i', video_path,
    '-vf', 'fps=20,scale=540:960',
    os.path.join(output_dir, 'frame_%03d.jpg')
]
print("Running ffmpeg extraction...")
subprocess.run(cmd, check=True)

# Also check copy_4B302E3F-DDE7-4D25-B339-2288593E397B.mov
video2 = r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_4B302E3F-DDE7-4D25-B339-2288593E397B.mov'
output2 = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_v2_scan'
os.makedirs(output2, exist_ok=True)
if os.path.exists(video2):
    cmd2 = [
        'ffmpeg', '-y',
        '-ss', '0.0',
        '-t', '5.0',
        '-i', video2,
        '-vf', 'fps=2,scale=540:960',
        os.path.join(output2, 'frame_%02d.jpg')
    ]
    subprocess.run(cmd2, check=True)

print("Frames extracted successfully.")
