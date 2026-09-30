from PIL import Image, ImageDraw

def render_canvas_sim(name, img_file, lm, data):
    p = rf"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets\{img_file}"
    out = rf"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\canvas_{name}.jpg"
    img = Image.open(p).convert("RGBA")
    w, h = 450, 800
    resized = img.resize((w, h), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", (w, h), (7, 9, 14, int(255 * 0.35)))
    composed = Image.alpha_composite(resized, overlay)
    draw = ImageDraw.Draw(composed)

    headX = w * lm["head"][0]
    headY = h * lm["head"][1]
    shLX = w * lm["shoulderL"][0]
    shRX = w * lm["shoulderR"][0]
    shY = h * lm["shoulderL"][1]
    chestX = w * lm["chest"][0]
    chestY = h * lm["chest"][1]
    waistLX = w * lm["waistL"][0]
    waistRX = w * lm["waistR"][0]
    waistY = h * lm["waistL"][1]
    pelvisX = w * lm["pelvis"][0]
    pelvisY = h * lm["pelvis"][1]
    kneeLX = w * lm["kneeL"][0]
    kneeLY = h * lm["kneeL"][1]
    kneeRX = w * lm["kneeR"][0]
    kneeRY = h * lm["kneeR"][1]
    ankLX = w * lm["ankleL"][0]
    ankLY = h * lm["ankleL"][1]
    ankRX = w * lm["ankleR"][0]
    ankRY = h * lm["ankleR"][1]

    gold = (212, 175, 55, 230)
    green = (74, 222, 128, 255)

    conn = [
        ((headX, headY), (chestX, chestY)),
        ((chestX, chestY), (pelvisX, pelvisY)),
        ((shLX, shY), (shRX, shY)),
        ((shLX, shY), (chestX, chestY)),
        ((shRX, shY), (chestX, chestY)),
        ((waistLX, waistY), (waistRX, waistY)),
        ((pelvisX, pelvisY), (kneeLX, kneeLY)),
        ((pelvisX, pelvisY), (kneeRX, kneeRY)),
        ((kneeLX, kneeLY), (ankLX, ankLY)),
        ((kneeRX, kneeRY), (ankRX, ankRY))
    ]
    for p1, p2 in conn:
        draw.line([p1, p2], fill=gold, width=2)

    nodes = [
        (headX, headY), (shLX, shY), (shRX, shY), (chestX, chestY),
        (waistLX, waistY), (waistRX, waistY), (pelvisX, pelvisY),
        (kneeLX, kneeLY), (kneeRX, kneeRY), (ankLX, ankLY), (ankRX, ankRY)
    ]
    for nx, ny in nodes:
        draw.ellipse([nx-6, ny-6, nx+6, ny+6], outline=green, fill=(74, 222, 128, 90), width=2)
        draw.ellipse([nx-2.5, ny-2.5, nx+2.5, ny+2.5], fill=green)

    # Badges
    badge_x = int(w * 0.06) if lm.get("badgeSide") == "left" else int(w * 0.56)
    badges = [
        (shY - 6, f"SHOULDER: {data['shoulder']} CM"),
        (chestY, f"CHEST: {data['chest']} CM"),
        (waistY, f"WAIST: {data['waist']} CM"),
        (kneeLY - 40, f"OUTSEAM: {data['outseam']} CM")
    ]
    for by, txt in badges:
        bw, bh = 145, 22
        draw.rounded_rectangle([badge_x, by-11, badge_x+bw, by+11], radius=4, fill=(7, 9, 14, 230), outline=(212, 175, 55, 255), width=1)
        draw.text((badge_x + 8, by - 6), txt, fill=(243, 229, 171, 255))

    composed.convert("RGB").save(out, quality=95)
    print(f"Rendered canvas sim: {out}")

lm_master = {
    "head": (0.615, 0.22),
    "shoulderL": (0.49, 0.315),
    "shoulderR": (0.74, 0.315),
    "chest": (0.615, 0.40),
    "waistL": (0.52, 0.575),
    "waistR": (0.71, 0.575),
    "pelvis": (0.62, 0.63),
    "kneeL": (0.55, 0.76),
    "kneeR": (0.70, 0.76),
    "ankleL": (0.54, 0.91),
    "ankleR": (0.75, 0.91),
    "badgeSide": "left"
}
data_master = {"shoulder": 49.0, "chest": 54.0, "waist": 42.0, "outseam": 103.0}
render_canvas_sim("master", "model_baku_master.jpg", lm_master, data_master)
