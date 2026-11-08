import os
import glob
import re

def extract_schemas():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'projects', 'sayyafac', 'website'))
    
    # Pattern to match exact script tags containing application/ld+json
    script_pattern = re.compile(
        r'(<script\b[^>]*\btype=["\']application/ld\+json["\'][^>]*>[\s\S]*?</script>)',
        re.IGNORECASE
    )
    title_pattern = re.compile(r'<title\b[^>]*>([\s\S]*?)</title>', re.IGNORECASE)
    canonical_pattern = re.compile(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)["\']', re.IGNORECASE)
    
    # Priority order for pages
    priority = [
        "index.html",
        "split-ac-installation-technician/index.html",
        "maintenance/index.html",
        "cleaning/index.html",
        "copper-piping/index.html",
        "services/index.html",
        "about/index.html",
        "contact/index.html",
        "articles/index.html",
        "articles/split-ac-guide/index.html",
        "articles/freon-types-guide/index.html",
        "articles/water-leakage-guide/index.html",
        "articles/deep-cleaning-guide/index.html",
        "articles/taif-winter-heating-guide/index.html",
        "privacy/index.html",
        "terms/index.html",
        "404.html"
    ]
    
    found_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)
    rel_files = [os.path.relpath(f, base_dir).replace('\\', '/') for f in found_files]
    
    # Sort files according to priority
    sorted_files = []
    for p in priority:
        if p in rel_files:
            sorted_files.append(p)
    for r in rel_files:
        if r not in sorted_files:
            sorted_files.append(r)
            
    extracted_items = []
    
    for rel_path in sorted_files:
        full_path = os.path.join(base_dir, rel_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        scripts = script_pattern.findall(content)
        
        title_match = title_pattern.search(content)
        title = title_match.group(1).strip() if title_match else "بدون عنوان"
        # Clean title spaces
        title = re.sub(r'\s+', ' ', title)
        
        canonical_match = canonical_pattern.search(content)
        canonical = canonical_match.group(1).strip() if canonical_match else ""
        
        route = "/" if rel_path == "index.html" else "/" + rel_path.replace("index.html", "")
        
        extracted_items.append({
            'rel_path': rel_path,
            'full_path': full_path,
            'route': route,
            'title': title,
            'canonical': canonical,
            'scripts': scripts
        })
        
    # Generate output text
    total_scripts = sum(len(item['scripts']) for item in extracted_items)
    pages_with_schemas = sum(1 for item in extracted_items if len(item['scripts']) > 0)
    
    lines = []
    lines.append("=" * 90)
    lines.append("SAYYAF AC - JSON-LD (application/ld+json) SCHEMA MARKUP COLLECTION")
    lines.append("مجموعة وسوم الاسكيما (Schema.org) المستخرجة لجميع صفحات ومقالات موقع صياف للتكييف")
    lines.append(f"إجمالي الصفحات المفحوصة: {len(extracted_items)} | الصفحات التي تحتوي اسكيما: {pages_with_schemas} | إجمالي وسوم الاسكيما: {total_scripts}")
    lines.append("=" * 90)
    lines.append("")
    lines.append("فهرس الصفحات والمقالات (TABLE OF CONTENTS):")
    lines.append("-" * 90)
    
    idx = 1
    for item in extracted_items:
        if not item['scripts']:
            continue
        lines.append(f"  {idx:02d}. [{item['route']}] - {item['title']}")
        lines.append(f"      مسار الملف: projects/sayyafac/website/{item['rel_path']}")
        lines.append(f"      الرابط الدائم: {item['canonical']}")
        lines.append("")
        idx += 1
        
    lines.append("=" * 90)
    lines.append("بداية وسوم الاسكيما المستخرجة (كاملة بجميع محتوياتها ووسوم script كما هي)")
    lines.append("START OF EXTRACTED SCHEMA SCRIPTS")
    lines.append("=" * 90)
    lines.append("\n")
    
    script_idx = 1
    for item in extracted_items:
        if not item['scripts']:
            continue
            
        lines.append("/* " + "=" * 84 + " */")
        lines.append(f"/* PAGE #{script_idx:02d}: {item['title']}")
        lines.append(f"/* ROUTE:     {item['route']}")
        lines.append(f"/* CANONICAL: {item['canonical']}")
        lines.append(f"/* FILE PATH: projects/sayyafac/website/{item['rel_path']}")
        lines.append(f"/* SCHEMAS:   {len(item['scripts'])} script tag(s)")
        lines.append("/* " + "=" * 84 + " */")
        lines.append("")
        
        for s_num, s_content in enumerate(item['scripts'], 1):
            if len(item['scripts']) > 1:
                lines.append(f"<!-- Tag #{s_num} for {item['route']} -->")
            lines.append(s_content.strip())
            lines.append("")
            
        lines.append("\n" + "#" * 90 + "\n\n")
        script_idx += 1
        
    output_content = "\n".join(lines)
    
    # Save to both .txt and .html in root workspace
    output_txt = os.path.abspath(os.path.join(os.path.dirname(__file__), 'all_ld_json_schemas.txt'))
    output_html = os.path.abspath(os.path.join(os.path.dirname(__file__), 'all_ld_json_schemas.html'))
    
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(output_content)
        
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(output_content)
        
    print(f"Successfully processed {len(extracted_items)} files.")
    print(f"Extracted {total_scripts} schema scripts from {pages_with_schemas} pages.")
    print(f"Saved to:")
    print(f"  - {output_txt}")
    print(f"  - {output_html}")

if __name__ == '__main__':
    extract_schemas()
