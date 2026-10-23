import os
import base64
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath('projects/sayyafac/social-assets')
os.makedirs(output_dir, exist_ok=True)

website_img_dir = os.path.abspath('projects/sayyafac/website/assets/images')
os.makedirs(website_img_dir, exist_ok=True)

brain_dir = os.path.abspath(r'C:\Users\City\.gemini\antigravity\brain\7cdbb196-3bf0-400b-9a92-f1f680b148ce')
os.makedirs(brain_dir, exist_ok=True)

# Load Cairo font as base64
with open('projects/sayyafac/website/assets/fonts/cairo-v35-arabic-800.woff2', 'rb') as f:
    font_800_b64 = base64.b64encode(f.read()).decode('utf-8')
with open('projects/sayyafac/website/assets/fonts/cairo-v35-arabic-700.woff2', 'rb') as f:
    font_700_b64 = base64.b64encode(f.read()).decode('utf-8')

font_css = f"""
@font-face {{
  font-family: 'Cairo';
  font-style: normal;
  font-weight: 700;
  src: url('data:font/woff2;base64,{font_700_b64}') format('woff2');
}}
@font-face {{
  font-family: 'Cairo';
  font-style: normal;
  font-weight: 800;
  src: url('data:font/woff2;base64,{font_800_b64}') format('woff2');
}}
"""

def generate_snowflake_svg(width=500, height=500, cyan="#38bdf8", white="#ffffff"):
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Glow & Backing -->
      <circle cx="50" cy="50" r="33" fill="{cyan}" opacity="0.12" />
      
      <!-- Cross Arms -->
      <line x1="50" y1="12" x2="50" y2="88" stroke="{cyan}" stroke-width="5.5" stroke-linecap="round"/>
      <line x1="12" y1="50" x2="88" y2="50" stroke="{cyan}" stroke-width="5.5" stroke-linecap="round"/>
      
      <!-- Diagonal Arms -->
      <line x1="23" y1="23" x2="77" y2="77" stroke="{cyan}" stroke-width="5.5" stroke-linecap="round"/>
      <line x1="77" y1="23" x2="23" y2="77" stroke="{cyan}" stroke-width="5.5" stroke-linecap="round"/>
      
      <!-- Top Tips -->
      <path d="M43 20L50 12L57 20" stroke="{white}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M43 30L50 23L57 30" stroke="{cyan}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
      
      <!-- Bottom Tips -->
      <path d="M43 80L50 88L57 80" stroke="{white}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M43 70L50 77L57 70" stroke="{cyan}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
      
      <!-- Left Tips -->
      <path d="M20 43L12 50L20 57" stroke="{white}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M30 43L23 50L30 57" stroke="{cyan}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
      
      <!-- Right Tips -->
      <path d="M80 43L88 50L80 57" stroke="{white}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M70 43L77 50L70 57" stroke="{cyan}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
      
      <!-- Diagonals Tips -->
      <circle cx="23" cy="23" r="3.5" fill="{white}"/>
      <circle cx="77" cy="23" r="3.5" fill="{white}"/>
      <circle cx="23" cy="77" r="3.5" fill="{white}"/>
      <circle cx="77" cy="77" r="3.5" fill="{white}"/>
      
      <!-- Center Core Badge -->
      <circle cx="50" cy="50" r="10.5" fill="{white}" filter="drop-shadow(0px 3px 6px rgba(0,0,0,0.25))"/>
      <circle cx="50" cy="50" r="5.2" fill="{cyan}"/>
    </svg>
    """

# -------------------------------------------------------------
# 1. ICON ONLY (No text at all) - 2400 x 2400
# -------------------------------------------------------------

# A. Dark Navy
html_icon_dark = f"""
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 2400px;
  height: 2400px;
  background: radial-gradient(circle at 50% 50%, #0e3d6b 0%, #061b31 65%, #020b16 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}}
.emblem-box {{
  width: 1400px;
  height: 1400px;
  border-radius: 360px;
  background: linear-gradient(145deg, #13528c 0%, #08294a 100%);
  border: 16px solid rgba(56, 189, 248, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 50px 120px rgba(0, 0, 0, 0.6), 0 0 140px rgba(56, 189, 248, 0.35);
}}
</style>
</head>
<body>
  <div class="emblem-box">
    {generate_snowflake_svg(950, 950, "#38bdf8", "#ffffff")}
  </div>
</body>
</html>
"""

# B. Clean White
html_icon_light = f"""
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 2400px;
  height: 2400px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}}
.emblem-box {{
  width: 1400px;
  height: 1400px;
  border-radius: 360px;
  background: linear-gradient(145deg, #0b3b60 0%, #072640 100%);
  border: 16px solid rgba(2, 132, 199, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 45px 110px rgba(11, 59, 96, 0.22), 0 0 80px rgba(2, 132, 199, 0.18);
}}
</style>
</head>
<body>
  <div class="emblem-box">
    {generate_snowflake_svg(950, 950, "#38bdf8", "#ffffff")}
  </div>
</body>
</html>
"""

# C. Transparent
html_icon_transparent = f"""
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 2400px;
  height: 2400px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}}
.emblem-box {{
  width: 1400px;
  height: 1400px;
  border-radius: 360px;
  background: linear-gradient(145deg, #0b3b60 0%, #072640 100%);
  border: 16px solid #38bdf8;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 45px 110px rgba(11, 59, 96, 0.35);
}}
</style>
</head>
<body>
  <div class="emblem-box">
    {generate_snowflake_svg(950, 950, "#38bdf8", "#ffffff")}
  </div>
</body>
</html>
"""

# -------------------------------------------------------------
# 2. ARABIC TEXT ONLY: "صَيّاف للتكييف" (No English) - 2400 x 2400
# -------------------------------------------------------------

# A. Dark Navy Square Avatar
html_arabic_dark = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
{font_css}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 2400px;
  height: 2400px;
  background: radial-gradient(circle at 50% 45%, #0e3d6b 0%, #061b31 65%, #020b16 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: 'Cairo', sans-serif;
  overflow: hidden;
}}
.emblem-box {{
  width: 900px;
  height: 900px;
  border-radius: 230px;
  background: linear-gradient(145deg, #13528c 0%, #08294a 100%);
  border: 12px solid rgba(56, 189, 248, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.55), 0 0 120px rgba(56, 189, 248, 0.3);
  margin-bottom: 90px;
}}
.brand-title {{
  font-size: 210px;
  font-weight: 800;
  color: #ffffff;
  text-shadow: 0 10px 35px rgba(0, 0, 0, 0.6);
  letter-spacing: -1px;
  line-height: 1.15;
  text-align: center;
}}
</style>
</head>
<body>
  <div class="emblem-box">
    {generate_snowflake_svg(620, 620, "#38bdf8", "#ffffff")}
  </div>
  <div class="brand-title">صَيّاف للتكييف</div>
</body>
</html>
"""

# B. Clean White Square Avatar
html_arabic_light = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
{font_css}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 2400px;
  height: 2400px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: 'Cairo', sans-serif;
  overflow: hidden;
}}
.emblem-box {{
  width: 900px;
  height: 900px;
  border-radius: 230px;
  background: linear-gradient(145deg, #0b3b60 0%, #072640 100%);
  border: 12px solid rgba(2, 132, 199, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 40px 100px rgba(11, 59, 96, 0.22), 0 0 70px rgba(2, 132, 199, 0.15);
  margin-bottom: 90px;
}}
.brand-title {{
  font-size: 210px;
  font-weight: 800;
  color: #0b3b60;
  letter-spacing: -1px;
  line-height: 1.15;
  text-align: center;
}}
</style>
</head>
<body>
  <div class="emblem-box">
    {generate_snowflake_svg(620, 620, "#38bdf8", "#ffffff")}
  </div>
  <div class="brand-title">صَيّاف للتكييف</div>
</body>
</html>
"""

# C. Transparent Arabic Square
html_arabic_transparent = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
{font_css}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 2400px;
  height: 2400px;
  background: transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: 'Cairo', sans-serif;
  overflow: hidden;
}}
.emblem-box {{
  width: 900px;
  height: 900px;
  border-radius: 230px;
  background: linear-gradient(145deg, #0b3b60 0%, #072640 100%);
  border: 12px solid #38bdf8;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 40px 100px rgba(11, 59, 96, 0.35);
  margin-bottom: 90px;
}}
.brand-title {{
  font-size: 210px;
  font-weight: 800;
  color: #0b3b60;
  letter-spacing: -1px;
  line-height: 1.15;
  text-align: center;
}}
</style>
</head>
<body>
  <div class="emblem-box">
    {generate_snowflake_svg(620, 620, "#38bdf8", "#ffffff")}
  </div>
  <div class="brand-title">صَيّاف للتكييف</div>
</body>
</html>
"""

# D. Horizontal Arabic Only (3000 x 1000) - Clean White
html_arabic_horizontal_light = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
{font_css}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 3000px;
  height: 1000px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 100px;
  padding: 0 100px;
  font-family: 'Cairo', sans-serif;
  overflow: hidden;
}}
.emblem-box {{
  width: 600px;
  height: 600px;
  border-radius: 155px;
  background: linear-gradient(145deg, #0b3b60 0%, #072640 100%);
  border: 9px solid #38bdf8;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 35px 80px rgba(11, 59, 96, 0.25);
  flex-shrink: 0;
}}
.brand-title {{
  font-size: 260px;
  font-weight: 800;
  color: #0b3b60;
  line-height: 1;
  letter-spacing: -2px;
}}
</style>
</head>
<body>
  <div class="emblem-box">
    {generate_snowflake_svg(420, 420, "#38bdf8", "#ffffff")}
  </div>
  <div class="brand-title">صَيّاف للتكييف</div>
</body>
</html>
"""

# E. Horizontal Arabic Only (3000 x 1000) - Dark Navy
html_arabic_horizontal_dark = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
{font_css}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 3000px;
  height: 1000px;
  background: radial-gradient(circle at 60% 50%, #0e3d6b 0%, #061b31 65%, #020b16 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 100px;
  padding: 0 100px;
  font-family: 'Cairo', sans-serif;
  overflow: hidden;
}}
.emblem-box {{
  width: 600px;
  height: 600px;
  border-radius: 155px;
  background: linear-gradient(145deg, #13528c 0%, #08294a 100%);
  border: 9px solid rgba(56, 189, 248, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 35px 80px rgba(0, 0, 0, 0.6), 0 0 90px rgba(56, 189, 248, 0.3);
  flex-shrink: 0;
}}
.brand-title {{
  font-size: 260px;
  font-weight: 800;
  color: #ffffff;
  line-height: 1;
  letter-spacing: -2px;
  text-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}
</style>
</head>
<body>
  <div class="emblem-box">
    {generate_snowflake_svg(420, 420, "#38bdf8", "#ffffff")}
  </div>
  <div class="brand-title">صَيّاف للتكييف</div>
</body>
</html>
"""

tasks = [
    # 1. Pure Icon Only (No Text)
    ("sayyafac-icon-only-dark.png", html_icon_dark, 2400, 2400, False),
    ("sayyafac-icon-only-light.png", html_icon_light, 2400, 2400, False),
    ("sayyafac-icon-only-transparent.png", html_icon_transparent, 2400, 2400, True),
    
    # 2. Arabic Text Only (صَيّاف للتكييف - No English)
    ("sayyafac-arabic-only-dark.png", html_arabic_dark, 2400, 2400, False),
    ("sayyafac-arabic-only-light.png", html_arabic_light, 2400, 2400, False),
    ("sayyafac-arabic-only-transparent.png", html_arabic_transparent, 2400, 2400, True),
    ("sayyafac-arabic-horizontal-light.png", html_arabic_horizontal_light, 3000, 1000, False),
    ("sayyafac-arabic-horizontal-dark.png", html_arabic_horizontal_dark, 3000, 1000, False),
]

print("Launching Playwright for Ultra High-Res Logos (2400x2400 & 3000x1000)...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    for filename, html_content, w, h, omit_bg in tasks:
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        page.set_content(html_content)
        page.wait_for_timeout(350)
        
        # Save to social-assets
        path1 = os.path.join(output_dir, filename)
        page.screenshot(path=path1, omit_background=omit_bg)
        
        # Save to website assets
        path2 = os.path.join(website_img_dir, filename)
        page.screenshot(path=path2, omit_background=omit_bg)
        
        # Save to brain artifacts directory
        path3 = os.path.join(brain_dir, filename)
        page.screenshot(path=path3, omit_background=omit_bg)
        
        print(f"Generated {filename} ({w}x{h})")
        page.close()
        
    browser.close()

# Also write pure standalone vector SVG files for infinite scalability!
svg_icon_only = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="emblemGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#13528c"/>
      <stop offset="100%" stop-color="#08294a"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="25" stdDeviation="40" flood-color="#000000" flood-opacity="0.4"/>
      <feDropShadow dx="0" dy="0" stdDeviation="50" flood-color="#38bdf8" flood-opacity="0.3"/>
    </filter>
  </defs>
  <rect x="125" y="125" width="750" height="750" rx="200" fill="url(#emblemGrad)" stroke="#38bdf8" stroke-width="10" filter="url(#shadow)"/>
  <g transform="translate(250, 250) scale(5)">
    <circle cx="50" cy="50" r="33" fill="#38bdf8" opacity="0.12"/>
    <line x1="50" y1="12" x2="50" y2="88" stroke="#38bdf8" stroke-width="5.5" stroke-linecap="round"/>
    <line x1="12" y1="50" x2="88" y2="50" stroke="#38bdf8" stroke-width="5.5" stroke-linecap="round"/>
    <line x1="23" y1="23" x2="77" y2="77" stroke="#38bdf8" stroke-width="5.5" stroke-linecap="round"/>
    <line x1="77" y1="23" x2="23" y2="77" stroke="#38bdf8" stroke-width="5.5" stroke-linecap="round"/>
    <path d="M43 20L50 12L57 20" stroke="#ffffff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M43 30L50 23L57 30" stroke="#38bdf8" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M43 80L50 88L57 80" stroke="#ffffff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M43 70L50 77L57 70" stroke="#38bdf8" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M20 43L12 50L20 57" stroke="#ffffff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M30 43L23 50L30 57" stroke="#38bdf8" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M80 43L88 50L80 57" stroke="#ffffff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M70 43L77 50L70 57" stroke="#38bdf8" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="23" cy="23" r="3.5" fill="#ffffff"/>
    <circle cx="77" cy="23" r="3.5" fill="#ffffff"/>
    <circle cx="23" cy="77" r="3.5" fill="#ffffff"/>
    <circle cx="77" cy="77" r="3.5" fill="#ffffff"/>
    <circle cx="50" cy="50" r="10.5" fill="#ffffff"/>
    <circle cx="50" cy="50" r="5.2" fill="#38bdf8"/>
  </g>
</svg>
"""

with open(os.path.join(output_dir, "sayyafac-icon-only.svg"), "w", encoding="utf-8") as f:
    f.write(svg_icon_only)
with open(os.path.join(website_img_dir, "sayyafac-icon-only.svg"), "w", encoding="utf-8") as f:
    f.write(svg_icon_only)
with open(os.path.join(brain_dir, "sayyafac-icon-only.svg"), "w", encoding="utf-8") as f:
    f.write(svg_icon_only)

print("All Ultra High-Res Logos rendered and SVGs saved successfully!")
