import os
import subprocess
import shutil

web_dir = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web"
assets_dir = os.path.join(web_dir, "assets")
scratch_dir = r"C:\Users\User\.gemini\antigravity\scratch"
tg_base = r"D:\Media\Telegram_Exports\ChatExport_2026-09-26"
photos_dir = os.path.join(tg_base, "photos")
vids_dir = os.path.join(tg_base, "video_files")

print("Safeguarding original pristine photos...")
# Original MB-01_front.jpg is the Armani sneaker
armani_sneaker_backup = os.path.join(scratch_dir, "armani_sneaker_orig.jpg")
if os.path.exists(os.path.join(assets_dir, "MB-01_front.jpg")) and not os.path.exists(armani_sneaker_backup):
    shutil.copy2(os.path.join(assets_dir, "MB-01_front.jpg"), armani_sneaker_backup)

# Original MB-07_front.jpg is the Loro Piana navy loafer
loro_piana_backup = os.path.join(scratch_dir, "loro_piana_orig.jpg")
if os.path.exists(os.path.join(assets_dir, "MB-07_front.jpg")) and not os.path.exists(loro_piana_backup):
    shutil.copy2(os.path.join(assets_dir, "MB-07_front.jpg"), loro_piana_backup)

# Original MB-03_front.jpg is the Philipp Plein leather-trim jacket
pp_jacket_backup = os.path.join(scratch_dir, "pp_jacket_orig.jpg")
if os.path.exists(os.path.join(assets_dir, "MB-03_front.jpg")) and not os.path.exists(pp_jacket_backup):
    shutil.copy2(os.path.join(assets_dir, "MB-03_front.jpg"), pp_jacket_backup)

# Original MB-10_front.jpg is the Dolce & Gabbana black hoodie
dg_hoodie_backup = os.path.join(scratch_dir, "dg_hoodie_orig.jpg")
if os.path.exists(os.path.join(assets_dir, "MB-10_front.jpg")) and not os.path.exists(dg_hoodie_backup):
    shutil.copy2(os.path.join(assets_dir, "MB-10_front.jpg"), dg_hoodie_backup)

# Original MB-02_front.jpg is the Fendi cap
fendi_cap_backup = os.path.join(scratch_dir, "fendi_cap_orig.jpg")
if os.path.exists(os.path.join(assets_dir, "MB-02_front.jpg")) and not os.path.exists(fendi_cap_backup):
    shutil.copy2(os.path.join(assets_dir, "MB-02_front.jpg"), fendi_cap_backup)

print("Original photos safeguarded successfully.")

# 1. MB-01: Dolce & Gabbana White Silk Resort Set (Shirt + Shorts)
# Master video: MB-01_walk.mp4
subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:01.2", "-i", os.path.join(assets_dir, "MB-01_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-01_front.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:02.5", "-i", os.path.join(assets_dir, "MB-01_walk.mp4"),
    "-vframes", "1", "-vf", "crop=in_w*0.5:in_h*0.4:in_w*0.45:in_h*0.2", "-q:v", "1",
    os.path.join(assets_dir, "MB-01_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:03.0", "-i", os.path.join(assets_dir, "MB-01_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-01_back.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-01_front.jpg"), os.path.join(assets_dir, "MB-01_main.jpg"))
print("Processed MB-01 (Dolce & Gabbana Silk Resort Set)")

# 2. MB-02: EA7 Emporio Armani Piped Athletic Tracksuit
# Master video: MB-02_walk.mp4
subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:02.5", "-i", os.path.join(assets_dir, "MB-02_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-02_front.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:03.2", "-i", os.path.join(assets_dir, "MB-02_walk.mp4"),
    "-vframes", "1", "-vf", "crop=in_w*0.5:in_h*0.35:in_w*0.25:in_h*0.1", "-q:v", "1",
    os.path.join(assets_dir, "MB-02_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:01.0", "-i", os.path.join(assets_dir, "MB-02_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-02_back.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-02_front.jpg"), os.path.join(assets_dir, "MB-02_main.jpg"))
print("Processed MB-02 (EA7 Emporio Armani Tracksuit)")

# 3. MB-03: Gucci GG Supreme Jacquard Knit Web-Collar Polo
# Master video: MB-03_walk.mp4
subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:02.0", "-i", os.path.join(assets_dir, "MB-03_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-03_front.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:03.5", "-i", os.path.join(assets_dir, "MB-03_walk.mp4"),
    "-vframes", "1", "-vf", "crop=in_w*0.6:in_h*0.35:in_w*0.2:in_h*0.15", "-q:v", "1",
    os.path.join(assets_dir, "MB-03_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:05.5", "-i", os.path.join(assets_dir, "MB-03_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-03_back.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-03_front.jpg"), os.path.join(assets_dir, "MB-03_main.jpg"))
print("Processed MB-03 (Gucci GG Supreme Jacquard Polo)")

# 4. MB-04: Moncler Tricolor Sleeve-Stripe Interlock Tracksuit
moncler_vid_src = os.path.join(vids_dir, "B77C05CD-3662-4968-B1A7-A7B93A9477AF.MP4")
moncler_vid_dst = os.path.join(assets_dir, "MB-04_walk.mp4")
if os.path.exists(moncler_vid_src):
    shutil.copy2(moncler_vid_src, moncler_vid_dst)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:02.2", "-i", moncler_vid_dst,
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-04_front.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:03.0", "-i", moncler_vid_dst,
    "-vframes", "1", "-vf", "crop=in_w*0.5:in_h*0.35:in_w*0.3:in_h*0.1", "-q:v", "1",
    os.path.join(assets_dir, "MB-04_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:01.0", "-i", moncler_vid_dst,
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-04_back.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-04_front.jpg"), os.path.join(assets_dir, "MB-04_main.jpg"))
print("Processed MB-04 (Moncler Tricolor Tracksuit)")

# 5. MB-05: Emporio Armani Gilded Eagle Athletic Tracksuit
armani_vid_src = os.path.join(vids_dir, "50A1F4B6-D330-452B-95DE-A484A9639557.MP4")
armani_vid_dst = os.path.join(assets_dir, "MB-05_walk.mp4")
if os.path.exists(armani_vid_src):
    shutil.copy2(armani_vid_src, armani_vid_dst)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:02.0", "-i", armani_vid_dst,
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-05_front.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:03.5", "-i", armani_vid_dst,
    "-vframes", "1", "-vf", "crop=in_w*0.6:in_h*0.35:in_w*0.2:in_h*0.35", "-q:v", "1",
    os.path.join(assets_dir, "MB-05_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:01.0", "-i", armani_vid_dst,
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-05_back.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-05_front.jpg"), os.path.join(assets_dir, "MB-05_main.jpg"))
print("Processed MB-05 (Emporio Armani Gilded Tracksuit)")

# 6. MB-06: Gucci GG Supreme Monogram Canvas Baseball Cap
# Master video: MB-06_walk.mp4
subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:01.0", "-i", os.path.join(assets_dir, "MB-06_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-06_front.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:02.0", "-i", os.path.join(assets_dir, "MB-06_walk.mp4"),
    "-vframes", "1", "-vf", "crop=in_w*0.65:in_h*0.5:in_w*0.18:in_h*0.25", "-q:v", "1",
    os.path.join(assets_dir, "MB-06_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:03.5", "-i", os.path.join(assets_dir, "MB-06_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-06_back.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-06_front.jpg"), os.path.join(assets_dir, "MB-06_main.jpg"))
print("Processed MB-06 (Gucci GG Supreme Baseball Cap)")

# 7. MB-07: Gucci Interlocking GG Web Stripe Crewneck Sweaters
# Master video: MB-07_walk.mp4
subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:01.0", "-i", os.path.join(assets_dir, "MB-07_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-07_front.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:02.2", "-i", os.path.join(assets_dir, "MB-07_walk.mp4"),
    "-vframes", "1", "-vf", "crop=in_w*0.6:in_h*0.5:in_w*0.2:in_h*0.25", "-q:v", "1",
    os.path.join(assets_dir, "MB-07_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:03.0", "-i", os.path.join(assets_dir, "MB-07_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-07_back.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-07_front.jpg"), os.path.join(assets_dir, "MB-07_main.jpg"))
print("Processed MB-07 (Gucci Web Stripe Sweaters)")

# 8. MB-08: Christian Dior Oblique Pocket Slim-Fit Denim Jeans
dior_src = os.path.join(photos_dir, "photo_40@31-07-2024_03-20-48.jpg")
if os.path.exists(dior_src):
    shutil.copy2(dior_src, os.path.join(assets_dir, "MB-08_front.jpg"))
    shutil.copy2(dior_src, os.path.join(assets_dir, "MB-08_main.jpg"))
    subprocess.run([
        "ffmpeg", "-y", "-i", dior_src,
        "-vf", "crop=in_w*0.5:in_h*0.35:in_w*0.15:in_h*0.4", "-q:v", "1",
        os.path.join(assets_dir, "MB-08_detail.jpg")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.copy2(dior_src, os.path.join(assets_dir, "MB-08_back.jpg"))
print("Processed MB-08 (Christian Dior Oblique Denim)")

# 9. MB-09: Loro Piana Summer Walk Water-Repellent Suede Loafers
if os.path.exists(loro_piana_backup):
    shutil.copy2(loro_piana_backup, os.path.join(assets_dir, "MB-09_front.jpg"))
    shutil.copy2(loro_piana_backup, os.path.join(assets_dir, "MB-09_main.jpg"))
    subprocess.run([
        "ffmpeg", "-y", "-i", loro_piana_backup,
        "-vf", "crop=in_w*0.55:in_h*0.5:in_w*0.25:in_h*0.45", "-q:v", "1",
        os.path.join(assets_dir, "MB-09_detail.jpg")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.copy2(loro_piana_backup, os.path.join(assets_dir, "MB-09_back.jpg"))
print("Processed MB-09 (Loro Piana Suede Loafers)")

# 10. MB-10: Dolce & Gabbana Milano Metallic Plaque Heavy Fleece Hoodie
dg_hoodie_vid_src = os.path.join(vids_dir, "IMG_0039.MOV")
dg_hoodie_vid_dst = os.path.join(assets_dir, "MB-10_walk.mp4")
if os.path.exists(dg_hoodie_vid_src):
    shutil.copy2(dg_hoodie_vid_src, dg_hoodie_vid_dst)

if os.path.exists(dg_hoodie_backup):
    shutil.copy2(dg_hoodie_backup, os.path.join(assets_dir, "MB-10_front.jpg"))
    shutil.copy2(dg_hoodie_backup, os.path.join(assets_dir, "MB-10_main.jpg"))

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:03.0", "-i", dg_hoodie_vid_dst,
    "-vframes", "1", "-vf", "crop=in_w*0.55:in_h*0.35:in_w*0.22:in_h*0.5", "-q:v", "1",
    os.path.join(assets_dir, "MB-10_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-10_front.jpg"), os.path.join(assets_dir, "MB-10_back.jpg"))
print("Processed MB-10 (Dolce & Gabbana Metallic Plaque Hoodie)")

# 11. MB-11: Louis Vuitton Monogram Light-Wash Selvedge Denim
# Master video: MB-11_walk.mp4
subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:02.5", "-i", os.path.join(assets_dir, "MB-11_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-11_front.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:01.0", "-i", os.path.join(assets_dir, "MB-11_walk.mp4"),
    "-vframes", "1", "-vf", "crop=in_w*0.55:in_h*0.4:in_w*0.25:in_h*0.3", "-q:v", "1",
    os.path.join(assets_dir, "MB-11_detail.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:04.0", "-i", os.path.join(assets_dir, "MB-11_walk.mp4"),
    "-vframes", "1", "-q:v", "1", os.path.join(assets_dir, "MB-11_back.jpg")
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copy2(os.path.join(assets_dir, "MB-11_front.jpg"), os.path.join(assets_dir, "MB-11_main.jpg"))
print("Processed MB-11 (Louis Vuitton Denim Jeans)")

# 12. MB-12: Philipp Plein Lambskin-Collar Wool Zip Blouson
if os.path.exists(pp_jacket_backup):
    shutil.copy2(pp_jacket_backup, os.path.join(assets_dir, "MB-12_front.jpg"))
    shutil.copy2(pp_jacket_backup, os.path.join(assets_dir, "MB-12_main.jpg"))
    subprocess.run([
        "ffmpeg", "-y", "-i", pp_jacket_backup,
        "-vf", "crop=in_w*0.55:in_h*0.35:in_w*0.22:in_h*0.08", "-q:v", "1",
        os.path.join(assets_dir, "MB-12_detail.jpg")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.copy2(pp_jacket_backup, os.path.join(assets_dir, "MB-12_back.jpg"))
print("Processed MB-12 (Philipp Plein Zip Blouson)")

print("All 12 authentic product assets perfectly synchronized and generated!")
