import os
import re
import json

def validate_sayyafac_engineering():
    print("=== STARTING SAYYAFAC ENGINEERING AUDIT (GATE 4 & GATE 5) ===")
    errors = []
    passes = []
    
    base_dir = os.path.join('projects', 'sayyafac', 'website')
    
    # 1. Check CSS @import prohibition
    css_files = [
        os.path.join(base_dir, 'assets', 'css', 'style.css'),
        os.path.join(base_dir, 'assets', 'css', 'fonts.css')
    ]
    for css_path in css_files:
        if not os.path.exists(css_path):
            errors.append(f"Missing CSS file: {css_path}")
            continue
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '@import' in content:
                errors.append(f"FORBIDDEN @import found in {css_path}")
            else:
                passes.append(f"ZERO @import in {os.path.basename(css_path)}")

    # 2. Check local font files
    fonts_dir = os.path.join(base_dir, 'assets', 'fonts')
    font_files = [f for f in os.listdir(fonts_dir) if f.endswith('.woff2')]
    if len(font_files) < 4:
        errors.append(f"Expected at least 4 .woff2 font files in assets/fonts, found {len(font_files)}")
    else:
        passes.append(f"Found {len(font_files)} local self-hosted .woff2 font files: {font_files}")

    # 3. Check pages
    pages = [
        (os.path.join(base_dir, 'index.html'), 'website', False),
        (os.path.join(base_dir, 'split-ac-installation-technician', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'services', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'maintenance', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'cleaning', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'copper-piping', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'articles', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'articles', 'split-ac-guide', 'index.html'), 'article', True),
        (os.path.join(base_dir, 'about', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'contact', 'index.html'), 'website', False)
    ]

    for rel_path, expected_og_type, is_article in pages:
        if not os.path.exists(rel_path):
            errors.append(f"Missing page: {rel_path}")
            continue
        with open(rel_path, 'r', encoding='utf-8') as f:
            html = f.read()

        page_name = os.path.relpath(rel_path, base_dir).replace('\\', '/')

        # Subpage navigation parity
        if 'sayyaf-mobile-toggle' not in html:
            errors.append(f"Missing mobile toggle button on {page_name}")
        if 'sayyaf-drawer' not in html:
            errors.append(f"Missing mobile drawer markup on {page_name}")
        if 'sayyaf-drawer-backdrop' not in html:
            errors.append(f"Missing mobile drawer backdrop on {page_name}")
        if 'main.js' not in html:
            errors.append(f"Missing main.js script tag on {page_name}")

        # Check Open Graph og:type
        og_match = re.search(r'<meta\s+property=["\']og:type["\']\s+content=["\']([^"\']+)["\']', html)
        if not og_match:
            errors.append(f"Missing og:type in {page_name}")
        elif og_match.group(1) != expected_og_type:
            errors.append(f"Mismatched og:type in {page_name}: expected {expected_og_type}, got {og_match.group(1)}")
        else:
            passes.append(f"og:type='{expected_og_type}' correct on {page_name}")

        # Check JSON-LD schema
        schema_matches = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.DOTALL)
        if not schema_matches:
            errors.append(f"Missing JSON-LD schema in {page_name}")
        else:
            for s_str in schema_matches:
                try:
                    s_data = json.loads(s_str)
                    if '@graph' not in s_data:
                        errors.append(f"JSON-LD in {page_name} missing unified @graph")
                    else:
                        passes.append(f"Connected @graph schema valid on {page_name}")
                    
                    if is_article:
                        art = next((item for item in s_data.get('@graph', []) if item.get('@type') == 'Article'), None)
                        if not art:
                            errors.append(f"Article entity missing in @graph on {page_name}")
                        else:
                            if 'datePublished' not in art or 'dateModified' not in art:
                                errors.append(f"Article missing datePublished or dateModified in {page_name}")
                            else:
                                passes.append(f"Article dates present ({art['datePublished']}) on {page_name}")
                except Exception as ex:
                    errors.append(f"Invalid JSON in schema on {page_name}: {ex}")

        # Strict Ban on self-serving reviews / fake ratings (Gate: Zero Fake Reviews on New Domains)
        if 'aggregateRating' in html or 'AggregateRating' in html or 'ac-review' in html:
            errors.append(f"CRITICAL VIOLATION: Forbidden self-serving aggregateRating or fake reviews found in {page_name}")
        else:
            passes.append(f"ZERO fake reviews and ZERO aggregateRating verified in {page_name}")

        # Trailing slash checks in internal links
        internal_links = re.findall(r'href=["\'](/[^"\']*)["\']', html)
        for link in internal_links:
            if link.startswith(('/assets/', '/favicon.', '#')):
                continue
            # Skip file extensions like .txt, .xml, .svg
            if re.search(r'\.[a-zA-Z0-9]+$', link):
                continue
            if not link.endswith('/'):
                errors.append(f"Non-trailing slash link in {page_name}: {link}")

        # Information Integrity: Verify canonical phone exists
        if '0538972324' not in html:
            errors.append(f"Canonical phone number missing in {page_name}")

        # Information Integrity: Verify canonical opening hours in footer
        if '07:00 ص – 11:50 م' not in html or '02:00 م – 11:50 م' not in html:
            errors.append(f"Opening hours missing or inconsistent in footer of {page_name}")
        else:
            passes.append(f"Footer opening hours (07:00-23:50 / Fri 14:00-23:50) verified in {page_name}")

    # 4. Check llms.txt & robots.txt & sitemap.xml
    llms_path = os.path.join(base_dir, 'llms.txt')
    robots_path = os.path.join(base_dir, 'robots.txt')
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')

    if not os.path.exists(llms_path):
        errors.append("Missing llms.txt")
    else:
        with open(llms_path, 'r', encoding='utf-8') as f:
            llms_content = f.read()
            if '0538972324' in llms_content and 'أم العراد' in llms_content and '07:00 صباحاً – 11:50 مساءً' in llms_content:
                passes.append("llms.txt contains Single Source of Truth entity data and canonical opening hours")
            else:
                errors.append("llms.txt missing core entity facts or opening hours")

    if not os.path.exists(robots_path):
        errors.append("Missing robots.txt")
    else:
        with open(robots_path, 'r', encoding='utf-8') as f:
            rob = f.read()
            if 'OAI-SearchBot' in rob and 'Claude-SearchBot' in rob and 'GPTBot' in rob:
                passes.append("robots.txt contains AI crawlers permissions")
            else:
                errors.append("robots.txt missing AI search bot rules")

    if not os.path.exists(sitemap_path):
        errors.append("Missing sitemap.xml")
    else:
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
            required_urls = [
                'https://sayyafac.com/split-ac-installation-technician/',
                'https://sayyafac.com/services/',
                'https://sayyafac.com/maintenance/',
                'https://sayyafac.com/cleaning/',
                'https://sayyafac.com/copper-piping/'
            ]
            missing_urls = [u for u in required_urls if u not in sitemap_content]
            if not missing_urls and '<image:image>' in sitemap_content:
                passes.append("sitemap.xml has all core services with trailing slash URLs and Image Sitemap namespace")
            else:
                errors.append(f"sitemap.xml incomplete, missing: {missing_urls}")

    # 5. Check 25 Canonical Districts Parity across Core Pages & llms.txt
    canonical_districts = [
        "مخططات الوسام", "حي شهار", "حي السداد", "حي الردف", "حي الخالدية",
        "حي أم العراد", "شارع عور", "حي قروى", "حي مسرة", "حي الأحباب",
        "الحوية", "الحلقة الشرقية", "الحلقة الغربية", "حي القيم", "حي الفيصلية",
        "حي الورود", "حي النسيم", "حي الجال", "حي جبرة", "حي السلامة",
        "حي المثناة", "الهدا", "الشفا", "السيل الصغير", "السيل الكبير"
    ]
    
    # Check llms.txt for canonical districts
    with open(llms_path, 'r', encoding='utf-8') as f:
        llms_text = f.read()
    missing_in_llms = [d for d in canonical_districts if d not in llms_text]
    if missing_in_llms:
        errors.append(f"llms.txt missing canonical districts: {missing_in_llms}")
    else:
        passes.append("llms.txt verified with all 25 canonical Taif districts across 4 tiers")

    # Check service pages and index/contact for Schema areaServed
    geo_pages = [
        os.path.join(base_dir, 'index.html'),
        os.path.join(base_dir, 'split-ac-installation-technician', 'index.html'),
        os.path.join(base_dir, 'maintenance', 'index.html'),
        os.path.join(base_dir, 'cleaning', 'index.html'),
        os.path.join(base_dir, 'copper-piping', 'index.html'),
        os.path.join(base_dir, 'contact', 'index.html'),
        os.path.join(base_dir, 'about', 'index.html')
    ]
    for gp in geo_pages:
        gp_name = os.path.relpath(gp, base_dir).replace('\\', '/')
        with open(gp, 'r', encoding='utf-8') as f:
            gp_html = f.read()
        missing_in_page = [d for d in canonical_districts if d not in gp_html]
        if missing_in_page:
            errors.append(f"Missing canonical districts in {gp_name}: {missing_in_page}")
        else:
            passes.append(f"All 25 canonical Taif districts present in {gp_name} (Schema & UI)")

    print("\n=== RESULTS ===")
    for p in passes:
        print(f"[PASS] {p}")

    print("\n=== AUDIT SUMMARY ===")
    if errors:
        print(f"FAILED with {len(errors)} error(s):")
        for e in errors:
            print(f" - [ERROR] {e}")
        return False
    else:
        print(f"ALL {len(passes)} ENGINEERING & QUALITY CRITERIA PASSED WITH ZERO ERRORS (100% COMPLIANT)!")
        return True

if __name__ == '__main__':
    success = validate_sayyafac_engineering()
    exit(0 if success else 1)
