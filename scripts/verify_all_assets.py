import json
import os
import re

base = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web"

# 1. Check products.json
with open(os.path.join(base, "products.json"), "r", encoding="utf-8") as f:
    products = json.load(f)

missing = []
for p in products:
    for key in ["image", "video", "back_image", "detail_image"]:
        val = p.get(key)
        if val:
            full = os.path.join(base, val.replace("/", os.sep))
            if not os.path.exists(full):
                missing.append((p["id"], key, val))

print(f"Products in catalog: {len(products)}")
if missing:
    print("MISSING ASSETS IN PRODUCTS.JSON:")
    for m in missing:
        print(" ", m)
else:
    print("-> All product media (front, video, back, detail) exist on disk.")

# 2. Check HTML files
for hname in ["index.html", "collections.html", "lookbook.html", "product.html"]:
    hpath = os.path.join(base, hname)
    with open(hpath, "r", encoding="utf-8") as f:
        content = f.read()
    srcs = re.findall(r'src=["\'](assets/[^"\']+)["\']', content)
    html_missing = []
    for s in srcs:
        full = os.path.join(base, s.replace("/", os.sep))
        if not os.path.exists(full):
            html_missing.append(s)
    if html_missing:
        print(f"MISSING IN {hname}: {html_missing}")
    else:
        print(f"-> {hname}: All {len(srcs)} static asset references verified.")
