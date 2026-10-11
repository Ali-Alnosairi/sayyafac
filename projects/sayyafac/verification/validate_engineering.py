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
        (os.path.join(base_dir, 'installation', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'maintenance', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'articles', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'articles', 'split-ac-installation-taif', 'index.html'), 'article', True),
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

    # 4. Check llms.txt & robots.txt & sitemap.xml
    llms_path = os.path.join(base_dir, 'llms.txt')
    robots_path = os.path.join(base_dir, 'robots.txt')
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')

    if not os.path.exists(llms_path):
        errors.append("Missing llms.txt")
    else:
        with open(llms_path, 'r', encoding='utf-8') as f:
            llms_content = f.read()
            if '0538972324' in llms_content and 'أم العراد' in llms_content:
                passes.append("llms.txt contains Single Source of Truth entity data")
            else:
                errors.append("llms.txt missing core entity facts")

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
            if 'https://sayyafac.com/installation/' in sitemap_content and '<image:image>' in sitemap_content:
                passes.append("sitemap.xml has trailing slash URLs and Image Sitemap namespace")
            else:
                errors.append("sitemap.xml incomplete")

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
