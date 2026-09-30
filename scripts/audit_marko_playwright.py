import asyncio
import json
import os
import sys

os.environ["NODE_OPTIONS"] = "--max-old-space-size=2048"
from playwright.async_api import async_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_URL = "http://localhost:8090"
OUTPUT_DIR = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\test_artifacts"
PRODUCTS_JSON_PATH = r"C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\products.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(PRODUCTS_JSON_PATH, "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

EXPECTED_NAV = ["Home", "Full Catalog", "Runway Lookbook", "Virtual Pavilion", "Global Proof", "The Atelier Difference"]
EXPECTED_CATEGORIES = {
    "all": 12,
    "knits": 3,
    "tailoring": 5,
    "denim": 2,
    "footwear": 1,
    "accessories": 1
}

async def run_audit():
    print("==================================================")
    print("STARTING ADVANCED PLAYWRIGHT AUDIT: MARKO BAKU FLAGSHIP")
    print(f"Target: {BASE_URL}")
    print("==================================================")

    audit_results = {
        "nav_consistency": {},
        "footer_consistency": {},
        "category_tabs": {},
        "category_urls": {},
        "density_toggle": {},
        "currency_switching": {},
        "cart_and_checkout": {},
        "lookbook_integrity": {},
        "product_measurements": {},
        "pavilion_integrity": {},
        "screenshots": [],
        "overall_pass": True
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"]
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # Capture browser console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        # ----------------------------------------------------
        # 1. AUDIT INDEX.HTML
        # ----------------------------------------------------
        print("\n--- 1. Auditing index.html ---")
        await page.goto(f"{BASE_URL}/index.html", wait_until="domcontentloaded")
        await page.wait_for_selector(".site-header")

        nav_links = await page.locator(".site-header .nav-links a").all_text_contents()
        nav_match = [n.strip() for n in nav_links] == EXPECTED_NAV
        audit_results["nav_consistency"]["index.html"] = {
            "found": [n.strip() for n in nav_links],
            "pass": nav_match
        }
        print(f"  Nav match: {nav_match}")

        footer_cols = await page.locator(".site-footer .footer-col").count()
        footer_bottom = await page.locator(".site-footer .footer-bottom").inner_text()
        footer_links_count = await page.locator(".site-footer .footer-links a").count()
        audit_results["footer_consistency"]["index.html"] = {
            "columns": footer_cols,
            "links_count": footer_links_count,
            "has_copyright": "Marko Baku Atelier Worldwide" in footer_bottom,
            "pass": footer_cols == 4 and "Marko Baku Atelier Worldwide" in footer_bottom
        }
        print(f"  Footer columns: {footer_cols}, Links count: {footer_links_count}")

        await page.screenshot(path=os.path.join(OUTPUT_DIR, "audit_index.png"), full_page=False)
        audit_results["screenshots"].append("audit_index.png")

        # ----------------------------------------------------
        # 2. AUDIT COLLECTIONS.HTML (CATEGORIES, URLS, DENSITY, CURRENCY)
        # ----------------------------------------------------
        print("\n--- 2. Auditing collections.html ---")
        await page.goto(f"{BASE_URL}/collections.html", wait_until="domcontentloaded")
        await page.wait_for_selector("#productsGrid .product-card")

        nav_links = await page.locator(".site-header .nav-links a").all_text_contents()
        nav_match = [n.strip() for n in nav_links] == EXPECTED_NAV
        audit_results["nav_consistency"]["collections.html"] = {
            "found": [n.strip() for n in nav_links],
            "pass": nav_match
        }

        # Check category buttons and click-through
        cat_buttons = await page.locator(".atelier-cat-link").all()
        print(f"  Found {len(cat_buttons)} Atelier category buttons")
        for btn in cat_buttons:
            text = (await btn.inner_text()).strip()
            onclick = await btn.get_attribute("onclick")
            # Extract category id from onclick
            cat_id = onclick.split("'")[1] if "'" in onclick else "all"
            await btn.click()
            await page.wait_for_timeout(200)

            rendered_cards = await page.locator("#productsGrid .product-card").count()
            expected_count = EXPECTED_CATEGORIES.get(cat_id, -1)
            cat_pass = rendered_cards == expected_count
            audit_results["category_tabs"][cat_id] = {
                "button_text": text,
                "rendered_cards": rendered_cards,
                "expected": expected_count,
                "pass": cat_pass
            }
            print(f"    Tab [{cat_id}]: {text} -> Rendered {rendered_cards} cards (Expected: {expected_count}) [Pass: {cat_pass}]")
            if not cat_pass:
                audit_results["overall_pass"] = False

        # Test Direct URL Query Filtering
        print("\n  Testing URL Query Parameter Filtering:")
        for cat_id, expected_count in EXPECTED_CATEGORIES.items():
            if cat_id == "all":
                continue
            test_url = f"{BASE_URL}/collections.html?cat={cat_id}"
            await page.goto(test_url, wait_until="domcontentloaded")
            await page.wait_for_selector("#productsGrid .product-card")
            active_btn_text = await page.locator(".atelier-cat-link.active").inner_text()
            rendered_cards = await page.locator("#productsGrid .product-card").count()
            url_pass = (rendered_cards == expected_count)
            audit_results["category_urls"][cat_id] = {
                "url": test_url,
                "active_tab": active_btn_text.replace("\n", " "),
                "rendered_cards": rendered_cards,
                "expected": expected_count,
                "pass": url_pass
            }
            print(f"    URL ?cat={cat_id}: Active Tab '{active_btn_text.strip()}' -> Cards {rendered_cards} (Expected: {expected_count}) [Pass: {url_pass}]")
            if not url_pass:
                audit_results["overall_pass"] = False

        # Reset to full collections
        await page.goto(f"{BASE_URL}/collections.html", wait_until="domcontentloaded")
        await page.wait_for_selector("#productsGrid .product-card")

        # Test Density Switcher
        print("\n  Testing Density Switcher:")
        editorial_btn = page.locator("#densityEditorialBtn")
        compact_btn = page.locator("#densityCompactBtn")
        await editorial_btn.click()
        await page.wait_for_timeout(150)
        has_editorial_class = await page.locator("#productsGrid").evaluate("el => el.classList.contains('editorial-view')")
        await compact_btn.click()
        await page.wait_for_timeout(150)
        has_compact_class = not (await page.locator("#productsGrid").evaluate("el => el.classList.contains('editorial-view')"))
        density_pass = has_editorial_class and has_compact_class
        audit_results["density_toggle"] = {
            "editorial_switch": has_editorial_class,
            "compact_switch": has_compact_class,
            "pass": density_pass
        }
        print(f"    Density Switch: Editorial={has_editorial_class}, Compact={has_compact_class} [Pass: {density_pass}]")

        # Test Multi-Currency Conversion
        print("\n  Testing Multi-Currency Conversion:")
        currency_select = page.locator("#currencySelector")
        prices_usd = await page.locator(".product-card .product-price").all_text_contents()
        first_usd_str = prices_usd[0] if prices_usd else "$0"

        await currency_select.select_option("EUR")
        await page.wait_for_timeout(150)
        prices_eur = await page.locator(".product-card .product-price").all_text_contents()
        first_eur_str = prices_eur[0] if prices_eur else ""

        await currency_select.select_option("GBP")
        await page.wait_for_timeout(150)
        prices_gbp = await page.locator(".product-card .product-price").all_text_contents()
        first_gbp_str = prices_gbp[0] if prices_gbp else ""

        await currency_select.select_option("AZN")
        await page.wait_for_timeout(150)
        prices_azn = await page.locator(".product-card .product-price").all_text_contents()
        first_azn_str = prices_azn[0] if prices_azn else ""

        # Return to USD
        await currency_select.select_option("USD")
        await page.wait_for_timeout(150)

        currency_pass = ("€" in first_eur_str and "£" in first_gbp_str and "₼" in first_azn_str and "$" in first_usd_str)
        audit_results["currency_switching"] = {
            "sample_USD": first_usd_str,
            "sample_EUR": first_eur_str,
            "sample_GBP": first_gbp_str,
            "sample_AZN": first_azn_str,
            "pass": currency_pass
        }
        print(f"    Currency Switch: USD={first_usd_str} -> EUR={first_eur_str} -> GBP={first_gbp_str} -> AZN={first_azn_str} [Pass: {currency_pass}]")

        # Test Cart Drawer and Checkout Flow
        print("\n  Testing Cart Drawer & Checkout:")
        first_quick_add = page.locator(".btn-quick-view").first
        await first_quick_add.scroll_into_view_if_needed()
        await first_quick_add.click()
        await page.wait_for_timeout(300)

        drawer_open = await page.locator("#cartDrawer").evaluate("el => el.classList.contains('open')")
        cart_items_count = await page.locator(".cart-item").count()
        cart_subtotal = await page.locator("#cartSubtotal").inner_text()

        # Click proceed to checkout
        checkout_btn = page.locator(".btn-checkout")
        await checkout_btn.click()
        await page.wait_for_timeout(300)

        modal_open = await page.locator("#checkoutModal").evaluate("el => el.classList.contains('open')")
        tracking_code = await page.locator("#checkoutTrackingCode").inner_text()
        close_modal_btn = page.locator("#checkoutModal .btn-primary")
        await close_modal_btn.click()
        await page.wait_for_timeout(200)

        cart_pass = drawer_open and cart_items_count > 0 and modal_open and "AZ-CARGO-" in tracking_code
        audit_results["cart_and_checkout"] = {
            "drawer_opened": drawer_open,
            "items_rendered": cart_items_count,
            "subtotal": cart_subtotal,
            "checkout_modal_opened": modal_open,
            "tracking_generated": tracking_code,
            "pass": cart_pass
        }
        print(f"    Cart Drawer Opened: {drawer_open}, Items: {cart_items_count}, Tracking: {tracking_code} [Pass: {cart_pass}]")

        await page.screenshot(path=os.path.join(OUTPUT_DIR, "audit_collections.png"), full_page=False)
        audit_results["screenshots"].append("audit_collections.png")

        # ----------------------------------------------------
        # 3. AUDIT LOOKBOOK.HTML
        # ----------------------------------------------------
        print("\n--- 3. Auditing lookbook.html ---")
        await page.goto(f"{BASE_URL}/lookbook.html", wait_until="domcontentloaded")
        await page.wait_for_selector(".lookbook-item")

        nav_links = await page.locator(".site-header .nav-links a").all_text_contents()
        nav_match = [n.strip() for n in nav_links] == EXPECTED_NAV
        audit_results["nav_consistency"]["lookbook.html"] = {
            "found": [n.strip() for n in nav_links],
            "pass": nav_match
        }

        lookbook_items = await page.locator(".lookbook-item").count()
        video_tags = await page.locator(".lookbook-video").count()
        inspect_links = await page.locator(".lookbook-item a[href*='product.html?id=']").count()

        lookbook_pass = (lookbook_items == 9 and video_tags == 9 and inspect_links == 9)
        audit_results["lookbook_integrity"] = {
            "item_count": lookbook_items,
            "video_count": video_tags,
            "inspect_links": inspect_links,
            "pass": lookbook_pass
        }
        print(f"  Lookbook items: {lookbook_items}, Videos: {video_tags}, Inspect links: {inspect_links} [Pass: {lookbook_pass}]")

        await page.screenshot(path=os.path.join(OUTPUT_DIR, "audit_lookbook.png"), full_page=False)
        audit_results["screenshots"].append("audit_lookbook.png")

        # ----------------------------------------------------
        # 4. AUDIT PRODUCT.HTML (MEASUREMENTS, BREADCRUMBS, UNIT CONVERSION)
        # ----------------------------------------------------
        print("\n--- 4. Auditing product.html Across Diverse Garment Types ---")
        test_ids = ["MB-01", "MB-02", "MB-03", "MB-06", "MB-08", "MB-09", "MB-12"]

        for pid in test_ids:
            p_data = next((x for x in PRODUCTS if x["id"] == pid), None)
            if not p_data:
                continue

            print(f"\n  Inspecting Product {pid}: {p_data['name']}")
            await page.goto(f"{BASE_URL}/product.html?id={pid}", wait_until="domcontentloaded")
            await page.wait_for_selector("#pdpTitle")

            # Nav match
            nav_links = await page.locator(".site-header .nav-links a").all_text_contents()
            nav_match = [n.strip() for n in nav_links] == EXPECTED_NAV

            # Breadcrumb check
            breadcrumb_cat = (await page.locator("#breadcrumbCategory").inner_text()).strip()
            breadcrumb_href = await page.locator("#breadcrumbCategory").evaluate("el => el.getAttribute('href') || el.href")
            breadcrumb_title = (await page.locator("#breadcrumbTitle").inner_text()).strip()
            breadcrumb_pass = (p_data["category"].lower() in breadcrumb_cat.lower() and "collections.html?cat=" in breadcrumb_href)

            # Title check
            title_text = await page.locator("#pdpTitle").inner_text()
            title_match = p_data["name"] in title_text

            # Matrix table CM measurements
            meas_table = page.locator("#matrixTableBody")
            cm_rows = {}
            if await meas_table.count() > 0:
                rows = await meas_table.locator("tr").all()
                for row in rows:
                    cells = await row.locator("td").all_text_contents()
                    if len(cells) == 2:
                        cm_rows[cells[0].strip()] = cells[1].strip()

            # Unit toggle to INCHES
            unit_btn_in = page.locator("#unitInBtn")
            in_rows = {}
            toggle_success = True

            if await unit_btn_in.count() > 0:
                await unit_btn_in.click()
                await page.wait_for_timeout(150)
                rows_in = await meas_table.locator("tr").all()
                for row in rows_in:
                    cells = await row.locator("td").all_text_contents()
                    if len(cells) == 2:
                        in_rows[cells[0].strip()] = cells[1].strip()

                for metric, cm_str in cm_rows.items():
                    if "cm" in cm_str.lower():
                        try:
                            cm_val = float(cm_str.replace("cm", "").strip())
                            in_str = in_rows.get(metric, "")
                            in_val = float(in_str.replace("in", "").replace('"', '').strip())
                            expected_in = round(cm_val / 2.54, 1)
                            diff = abs(in_val - expected_in)
                            if diff > 0.3:
                                toggle_success = False
                                print(f"    WARNING: Conversion discrepancy for {metric}: {cm_val} cm -> {in_val} in (expected {expected_in} in)")
                        except ValueError:
                            pass

            # Reset unit back to CM
            await page.locator("#unitCmBtn").click()

            # Size selection
            size_buttons = page.locator("#sizePillsContainer .pdp-size-btn")
            size_btn_count = await size_buttons.count()
            size_switch_pass = True
            if size_btn_count > 1:
                second_btn = size_buttons.nth(1)
                second_size_label = (await second_btn.inner_text()).strip()
                await second_btn.click()
                await page.wait_for_timeout(150)
                active_size_text = await page.locator("#activeSizeBadge").inner_text()
                size_switch_pass = second_size_label in active_size_text

            # Complete the look
            styled_with_count = await page.locator("#styledWithContainer .styled-item-card").count()
            expected_styled_count = len(p_data.get("styled_with", []))
            styled_pass = (styled_with_count == expected_styled_count)

            pdp_pass = nav_match and title_match and breadcrumb_pass and toggle_success and size_switch_pass and styled_pass
            audit_results["product_measurements"][pid] = {
                "name": p_data["name"],
                "nav_match": nav_match,
                "title_match": title_match,
                "breadcrumb_pass": breadcrumb_pass,
                "cm_metrics": len(cm_rows),
                "unit_toggle_pass": toggle_success,
                "size_switch_pass": size_switch_pass,
                "styled_with_rendered": styled_with_count,
                "pass": pdp_pass
            }

            print(f"    Nav: {nav_match} | Title: {title_match} | Breadcrumb: {breadcrumb_pass}")
            print(f"    Metrics Count: {len(cm_rows)} | Unit Toggle: {toggle_success} | Size Switch: {size_switch_pass} | Styled With: {styled_with_count}")
            if not pdp_pass:
                audit_results["overall_pass"] = False

            shot_name = f"audit_pdp_{pid}.png"
            await page.screenshot(path=os.path.join(OUTPUT_DIR, shot_name), full_page=False)
            audit_results["screenshots"].append(shot_name)

        # ----------------------------------------------------
        # 5. AUDIT PAVILION.HTML (VIRTUAL FITTING PAVILION)
        # ----------------------------------------------------
        print("\n--- 5. Auditing pavilion.html (Virtual Fitting Pavilion) ---")
        await page.goto(f"{BASE_URL}/pavilion.html", wait_until="domcontentloaded")
        await page.wait_for_selector("#visionCanvas")
        await page.wait_for_timeout(600)  # Ensure canvas image onload fires

        # Nav match
        nav_links = await page.locator(".site-header .nav-links a").all_text_contents()
        nav_match = [n.strip() for n in nav_links] == EXPECTED_NAV
        audit_results["nav_consistency"]["pavilion.html"] = {
            "found": [n.strip() for n in nav_links],
            "pass": nav_match
        }
        print(f"  Nav match: {nav_match}")

        # Footer check
        footer_cols = await page.locator(".site-footer .footer-col").count()
        footer_bottom = await page.locator(".site-footer .footer-bottom").inner_text()
        footer_pass = (footer_cols == 4 and "Marko Baku Atelier Worldwide" in footer_bottom)
        audit_results["footer_consistency"]["pavilion.html"] = {
            "columns": footer_cols,
            "has_copyright": "Marko Baku Atelier Worldwide" in footer_bottom,
            "pass": footer_pass
        }
        print(f"  Footer columns: {footer_cols} [Pass: {footer_pass}]")

        # Canvas check
        canvas_visible = await page.locator("#visionCanvas").is_visible()
        print(f"  Vision Canvas visible: {canvas_visible}")

        # Capture unscrolled scanner screenshot immediately
        scanner_shot = "audit_pavilion_scanner.png"
        await page.locator(".vision-card.highlight").screenshot(path=os.path.join(OUTPUT_DIR, scanner_shot))
        audit_results["screenshots"].append(scanner_shot)
        print(f"  Captured unscrolled scanner element: {scanner_shot}")

        # Archetype preset clicks & biometrics check
        # 1) Test Showroom Tailored preset (baku_editorial)
        editorial_btn = page.locator(".archetype-chip", has_text="Showroom Tailored")
        await editorial_btn.click()
        await page.wait_for_timeout(300)

        height_editorial = (await page.locator("#statHeight").inner_text()).strip()
        build_editorial = (await page.locator("#statBuild").inner_text()).strip()
        silk_editorial = (await page.locator("#verdictSizeSilk").inner_text()).strip()
        editorial_pass = ("184 cm" in height_editorial and "Tailored" in build_editorial and "XL" in silk_editorial)
        print(f"  Editorial Preset: Height '{height_editorial}', Build '{build_editorial}', Silk '{silk_editorial}' [Pass: {editorial_pass}]")

        # 2) Test Athletic Interlock preset (baku_athletic)
        athletic_btn = page.locator(".archetype-chip", has_text="Athletic Interlock")
        await athletic_btn.click()
        await page.wait_for_timeout(300)

        height_athletic = (await page.locator("#statHeight").inner_text()).strip()
        silk_athletic = (await page.locator("#verdictSizeSilk").inner_text()).strip()
        athletic_pass = ("178 cm" in height_athletic and "Medium" in silk_athletic)
        print(f"  Athletic Preset: Height '{height_athletic}', Silk '{silk_athletic}' [Pass: {athletic_pass}]")

        # 3) Test Sartorial Tracksuit preset (baku_fendi)
        fendi_btn = page.locator(".archetype-chip", has_text="Sartorial Tracksuit")
        await fendi_btn.click()
        await page.wait_for_timeout(300)

        height_fendi = (await page.locator("#statHeight").inner_text()).strip()
        build_fendi = (await page.locator("#statBuild").inner_text()).strip()
        fendi_pass = ("180 cm" in height_fendi and "Sartorial" in build_fendi)
        print(f"  Fendi Preset: Height '{height_fendi}', Build '{build_fendi}' [Pass: {fendi_pass}]")

        # 4) Reset to Baku House Model (baku_master)
        master_btn = page.locator(".archetype-chip", has_text="Baku House Model")
        await master_btn.click()
        await page.wait_for_timeout(300)

        height_master = (await page.locator("#statHeight").inner_text()).strip()
        build_master = (await page.locator("#statBuild").inner_text()).strip()
        master_pass = ("182 cm" in height_master and "Athletic Caspian" in build_master)
        print(f"  Baku House Master Preset: Height '{height_master}', Build '{build_master}' [Pass: {master_pass}]")

        # 4b) Test Height Fine-Calibration Slider (Fail-Safe Dial)
        slider_locator = page.locator("#heightSlider")
        slider_exists = await slider_locator.is_visible()
        initial_slider_val = await slider_locator.input_value()
        print(f"  Height Slider visible: {slider_exists}, Initial Value: {initial_slider_val}")

        # Dial slider to 192 cm (Tall Stature test)
        await slider_locator.fill("192")
        await slider_locator.dispatch_event("input")
        await page.wait_for_timeout(250)

        h192_readout = (await page.locator("#sliderHeightVal").inner_text()).strip()
        h192_stat = (await page.locator("#statHeight").inner_text()).strip()
        h192_silk = (await page.locator("#verdictSizeSilk").inner_text()).strip()
        h192_denim = (await page.locator("#verdictSizeDenim").inner_text()).strip()
        slider_192_pass = ("192 cm" in h192_readout and "192 cm" in h192_stat and "XL" in h192_silk and "34" in h192_denim)
        print(f"  Slider dial to 192 cm: Readout '{h192_readout}', Silk '{h192_silk}', Denim '{h192_denim}' [Pass: {slider_192_pass}]")

        # Dial slider to 170 cm (Compact Stature test)
        await slider_locator.fill("170")
        await slider_locator.dispatch_event("input")
        await page.wait_for_timeout(250)

        h170_readout = (await page.locator("#sliderHeightVal").inner_text()).strip()
        h170_stat = (await page.locator("#statHeight").inner_text()).strip()
        h170_silk = (await page.locator("#verdictSizeSilk").inner_text()).strip()
        h170_denim = (await page.locator("#verdictSizeDenim").inner_text()).strip()
        slider_170_pass = ("170 cm" in h170_readout and "170 cm" in h170_stat and "Small" in h170_silk and "30" in h170_denim)
        print(f"  Slider dial to 170 cm: Readout '{h170_readout}', Silk '{h170_silk}', Denim '{h170_denim}' [Pass: {slider_170_pass}]")

        # Reset slider to 182 cm
        await slider_locator.fill("182")
        await slider_locator.dispatch_event("input")
        await page.wait_for_timeout(250)

        # 5) Test Curated 4-Piece Ensemble Addition to Bag
        initial_cart_badge = (await page.locator("#cartCount").inner_text()).strip()
        ensemble_btn = page.locator(".btn-add-ensemble")
        await ensemble_btn.click()
        await page.wait_for_timeout(400)

        updated_cart_badge = (await page.locator("#cartCount").inner_text()).strip()
        cart_drawer_active = await page.locator("#cartDrawer").evaluate("el => el.classList.contains('open')")
        cart_items_count = await page.locator("#cartItemsList .cart-item").count()
        ensemble_cart_pass = (int(updated_cart_badge) >= 4 and cart_drawer_active and cart_items_count >= 4)
        print(f"  Add Curated Look to Bag: Badge {updated_cart_badge}, Drawer Open: {cart_drawer_active}, Items: {cart_items_count} [Pass: {ensemble_cart_pass}]")

        # Close cart drawer
        await page.locator("#cartCloseBtn").click()
        await page.wait_for_timeout(300)

        pavilion_pass = (nav_match and footer_pass and canvas_visible and editorial_pass and athletic_pass and fendi_pass and master_pass and ensemble_cart_pass)
        audit_results["pavilion_integrity"] = {
            "nav_match": nav_match,
            "footer_pass": footer_pass,
            "canvas_visible": canvas_visible,
            "editorial_preset_pass": editorial_pass,
            "athletic_preset_pass": athletic_pass,
            "fendi_preset_pass": fendi_pass,
            "master_preset_pass": master_pass,
            "ensemble_cart_pass": ensemble_cart_pass,
            "pass": pavilion_pass
        }

        if not pavilion_pass:
            audit_results["overall_pass"] = False

        # Scroll back to top before capturing viewport
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(300)

        shot_name = "audit_pavilion.png"
        await page.screenshot(path=os.path.join(OUTPUT_DIR, shot_name), full_page=False)
        audit_results["screenshots"].append(shot_name)

        # For full_page screenshot, neutralize sticky positioning temporarily so header and cards don't ghost during scroll stitching
        await page.evaluate("""() => {
            document.querySelectorAll('.site-header, .vision-card.highlight').forEach(el => {
                el.style.position = 'relative';
                el.style.top = 'auto';
            });
        }""")
        fullpage_shot = "audit_pavilion_fullpage.png"
        await page.screenshot(path=os.path.join(OUTPUT_DIR, fullpage_shot), full_page=True)
        audit_results["screenshots"].append(fullpage_shot)

        await browser.close()

    audit_results["console_errors"] = console_errors
    report_path = os.path.join(OUTPUT_DIR, "audit_summary.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2)

    print("\n==================================================")
    print(f"AUDIT COMPLETE — OVERALL PASS: {audit_results['overall_pass']}")
    print(f"Audit Summary saved to: {report_path}")
    print("==================================================")
    return audit_results["overall_pass"]

if __name__ == "__main__":
    passed = asyncio.run(run_audit())
    sys.exit(0 if passed else 1)
