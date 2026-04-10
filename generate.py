"""
Generate landing pages for all 10 I am The Coach sports apps.
Crops mockup images to phone-screen-only and builds HTML pages.
"""
from PIL import Image
import os, shutil

SPORTS = [
    {
        "key": "soccer",
        "name": "Soccer",
        "folder": "Soccer",
        "package": "com.coachboard.coachboard",
        "sport_label": "Soccer",
        "tagline": "The ultimate soccer coaching tool.\nFormations, tactics, live tracking & analytics.",
        "formations": "36+",
        "radar": "PAC, SHO, PAS, DRI, DEF, PHY",
        "uniforms": "EPL, La Liga, Bundesliga, Serie A presets",
        "field": "pitch",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "goals, assists, cards, substitutions",
        "accent": "#22c55e",
        "accent_light": "#dcfce7",
        "gradient_start": "#f0fdf4",
    },
    {
        "key": "basketball",
        "name": "Basketball",
        "folder": "Basketball",
        "package": "com.coachboard.basketball",
        "sport_label": "Basketball",
        "tagline": "The ultimate basketball coaching tool.\nLineups, plays, live tracking & analytics.",
        "formations": "32+",
        "radar": "SHT, PLY, ATH, DEF, REB, STR",
        "uniforms": "NBA, National presets",
        "field": "court",
        "privacy": "https://gggk720.github.io/coachboard-basketball-privacy.html",
        "match_events": "points, assists, rebounds, fouls",
        "accent": "#f97316",
        "accent_light": "#ffedd5",
        "gradient_start": "#fff7ed",
    },
    {
        "key": "baseball",
        "name": "Baseball",
        "folder": "Baseball",
        "package": "com.coachboard.baseball",
        "sport_label": "Baseball",
        "tagline": "The ultimate baseball coaching tool.\nDefense, batting order & game analytics.",
        "formations": "6+",
        "radar": "CON, POW, SPD, FLD, EYE, ARM",
        "uniforms": "MLB, National presets",
        "field": "diamond",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "runs, hits, errors, substitutions",
        "accent": "#ef4444",
        "accent_light": "#fee2e2",
        "gradient_start": "#fef2f2",
    },
    {
        "key": "cricket",
        "name": "Cricket",
        "folder": "Cricket",
        "package": "com.coachboard.cricket",
        "sport_label": "Cricket",
        "tagline": "The ultimate cricket coaching tool.\nFielding, batting order & match analytics.",
        "formations": "26+",
        "radar": "BAT, BWL, FLD, PWR, CST, TEC",
        "uniforms": "IPL, BBL, PSL, CPL, The Hundred presets",
        "field": "ground",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "runs, wickets, overs, extras",
        "accent": "#14b8a6",
        "accent_light": "#ccfbf1",
        "gradient_start": "#f0fdfa",
    },
    {
        "key": "hockey",
        "name": "Hockey",
        "folder": "Hockey",
        "package": "com.coachboard.hockey",
        "sport_label": "Ice Hockey",
        "tagline": "The ultimate ice hockey coaching tool.\nLineups, tactics, live tracking & analytics.",
        "formations": "13+",
        "radar": "SKT, SHT, PAS, CHK, DEF, STR",
        "uniforms": "NHL, National presets",
        "field": "ice rink",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "goals, assists, penalties, power plays",
        "accent": "#6366f1",
        "accent_light": "#e0e7ff",
        "gradient_start": "#eef2ff",
    },
    {
        "key": "volleyball",
        "name": "Volleyball",
        "folder": "Volleyball",
        "package": "com.coachboard.volleyball",
        "sport_label": "Volleyball",
        "tagline": "The ultimate volleyball coaching tool.\nRotations, tactics, live tracking & analytics.",
        "formations": "13+",
        "radar": "ATK, SRV, BLK, DIG, SET, RCV",
        "uniforms": "V-League, Serie A, Europe presets",
        "field": "court",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "kills, aces, blocks, digs",
        "accent": "#eab308",
        "accent_light": "#fef9c3",
        "gradient_start": "#fefce8",
    },
    {
        "key": "handball",
        "name": "Handball",
        "folder": "Handball",
        "package": "com.coachboard.handball",
        "sport_label": "Handball",
        "tagline": "The ultimate handball coaching tool.\nFormations, tactics, live tracking & analytics.",
        "formations": "38+",
        "radar": "SPD, SHT, PAS, STR, DEF, AGI",
        "uniforms": "EHF, National presets",
        "field": "court",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "goals, assists, saves, suspensions",
        "accent": "#f43f5e",
        "accent_light": "#ffe4e6",
        "gradient_start": "#fff1f2",
    },
    {
        "key": "lacrosse",
        "name": "Lacrosse",
        "folder": "Lacrosse",
        "package": "com.coachboard.lacrosse",
        "sport_label": "Lacrosse",
        "tagline": "The ultimate lacrosse coaching tool.\nFormations, tactics, live tracking & analytics.",
        "formations": "32+",
        "radar": "SPD, SHT, PAS, STK, DEF, IQ",
        "uniforms": "PLL, League presets",
        "field": "field",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "goals, assists, ground balls, saves",
        "accent": "#8b5cf6",
        "accent_light": "#ede9fe",
        "gradient_start": "#f5f3ff",
    },
    {
        "key": "rugby",
        "name": "Rugby",
        "folder": "Rugby",
        "package": "com.coachboard.rugby",
        "sport_label": "Rugby",
        "tagline": "The ultimate rugby coaching tool.\nFormations, tactics, live tracking & analytics.",
        "formations": "32+",
        "radar": "SPD, PAS, KIC, EVA, TAC, VIS",
        "uniforms": "League, National presets",
        "field": "pitch",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "tries, conversions, penalties, scrums",
        "accent": "#059669",
        "accent_light": "#d1fae5",
        "gradient_start": "#ecfdf5",
    },
    {
        "key": "football",
        "name": "Football",
        "folder": "Football",
        "package": "com.coachboard.football",
        "sport_label": "American Football",
        "tagline": "The ultimate football coaching tool.\nOffense, defense, special teams & analytics.",
        "formations": "53+",
        "radar": "SPD, STR, AGI, ARM, AWR, TGH",
        "uniforms": "NFL, National presets",
        "field": "gridiron",
        "privacy": "https://gggk720.github.io/coachboard-privacy/",
        "match_events": "touchdowns, field goals, turnovers, sacks",
        "accent": "#b45309",
        "accent_light": "#fef3c7",
        "gradient_start": "#fffbeb",
    },
]

MOCKUP_BASE = r"C:\Users\SMART\Desktop\App Mockups"
LANDING_BASE = r"C:\Users\SMART\coachboard-landing"

MOCKUP_FILES = [
    ("1_home.jpg", "Home"),
    ("3_lineup.jpg", "Lineup"),
    ("5_match.jpg", "Match"),
    ("7_player.jpg", "Player"),
    ("4_matchday.jpg", "Matchday"),
    ("8_uniform.jpg", "Uniform"),
    ("8_season.jpg", "Season"),
]

# Crop phone screen from mockup image
# The mockups are 1080x1920 with title at top ~200px, phone frame below
# We want just the phone screen area
def crop_screen(img_path, out_path):
    img = Image.open(img_path)
    w, h = img.size
    # Title takes roughly top 12%, phone frame starts after
    # Phone screen is roughly center 75% width, from 15% to 92% height
    # Adjust based on actual mockup structure
    top = int(h * 0.115)  # skip title text
    bottom = h  # keep to bottom
    left = 0
    right = w
    cropped = img.crop((left, top, right, bottom))
    cropped.save(out_path, quality=90)

def generate_html(sport):
    others = [s for s in SPORTS if s["key"] != sport["key"]]

    other_icons_html = ""
    for s in others:
        other_icons_html += f'''      <a class="sport-item" href="../{s["key"]}/">
        <img src="../{s["key"]}/assets/app_icon.png" alt="{s["name"]}">
        <span>{s["name"]}</span>
      </a>\n'''

    # Soccer and Basketball have season screenshot instead of uniform
    has_uniform = sport["key"] not in ("soccer", "basketball")
    last_feature = {
        "img": "screen_8_uniform.jpg" if has_uniform else "screen_8_season.jpg",
        "title": "Custom Uniforms" if has_uniform else "Season Analytics",
        "desc": (f'{sport["uniforms"]}. Solid, V-Stripes, H-Stripe, Sash patterns and more.'
                 if has_uniform else
                 "Win rate, form tracking, player rankings and visual charts across your entire season."),
    }

    features = [
        {
            "img": "screen_3_lineup.jpg",
            "title": "Lineup Builder",
            "desc": f'Drag-and-drop players onto a realistic {sport["field"]}. Choose from {sport["formations"]} formations.',
        },
        {
            "img": "screen_4_matchday.jpg",
            "title": "Tactical Board",
            "desc": "Draw plays with arrows, lines, and curves. Visualize strategies with an intuitive whiteboard.",
        },
        {
            "img": "screen_5_match.jpg",
            "title": "Live Match Tracking",
            "desc": f'Record {sport["match_events"]} in real-time. Switch formations mid-game.',
        },
        {
            "img": "screen_7_player.jpg",
            "title": "Player Ratings",
            "desc": f'Radar charts with {sport["radar"]} ratings. Track performance across matches.',
        },
        {
            "img": "screen_1_home.jpg",
            "title": "Team Management",
            "desc": "Manage multiple teams, track season stats, and plan matches with a built-in calendar.",
        },
        last_feature,
    ]

    features_html = ""
    for f in features:
        features_html += f'''      <div class="feature-card">
        <div class="phone-frame">
          <div class="phone-notch"></div>
          <img src="assets/{f["img"]}" alt="{f["title"]}" loading="lazy">
        </div>
        <h3>{f["title"]}</h3>
        <p>{f["desc"]}</p>
      </div>\n'''

    tagline_lines = sport["tagline"].split("\n")
    tagline_html = f"{tagline_lines[0]}<br>{tagline_lines[1]}"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{sport["name"]} - I am The Coach</title>
  <meta name="description" content="{sport["sport_label"]} lineup builder & team manager">
  <link rel="icon" type="image/png" href="assets/app_icon.png">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: #ffffff;
      color: #1a1a2e;
      overflow-x: hidden;
    }}

    /* Nav */
    nav {{
      position: fixed;
      top: 0;
      width: 100%;
      z-index: 100;
      background: rgba(255,255,255,0.92);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(0,0,0,0.06);
      padding: 14px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: #1a1a2e;
    }}

    .nav-brand img {{ width: 36px; height: 36px; border-radius: 10px; }}
    .nav-brand span {{ font-weight: 700; font-size: 1.05rem; }}

    .nav-cta {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: {sport["accent"]};
      color: #fff;
      text-decoration: none;
      padding: 10px 22px;
      border-radius: 50px;
      font-size: 0.9rem;
      font-weight: 600;
      transition: opacity 0.2s;
    }}

    .nav-cta:hover {{ opacity: 0.9; }}

    /* Hero */
    .hero {{
      padding: 140px 24px 80px;
      text-align: center;
      background: linear-gradient(180deg, {sport["gradient_start"]} 0%, #ffffff 100%);
    }}

    .hero-icon {{
      width: 100px;
      height: 100px;
      border-radius: 24px;
      box-shadow: 0 12px 40px rgba(0,0,0,0.1);
      margin-bottom: 28px;
    }}

    .hero h1 {{
      font-size: 3rem;
      font-weight: 800;
      letter-spacing: -1.5px;
      color: #1a1a2e;
      margin-bottom: 8px;
      line-height: 1.1;
    }}

    .sport-badge {{
      display: inline-block;
      background: {sport["accent"]};
      color: #fff;
      padding: 6px 20px;
      border-radius: 50px;
      font-size: 0.95rem;
      font-weight: 600;
      margin-bottom: 20px;
    }}

    .hero p {{
      font-size: 1.15rem;
      color: #64748b;
      max-width: 480px;
      margin: 0 auto 36px;
      line-height: 1.7;
    }}

    .hero-cta {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: #1a1a2e;
      color: #fff;
      text-decoration: none;
      padding: 16px 36px;
      border-radius: 50px;
      font-size: 1.05rem;
      font-weight: 600;
      transition: transform 0.2s, box-shadow 0.2s;
      box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }}

    .hero-cta:hover {{
      transform: translateY(-2px);
      box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }}

    .hero-cta svg {{ width: 22px; height: 22px; }}

    .trust {{
      display: flex;
      justify-content: center;
      gap: 40px;
      padding: 40px 24px 0;
      flex-wrap: wrap;
    }}

    .trust-item {{ text-align: center; }}
    .trust-item .num {{ font-size: 1.5rem; font-weight: 800; color: {sport["accent"]}; }}
    .trust-item .label {{ font-size: 0.8rem; color: #94a3b8; margin-top: 2px; }}

    /* Features */
    .features {{
      padding: 80px 24px;
      background: #fafafe;
    }}

    .features h2 {{
      text-align: center;
      font-size: 2.2rem;
      font-weight: 700;
      margin-bottom: 16px;
      color: #1a1a2e;
    }}

    .features .desc {{
      text-align: center;
      color: #64748b;
      font-size: 1.05rem;
      margin-bottom: 48px;
    }}

    .features-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 28px;
      max-width: 1060px;
      margin: 0 auto;
    }}

    .feature-card {{
      background: #fff;
      border: 1px solid #f0f0f5;
      border-radius: 20px;
      padding: 32px 24px 24px;
      text-align: center;
      transition: transform 0.2s, box-shadow 0.2s;
    }}

    .feature-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 12px 40px rgba(0,0,0,0.06);
    }}

    /* Phone frame */
    .phone-frame {{
      width: 200px;
      margin: 0 auto 20px;
      background: #1a1a2e;
      border-radius: 28px;
      padding: 8px;
      position: relative;
      box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }}

    .phone-notch {{
      width: 60px;
      height: 6px;
      background: #333;
      border-radius: 3px;
      margin: 4px auto 6px;
    }}

    .phone-frame img {{
      width: 100%;
      border-radius: 20px;
      display: block;
    }}

    .feature-card h3 {{
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 8px;
      color: #1a1a2e;
    }}

    .feature-card p {{
      font-size: 0.9rem;
      color: #64748b;
      line-height: 1.6;
    }}

    /* Also Available */
    .also-available {{
      padding: 80px 24px;
      text-align: center;
    }}

    .also-available h2 {{
      font-size: 1.8rem;
      font-weight: 700;
      margin-bottom: 12px;
      color: #1a1a2e;
    }}

    .also-available .desc {{
      color: #94a3b8;
      font-size: 1rem;
      margin-bottom: 40px;
    }}

    .sports-grid {{
      display: flex;
      justify-content: center;
      gap: 28px;
      flex-wrap: wrap;
      max-width: 900px;
      margin: 0 auto;
    }}

    .sport-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      transition: transform 0.2s;
    }}

    .sport-item:hover {{ transform: translateY(-4px); }}
    .sport-item img {{ width: 64px; height: 64px; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
    .sport-item span {{ font-size: 0.8rem; font-weight: 600; color: #64748b; }}

    /* CTA Bottom */
    .cta-bottom {{
      padding: 80px 24px;
      text-align: center;
      background: linear-gradient(180deg, #ffffff 0%, {sport["gradient_start"]} 100%);
    }}

    .cta-bottom h2 {{ font-size: 2.2rem; font-weight: 700; margin-bottom: 16px; color: #1a1a2e; }}
    .cta-bottom p {{ color: #64748b; font-size: 1.05rem; margin-bottom: 32px; }}

    footer {{
      text-align: center;
      padding: 32px 24px;
      border-top: 1px solid #f0f0f5;
    }}

    footer a {{ color: {sport["accent"]}; text-decoration: none; font-size: 0.9rem; }}
    footer p {{ color: #94a3b8; font-size: 0.8rem; margin-top: 8px; }}

    @media (max-width: 640px) {{
      .hero h1 {{ font-size: 2rem; }}
      .hero p {{ font-size: 1rem; }}
      .features h2 {{ font-size: 1.6rem; }}
      .phone-frame {{ width: 160px; }}
      .trust {{ gap: 24px; }}
      .sports-grid {{ gap: 16px; }}
      .sport-item img {{ width: 52px; height: 52px; border-radius: 14px; }}
    }}
  </style>
</head>
<body>

  <nav>
    <a href="#" class="nav-brand">
      <img src="assets/app_icon.png" alt="Icon">
      <span>I am The Coach</span>
    </a>
    <a href="https://play.google.com/store/apps/details?id={sport["package"]}" class="nav-cta">
      <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M3.609 1.814L13.792 12 3.61 22.186a2.37 2.37 0 0 1-.497-.544 2.37 2.37 0 0 1-.363-1.273V3.631c0-.463.13-.906.363-1.273.14-.222.306-.4.497-.544zm.86-.508L15.28 7.12l-2.89 2.89L4.468 1.306zm0 21.388l7.923-7.923-2.89-2.89L4.468 22.694zM16.6 7.78l3.394 1.97c.962.558.962 1.942 0 2.5L16.6 14.22 13.502 12 16.6 7.78z"/></svg>
      Download
    </a>
  </nav>

  <section class="hero">
    <img src="assets/app_icon.png" alt="I am The Coach - {sport["name"]}" class="hero-icon">
    <h1>I am The Coach</h1>
    <div class="sport-badge">{sport["sport_label"]}</div>
    <p>{tagline_html}</p>
    <a href="https://play.google.com/store/apps/details?id={sport["package"]}" class="hero-cta">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.609 1.814L13.792 12 3.61 22.186a2.37 2.37 0 0 1-.497-.544 2.37 2.37 0 0 1-.363-1.273V3.631c0-.463.13-.906.363-1.273.14-.222.306-.4.497-.544zm.86-.508L15.28 7.12l-2.89 2.89L4.468 1.306zm0 21.388l7.923-7.923-2.89-2.89L4.468 22.694zM16.6 7.78l3.394 1.97c.962.558.962 1.942 0 2.5L16.6 14.22 13.502 12 16.6 7.78z"/></svg>
      Get it on Google Play
    </a>
    <div class="trust">
      <div class="trust-item"><div class="num">100%</div><div class="label">Free to Use</div></div>
      <div class="trust-item"><div class="num">{sport["formations"]}</div><div class="label">Formations</div></div>
      <div class="trust-item"><div class="num">0</div><div class="label">Login Required</div></div>
    </div>
  </section>

  <section class="features">
    <h2>Everything a Coach Needs</h2>
    <p class="desc">Powerful tools designed for real coaching</p>
    <div class="features-grid">
{features_html}    </div>
  </section>

  <section class="also-available">
    <h2>Also Available</h2>
    <p class="desc">I am The Coach is available for 10 sports</p>
    <div class="sports-grid">
{other_icons_html}    </div>
  </section>

  <section class="cta-bottom">
    <h2>Ready to Coach?</h2>
    <p>Download now and take your team to the next level.</p>
    <a href="https://play.google.com/store/apps/details?id={sport["package"]}" class="hero-cta">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.609 1.814L13.792 12 3.61 22.186a2.37 2.37 0 0 1-.497-.544 2.37 2.37 0 0 1-.363-1.273V3.631c0-.463.13-.906.363-1.273.14-.222.306-.4.497-.544zm.86-.508L15.28 7.12l-2.89 2.89L4.468 1.306zm0 21.388l7.923-7.923-2.89-2.89L4.468 22.694zM16.6 7.78l3.394 1.97c.962.558.962 1.942 0 2.5L16.6 14.22 13.502 12 16.6 7.78z"/></svg>
      Get it on Google Play
    </a>
  </section>

  <footer>
    <a href="{sport["privacy"]}">Privacy Policy</a>
    <p>&copy; 2026 I am The Coach. All rights reserved.</p>
  </footer>

</body>
</html>'''


def main():
    for sport in SPORTS:
        key = sport["key"]
        folder = sport["folder"]
        out_dir = os.path.join(LANDING_BASE, key, "assets")
        os.makedirs(out_dir, exist_ok=True)

        src_dir = os.path.join(MOCKUP_BASE, folder)

        # Copy app icon
        shutil.copy2(
            os.path.join(src_dir, "app_icon.png"),
            os.path.join(out_dir, "app_icon.png"),
        )

        # Crop mockup screens
        for filename, label in MOCKUP_FILES:
            src = os.path.join(src_dir, filename)
            dst = os.path.join(out_dir, f"screen_{filename}")
            if os.path.exists(src):
                crop_screen(src, dst)
                print(f"  Cropped {filename} -> screen_{filename}")
            else:
                print(f"  MISSING {src}")

        # Write HTML
        html = generate_html(sport)
        html_path = os.path.join(LANDING_BASE, key, "index.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"[OK] {key}/index.html")

    print(f"\nDone! Generated {len(SPORTS)} landing pages.")


if __name__ == "__main__":
    main()
