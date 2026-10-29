import os
import json
import re

def validate_all_articles():
    articles = [
        'split-ac-guide',
        'water-leakage-guide',
        'freon-types-guide',
        'deep-cleaning-guide',
        'taif-winter-heating-guide'
    ]
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'website', 'articles')

    all_ok = True
    for art in articles:
        p = os.path.join(base_dir, art, 'index.html')
        if not os.path.exists(p):
            print(f"[FAIL] Missing {p}")
            all_ok = False
            continue
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. Canonical trailing slash
        m_can = re.search(r'<link rel="canonical" href="([^"]+)">', html)
        if not m_can or not m_can.group(1).endswith('/'):
            print(f"[FAIL] Bad canonical in {art}: {m_can.group(1) if m_can else None}")
            all_ok = False

        # 2. og:type == article
        if '<meta property="og:type" content="article">' not in html:
            print(f"[FAIL] og:type not article in {art}")
            all_ok = False

        # 3. JSON-LD valid
        m_json = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        if not m_json:
            print(f"[FAIL] No JSON-LD in {art}")
            all_ok = False
        else:
            try:
                d = json.loads(m_json.group(1))
                assert '@graph' in d
                types = []
                for n in d['@graph']:
                    t = n.get('@type')
                    if isinstance(t, list):
                        types.extend(t)
                    else:
                        types.append(t)
                assert 'Article' in types
                assert 'BreadcrumbList' in types
                assert 'Organization' in types
            except Exception as e:
                print(f"[FAIL] JSON-LD error in {art}: {e}")
                all_ok = False

        # 4. Hours in footer
        if '07:00 ص – 11:50 م' not in html or '02:00 م – 11:50 م' not in html:
            print(f"[FAIL] Missing hours in {art}")
            all_ok = False

        # 5. Phone
        if '0538972324' not in html:
            print(f"[FAIL] Missing phone in {art}")
            all_ok = False

        # 6. Author
        if 'الفني أبو عيسى' not in html:
            print(f"[FAIL] Missing author in {art}")
            all_ok = False

        print(f"[PASS] {art} fully verified!")

    if all_ok:
        print("\nALL 5 ARTICLES VERIFIED SUCCESSFULLY WITH ZERO ERRORS!")
    return all_ok

if __name__ == '__main__':
    ok = validate_all_articles()
    exit(0 if ok else 1)
