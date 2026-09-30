import os
import subprocess
from PIL import Image

out_dir = r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\highres_candidates'
os.makedirs(out_dir, exist_ok=True)

# 1. silk video at 0.00s and 0.10s (where arms are down, hands clasped at belt)
cmd1 = [
    'ffmpeg', '-y',
    '-ss', '0.00',
    '-i', r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov',
    '-vframes', '1',
    os.path.join(out_dir, 'silk_t0_0s.jpg')
]
subprocess.run(cmd1, check=True)

cmd1b = [
    'ffmpeg', '-y',
    '-ss', '0.10',
    '-i', r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\copy_3FD097F2-149E-4E5E-B23E-B4FE97836874.mov',
    '-vframes', '1',
    os.path.join(out_dir, 'silk_t0_1s.jpg')
]
subprocess.run(cmd1b, check=True)

# 2. IMG_1649 on red carpet at 4.0s and 5.0s
cmd2 = [
    'ffmpeg', '-y',
    '-ss', '4.00',
    '-i', r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\IMG_1649.MOV',
    '-vframes', '1',
    os.path.join(out_dir, 'black_silk_4s.jpg')
]
subprocess.run(cmd2, check=True)

# 3. IMG_1681 in black burberry tee at 1.0s (hands at side)
cmd3 = [
    'ffmpeg', '-y',
    '-ss', '1.00',
    '-i', r'D:\Media\Telegram_Exports\ChatExport_2026-09-26\video_files\IMG_1681.MOV',
    '-vframes', '1',
    os.path.join(out_dir, 'burberry_hands_at_side_1s.jpg')
]
subprocess.run(cmd3, check=True)

print("Extracted highres candidates.")
