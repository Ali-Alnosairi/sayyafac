import os
import re
import json

def validate_sayyafac_engineering():
    print("=== STARTING SAYYAFAC ENGINEERING AUDIT (GATE 4 & GATE 5 EXPANDED) ===")
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

    # Gather all HTML files site-wide
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    # 3. Check core pages for navigation, og:type, JSON-LD, and basic integrity
    pages = [
        (os.path.join(base_dir, 'index.html'), 'website', False),
        (os.path.join(base_dir, 'split-ac-installation-technician', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'services', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'maintenance', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'cleaning', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'copper-piping', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'articles', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'articles', 'split-ac-guide', 'index.html'), 'article', True),
        (os.path.join(base_dir, 'articles', 'water-leakage-guide', 'index.html'), 'article', True),
        (os.path.join(base_dir, 'articles', 'freon-types-guide', 'index.html'), 'article', True),
        (os.path.join(base_dir, 'articles', 'deep-cleaning-guide', 'index.html'), 'article', True),
        (os.path.join(base_dir, 'articles', 'taif-winter-heating-guide', 'index.html'), 'article', True),
        (os.path.join(base_dir, 'about', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'contact', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'privacy', 'index.html'), 'website', False),
        (os.path.join(base_dir, 'terms', 'index.html'), 'website', False)
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
            # Skip file extensions like .txt, .xml, .svg, .webmanifest
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

            if 'LLM-Txt:' in rob or 'LLM-Full-Txt:' in rob:
                errors.append("Non-standard directives (LLM-Txt) found in robots.txt causing Google Search Console syntax errors")
            else:
                passes.append("robots.txt has ZERO non-standard syntax errors")

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

    # 4b. Gate: Dual Favicon Architecture & SERP Icon Integrity (Lesson 29)
    favicon_ico_path = os.path.join(base_dir, 'favicon.ico')
    favicon_svg_path = os.path.join(base_dir, 'favicon.svg')
    if not os.path.exists(favicon_ico_path):
        errors.append("Missing root favicon.ico (triggers 404 on Googlebot favicon crawl)")
    elif os.path.getsize(favicon_ico_path) < 100:
        errors.append(f"Root favicon.ico is empty or invalid size: {os.path.getsize(favicon_ico_path)} bytes")
    else:
        passes.append("Root favicon.ico verified and valid (prevents Googlebot SERP icon 404)")

    if not os.path.exists(favicon_svg_path):
        errors.append("Missing root favicon.svg")
    else:
        passes.append("Root favicon.svg verified")

    missing_ico_link = []
    for hf in html_files:
        rel = os.path.relpath(hf, base_dir).replace('\\', '/')
        with open(hf, 'r', encoding='utf-8') as f:
            c = f.read()
        if '<link rel="icon" href="/favicon.ico" sizes="any">' not in c:
            missing_ico_link.append(rel)
    if missing_ico_link:
        errors.append(f"Pages missing explicit favicon.ico link: {missing_ico_link}")
    else:
        passes.append(f"Dual favicon architecture verified across all {len(html_files)} HTML pages")

    # 5. Check 25 Canonical Districts Parity across Core Pages & llms.txt
    canonical_districts = [
        "مخططات الوسام", "حي شهار", "حي السداد", "حي الردف", "حي الخالدية",
        "حي أم العراد", "شارع عور", "حي قروى", "حي مسرة", "حي الأحباب",
        "الحوية", "الحلقة الشرقية", "الحلقة الغربية", "حي القيم", "حي الفيصلية",
        "حي الورود", "حي النسيم", "حي الجال", "حي جبرة", "حي السلامة",
        "حي المثناة", "الهدا", "الشفا", "السيل الصغير", "السيل الكبير"
    ]
    
    with open(llms_path, 'r', encoding='utf-8') as f:
        llms_text = f.read()
    missing_in_llms = [d for d in canonical_districts if d not in llms_text]
    if missing_in_llms:
        errors.append(f"llms.txt missing canonical districts: {missing_in_llms}")
    else:
        passes.append("llms.txt verified with all 25 canonical Taif districts across 4 tiers")

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

    # 6. Gate: Heading Hierarchy Integrity (WCAG 2.1 A SC 1.3.1 - Zero Heading Skips)
    heading_skip_errors = 0
    for hf in html_files:
        rel = os.path.relpath(hf, base_dir).replace('\\', '/')
        with open(hf, 'r', encoding='utf-8') as f:
            h_content = f.read()
        headings = re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', h_content, re.DOTALL | re.IGNORECASE)
        prev_lvl = 0
        for lvl_str, h_text in headings:
            lvl = int(lvl_str)
            if prev_lvl > 0 and lvl > prev_lvl + 1:
                errors.append(f"Heading skip in {rel}: <h{prev_lvl}> followed by <h{lvl}> ({h_text.strip()[:30]})")
                heading_skip_errors += 1
            prev_lvl = lvl
    if heading_skip_errors == 0:
        passes.append(f"Gate 6: Heading hierarchy verified 100% compliant (zero skips) across all {len(html_files)} HTML pages")

    # 7. Gate: Schema OfferCatalog & Mathematical Pricing Bounds
    catalog_pages = [
        'index.html',
        'split-ac-installation-technician/index.html',
        'maintenance/index.html',
        'cleaning/index.html',
        'copper-piping/index.html'
    ]
    for cp in catalog_pages:
        full_p = os.path.join(base_dir, cp)
        with open(full_p, 'r', encoding='utf-8') as f:
            cp_content = f.read()
        schema_matches = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', cp_content, re.DOTALL)
        found_catalog = False
        for s_str in schema_matches:
            data = json.loads(s_str)
            graph = data.get('@graph', [])
            
            # Check unified Organization priceRange
            for node in graph:
                if any(t in node.get('@type', []) for t in ['Organization', 'HVACBusiness']):
                    if node.get('priceRange') != 'SAR 50 - SAR 350':
                        errors.append(f"Mismatched priceRange on Organization in {cp}: {node.get('priceRange')}")
                    else:
                        passes.append(f"priceRange 'SAR 50 - SAR 350' verified on {cp}")
            
            # Check Service OfferCatalog & AggregateOffer
            for node in graph:
                if node.get('@type') == 'Service' and 'hasOfferCatalog' in node:
                    cat = node['hasOfferCatalog']
                    items = cat.get('itemListElement', [])
                    if len(items) < 3:
                        errors.append(f"OfferCatalog in {cp} has fewer than 3 offers: {len(items)}")
                    else:
                        prices = [float(it['price']) for it in items if 'price' in it]
                        offers = node.get('offers', {})
                        if offers.get('@type') != 'AggregateOffer':
                            errors.append(f"Service in {cp} offers is not AggregateOffer: {offers.get('@type')}")
                        else:
                            if int(offers.get('offerCount', 0)) != len(items):
                                errors.append(f"offerCount ({offers.get('offerCount')}) does not match catalog count ({len(items)}) in {cp}")
                            if float(offers.get('lowPrice', 0)) != min(prices):
                                errors.append(f"lowPrice ({offers.get('lowPrice')}) does not match min price ({min(prices)}) in {cp}")
                            
                            high_val = float(offers.get('highPrice', 0))
                            if high_val < max(prices):
                                errors.append(f"highPrice ({high_val}) cannot be lower than max base price ({max(prices)}) in {cp}")
                            
                            high_str = str(int(high_val)) if high_val.is_integer() else str(high_val)
                            if high_str not in cp_content:
                                errors.append(f"highPrice ({high_str}) not found in visible page or schema for {cp}")
                            else:
                                found_catalog = True
                                passes.append(f"OfferCatalog & AggregateOffer verified on {cp} ({len(items)} offers: {min(prices)}-{high_str} SAR)")
        if not found_catalog:
            errors.append(f"Missing hasOfferCatalog in Service schema for {cp}")

    # 8. Gate: Forbidden Technical Orthography & Jargon Blacklist
    blacklist = {
        'أرمالكس': 'Should be أرمفلكس (Armaflex)',
        'كومبروسر': 'Should be unified to كمبروسر'
    }
    scan_exts = ('.html', '.txt', '.md', '.js', '.json')
    typo_errors = 0
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(scan_exts):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fl:
                    fcontent = fl.read()
                for bad_word, advice in blacklist.items():
                    if bad_word in fcontent:
                        errors.append(f"Forbidden orthography '{bad_word}' in {os.path.relpath(fpath, base_dir)}: {advice}")
                        typo_errors += 1
    if typo_errors == 0:
        passes.append("Gate 8: Technical orthography blacklist verified 100% clean (zero forbidden typos)")

    # 9. Gate: Form Progressive Enhancement & External Link Security
    for hf in html_files:
        rel = os.path.relpath(hf, base_dir).replace('\\', '/')
        with open(hf, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check forms for progressive enhancement
        forms = re.findall(r'<form\b([^>]*)>', content, re.IGNORECASE)
        for form_attrs in forms:
            if 'sayyaf-quote-form' in form_attrs:
                if 'action="https://wa.me/966538972324"' not in form_attrs or 'method="GET"' not in form_attrs:
                    errors.append(f"Form missing progressive enhancement fallback (action/method) in {rel}")
                else:
                    passes.append(f"Quote form progressive enhancement fallback verified in {rel}")

        # Check external links for noopener noreferrer
        ext_links = re.findall(r'<a\b([^>]*)href=["\'](https?://[^"\']+)["\']([^>]*)>', content, re.IGNORECASE)
        for pre, url, post in ext_links:
            attrs = pre + " " + post
            if 'sayyafac.com' in url or 'localhost' in url:
                continue
            if 'target="_blank"' in attrs:
                if 'rel=' not in attrs:
                    errors.append(f"External link to {url} in {rel} missing rel attribute")
                else:
                    rel_match = re.search(r'rel=["\']([^"\']+)["\']', attrs)
                    if not rel_match or 'noopener' not in rel_match.group(1) or 'noreferrer' not in rel_match.group(1):
                        errors.append(f"External link to {url} in {rel} missing noopener or noreferrer: {attrs}")

    # 10. Gate: AI Grounding & Webmanifest Shaddah Branding
    if '26 حياً' in llms_text or '26 حيا' in llms_text:
        errors.append("Conflicting hardcoded count '26 حياً' found in llms.txt")
    else:
        passes.append("llms.txt clean of conflicting numeric counters")

    manifest_path = os.path.join(base_dir, 'site.webmanifest')
    with open(manifest_path, 'r', encoding='utf-8') as f:
        man_data = json.load(f)
    if 'صَيّاف للتكييف' not in man_data.get('name', ''):
        errors.append(f"site.webmanifest name missing shaddah: {man_data.get('name')}")
    else:
        passes.append("site.webmanifest name correctly includes shaddah ('صَيّاف للتكييف')")

    # 11. Gate: Connected Entity Graph Integrity & Zero Dangling Nodes
    allowed_global_roots = {
        'https://sayyafac.com/#website',
        'https://sayyafac.com/#service-catalog'
    }
    for hf in html_files:
        rel = os.path.relpath(hf, base_dir).replace('\\', '/')
        with open(hf, 'r', encoding='utf-8') as f:
            content = f.read()

        schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', content, re.DOTALL)
        if rel == '404.html':
            if len(schemas) > 0:
                errors.append(f"404.html must not contain schema markup (found {len(schemas)})")
            else:
                passes.append("404.html correctly has zero schema markup")
            continue

        if not schemas:
            errors.append(f"Missing schema markup in {rel}")
            continue

        for s_str in schemas:
            try:
                data = json.loads(s_str)
            except Exception as ex:
                errors.append(f"Invalid JSON in schema for {rel}: {ex}")
                continue

            graph = data.get('@graph', [])
            if not graph:
                errors.append(f"Schema missing @graph in {rel}")
                continue

            defined_ids = set()
            for node in graph:
                if isinstance(node, dict) and '@id' in node:
                    defined_ids.add(node['@id'])

            # Hierarchy check on WebPage nodes
            webpage_types = {'WebPage', 'ItemPage', 'AboutPage', 'ContactPage', 'CollectionPage'}
            found_webpage = False
            found_org = False
            for node in graph:
                if not isinstance(node, dict):
                    continue
                ntypes = set()
                raw_type = node.get('@type', [])
                if isinstance(raw_type, list):
                    ntypes.update(raw_type)
                elif isinstance(raw_type, str):
                    ntypes.add(raw_type)

                if ntypes.intersection(webpage_types):
                    found_webpage = True
                    part_of = node.get('isPartOf', {})
                    part_of_id = part_of.get('@id') if isinstance(part_of, dict) else part_of
                    if part_of_id == 'https://sayyafac.com/#organization':
                        errors.append(f"Invalid container hierarchy: WebPage.isPartOf points to #organization instead of #website in {rel}")
                    elif part_of_id != 'https://sayyafac.com/#website':
                        errors.append(f"WebPage.isPartOf must point to https://sayyafac.com/#website (got {part_of_id}) in {rel}")

                # Check Organization consistency
                if ntypes.intersection({'Organization', 'HVACBusiness'}):
                    found_org = True
                    # Check rich ImageObject logo
                    logo = node.get('logo')
                    if not isinstance(logo, dict) or logo.get('@type') != 'ImageObject' or not logo.get('url', '').endswith('logo.png'):
                        errors.append(f"Organization logo is not a valid ImageObject in {rel}")
                    
                    # Check sameAs typo
                    same_as = node.get('sameAs', [])
                    for url in same_as:
                        if 'sayyafac.offical' in url:
                            errors.append(f"Typo 'sayyafac.offical' found in sameAs in {rel}")
                        if 'facebook.com' in url and 'sayyafac.official' not in url:
                            errors.append(f"Mismatched Facebook profile in {rel}: {url}")

                    # Check areaServed coverage and Wikidata
                    areas = node.get('areaServed', [])
                    if len(areas) < 20:
                        errors.append(f"Organization areaServed has fewer than 20 neighborhoods ({len(areas)}) in {rel}")
                    has_taif_wikidata = False
                    for area in areas:
                        if isinstance(area, dict):
                            if area.get('@type') == 'City' and 'wikidata.org' in str(area.get('@id', '')):
                                has_taif_wikidata = True
                            if area.get('@type') == 'AdministrativeArea':
                                contained = area.get('containedInPlace', {})
                                contained_name = contained.get('name') if isinstance(contained, dict) else ''
                                if contained_name != 'الطائف':
                                    errors.append(f"areaServed item {area.get('name')} missing containedInPlace 'الطائف' in {rel}")
                    if not has_taif_wikidata:
                        errors.append(f"Organization areaServed missing primary City node with Wikidata Q168544 in {rel}")


                # Check FAQPage contextual anchoring
                if 'FAQPage' in ntypes:
                    part_of = node.get('isPartOf', {})
                    part_of_id = part_of.get('@id') if isinstance(part_of, dict) else part_of
                    about_entity = node.get('about', {})
                    about_id = about_entity.get('@id') if isinstance(about_entity, dict) else about_entity
                    if not part_of_id or '#webpage' not in part_of_id:
                        errors.append(f"FAQPage isPartOf must anchor to #webpage in {rel} (got {part_of_id})")
                    if not about_id or not any(x in about_id for x in ['#service', '#article', '#organization']):
                        errors.append(f"FAQPage about must anchor to #service, #article, or #organization in {rel} (got {about_id})")

            # Check for dangling internal nodes
            def check_pointers(obj, path=""):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if k == '@id' and path.endswith(('founder', 'author', 'provider', 'itemOffered', 'mainEntity', 'about')):
                            if isinstance(v, str) and v.startswith('https://sayyafac.com/#') and v not in defined_ids and v not in allowed_global_roots:
                                errors.append(f"Dangling node reference '{v}' at '{path}' in {rel}")
                        else:
                            check_pointers(v, f"{path}.{k}" if path else k)
                elif isinstance(obj, list):
                    for idx, item in enumerate(obj):
                        check_pointers(item, f"{path}[{idx}]")

            check_pointers(graph)
            if found_webpage and found_org:
                passes.append(f"Gate 11: Schema entity graph integrity verified in {rel} (valid hierarchy, zero dangling nodes)")

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
