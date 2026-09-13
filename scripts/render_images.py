"""Render the article's memes and Pat's Slack-style messages to PNG with headless Chrome.

Every image is an original HTML/CSS illustration (emoji, shapes and text), so the
repo ships no third-party meme templates.

    uv run python scripts/render_images.py            # render everything
    uv run python scripts/render_images.py s_drake    # render some images

Set CHROME=/path/to/chrome if Chrome isn't in the default macOS location.
"""

import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: WIDTHpx; height: HEIGHTpx; overflow: hidden; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; }
code { font-family: Menlo, "SF Mono", Consolas, monospace; }
.impact {
  font-family: Impact, "Anton", "Arial Black", sans-serif; color: #fff; text-transform: uppercase;
  -webkit-text-stroke: 3px #000; paint-order: stroke fill; letter-spacing: 0.01em;
}
"""


def e(text):
    return html.escape(text)


# ------------------------------------------------------------------------------------------ memes

def iceberg():
    layers = [
        ("new SMS vendor (already signed 🙃)", 560, "rgba(10, 60, 110, 0.55)"),
        ("compliance: the audit log is append-only", 745, "rgba(8, 45, 90, 0.65)"),
        ("AI-powered by Friday ✨", 930, "rgba(6, 32, 70, 0.75)"),
        ("enterprise demo tomorrow", 1115, "rgba(4, 20, 50, 0.85)"),
        ("“actually, can we go back to email?”", 1275, "rgba(0, 0, 0, 0.9)"),
    ]
    labels = "".join(
        f'<div class="layer" style="top:{top}px;background:{bg}">{e(text)}</div>' for text, top, bg in layers
    )
    return 1080, 1350, """
.sky { position:absolute; inset:0 0 auto 0; height:400px; background:linear-gradient(#bfe6ff,#e9f7ff); }
.sea { position:absolute; inset:400px 0 0 0; background:linear-gradient(#2a8fd6,#0b3f78 45%,#03152e); }
svg { position:absolute; inset:0; }
.tip-label { position:absolute; top:70px; left:0; right:0; text-align:center; font-weight:800; font-size:50px; color:#0b2540; }
.tip-label small { display:block; font-weight:500; font-size:30px; color:#3c5d7a; margin-top:6px; }
.layer { position:absolute; left:50%; transform:translateX(-50%); color:#fff; font-weight:700; font-size:36px;
  padding:14px 28px; border-radius:40px; white-space:nowrap; box-shadow:0 0 0 2px rgba(255,255,255,0.18); }
.boat { position:absolute; top:318px; left:120px; font-size:84px; }
""", f"""
<div class="sky"></div><div class="sea"></div>
<svg viewBox="0 0 1080 1350" width="1080" height="1350">
  <polygon points="440,402 520,250 560,280 640,402" fill="#ffffff"/>
  <polygon points="440,402 520,250 540,300 470,402" fill="#dff3ff"/>
  <polygon points="440,402 640,402 860,620 990,980 820,1350 260,1350 70,1020 200,640" fill="rgba(200,238,255,0.28)"/>
  <polygon points="440,402 640,402 700,520 560,1350 260,1350 70,1020 200,640" fill="rgba(255,255,255,0.10)"/>
</svg>
<div class="tip-label">Pat: “it's a small change”<small>what's above the water</small></div>
<div class="boat">🛶</div>
{labels}
"""


def drake():
    return 1080, 1080, """
.grid { display:grid; grid-template-columns: 460px 620px; grid-template-rows: 540px 540px; height:1080px; }
.pic { position:relative; background:#f2b84b; border-bottom:4px solid #fff; overflow:hidden; }
.pic.yes { background:#f5c86a; border-bottom:0; }
.face { position:absolute; font-size:230px; left:70px; top:120px; }
.hand { position:absolute; font-size:170px; }
.no .hand { left:250px; top:210px; transform:rotate(-12deg); }
.yes .hand { left:250px; top:230px; }
.txt { background:#fff; display:flex; align-items:center; padding:0 56px; font-size:56px; font-weight:700; line-height:1.18; color:#111; border-bottom:4px solid #eee; }
.txt code { font-size:48px; background:#eef2f7; padding:2px 10px; border-radius:8px; }
""", """
<div class="grid">
  <div class="pic no"><div class="face">😣</div><div class="hand">✋</div></div>
  <div class="txt"><span>Emailing the whole company to test one template</span></div>
  <div class="pic yes"><div class="face">😏</div><div class="hand">👉</div></div>
  <div class="txt"><span>Testing <code>EmailChannel_v1</code> on its own</span></div>
</div>
"""


def expanding_brain():
    rows = [
        ("Email", "background:#1e1e1e", "font-size:110px;filter:grayscale(0.7) brightness(0.65)"),
        ("SMS", "background:#2a2a2e", "font-size:130px"),
        ("Push notifications", "background:radial-gradient(circle,#3a6ea8 0%,#1c2f4a 70%)", "font-size:150px;filter:drop-shadow(0 0 18px #7fc4ff)"),
        ("Slack", "background:radial-gradient(circle,#8fe3ff 0%,#5b3fd1 55%,#1b1140 100%)", "font-size:170px;filter:drop-shadow(0 0 30px #d6f4ff)"),
        ("Zero edits to <code>Notifier_v4</code>",
         "background:repeating-conic-gradient(from 0deg,rgba(255,255,255,0.35) 0deg 6deg,transparent 6deg 18deg),radial-gradient(circle,#ffffff 0%,#ffe27a 22%,#ff6ad5 50%,#3b0a7a 100%)",
         "font-size:190px;filter:drop-shadow(0 0 40px #fff)"),
    ]
    cells = "".join(
        f'<div class="txt"><span>{text}</span></div><div class="pic" style="{bg}"><span style="{brain}">🧠</span>{"<i>✨</i>" if i >= 3 else ""}</div>'
        for i, (text, bg, brain) in enumerate(rows)
    )
    return 1080, 1500, """
.grid { display:grid; grid-template-columns: 560px 520px; grid-auto-rows: 300px; }
.txt { background:#fff; display:flex; align-items:center; padding:0 48px; font-size:58px; font-weight:700; color:#111; border-bottom:3px solid #ddd; line-height:1.15; }
.txt code { font-size:46px; background:#eef2f7; padding:2px 10px; border-radius:8px; }
.pic { position:relative; display:flex; align-items:center; justify-content:center; border-bottom:3px solid #000; overflow:hidden; }
.pic i { position:absolute; top:24px; right:40px; font-size:70px; font-style:normal; }
""", f'<div class="grid">{cells}</div>'


def this_is_fine():
    flames = "".join(
        f'<span class="flame" style="left:{x}px;top:{y}px;font-size:{s}px">🔥</span>'
        for x, y, s in [
            (-30, 820, 230), (150, 870, 190), (330, 900, 170), (560, 880, 200), (760, 850, 220), (900, 800, 240),
            (-40, 560, 200), (930, 540, 210), (-20, 330, 150), (960, 300, 160), (120, 690, 120), (820, 680, 130),
        ]
    )
    return 1080, 1080, """
body { background:linear-gradient(#4a4a4a 0%,#8a3b12 35%,#e3661b 70%,#ffb03b 100%); position:relative; }
.caption { position:absolute; top:34px; left:0; right:0; text-align:center; font-size:84px; }
.terminal { position:absolute; top:170px; left:90px; right:90px; background:#0f1115; border-radius:16px; padding:22px 28px 26px;
  box-shadow:0 12px 40px rgba(0,0,0,0.5); }
.terminal .dots { color:#555; font-size:26px; letter-spacing:6px; margin-bottom:10px; }
.terminal code { color:#ff7b72; font-size:31px; line-height:1.4; white-space:pre-wrap; }
.flame { position:absolute; }
.desk { position:absolute; left:240px; right:240px; top:800px; height:40px; background:#6b3f1d; border-radius:6px; }
.dev { position:absolute; left:380px; top:520px; font-size:280px; }
.coffee { position:absolute; left:660px; top:690px; font-size:110px; }
.bubble { position:absolute; left:640px; top:430px; background:#fff; border-radius:40px; padding:22px 34px;
  font-family:"Chalkboard SE", "Comic Sans MS", cursive; font-size:52px; font-weight:700; color:#111; }
.bubble:after { content:""; position:absolute; left:40px; bottom:-34px; border:22px solid transparent; border-top:34px solid #fff; }
""", f"""
<div class="caption impact">Monday, 9:01am</div>
<div class="terminal"><div class="dots">● ● ●</div><code>AttributeError: 'TextBlasterSmsChannel_v1'
object has no attribute 'connect'</code></div>
{flames}
<div class="dev">🧑‍💻</div>
<div class="desk"></div>
<div class="coffee">☕</div>
<div class="bubble">This is fine.</div>
"""


def two_buttons():
    return 1080, 1350, """
.top { position:absolute; inset:0 0 auto 0; height:800px; background:linear-gradient(#cfe3f7,#a9c8e8); }
.panel { position:absolute; left:110px; right:110px; top:300px; height:380px; background:linear-gradient(#b9bec6,#8d939c); border-radius:30px; box-shadow:inset 0 -12px 0 rgba(0,0,0,0.15); }
.btn { position:absolute; top:130px; width:250px; height:250px; border-radius:50%;
  background:radial-gradient(circle at 38% 32%,#ff9a9a 0%,#e0202c 45%,#8a0d14 100%); box-shadow:0 18px 0 #5a070c; }
.btn.a { left:110px; } .btn.b { right:110px; }
.label { position:absolute; top:60px; width:400px; background:#fffdf2; border:3px solid #222; padding:18px 20px; transform:rotate(-4deg);
  font-size:44px; font-weight:800; line-height:1.12; text-align:center; color:#111; }
.label.a { left:60px; } .label.b { right:60px; transform:rotate(4deg); }
.hand { position:absolute; top:520px; left:470px; font-size:150px; transform:rotate(8deg); }
.bottom { position:absolute; inset:800px 0 0 0; background:#f1e2c6; display:flex; align-items:center; justify-content:center; gap:40px; }
.face { font-size:300px; position:relative; }
.drop { position:absolute; font-size:90px; top:10px; right:-40px; }
.who { font-size:62px; font-weight:800; color:#111; max-width:420px; line-height:1.1; }
""", """
<div class="top"></div>
<div class="label a">Keep the compliance contract</div>
<div class="label b">Ship AI by Friday</div>
<div class="panel"><div class="btn a"></div><div class="btn b"></div></div>
<div class="hand">👆</div>
<div class="bottom"><div class="face">😰<span class="drop">💦</span></div><div class="who">Me, Thursday night</div></div>
"""


def same_picture():
    frame = lambda label: f'<div class="frame"><div class="canvas"><code>[]</code></div><div class="plate"><code>{e(label)}</code></div></div>'
    return 1080, 1350, """
body { background:#e9dcc3; }
.wall { position:absolute; inset:0; background:linear-gradient(#efe4cf,#dccbad); }
.line1 { position:absolute; top:44px; left:60px; right:60px; font-size:46px; font-weight:700; line-height:1.2; color:#2b2218; text-align:center; }
.frames { position:absolute; top:220px; left:60px; right:60px; display:flex; gap:40px; }
.frame { flex:1; background:#fff; border:14px solid #5b3b1e; box-shadow:0 12px 30px rgba(0,0,0,0.25); }
.canvas { height:330px; display:flex; align-items:center; justify-content:center; background:#fafafa; }
.canvas code { font-size:150px; color:#222; }
.plate { background:#1d1f24; padding:16px; text-align:center; }
.plate code { color:#e7e9ef; font-size:24px; line-height:1.35; }
.person { position:absolute; top:690px; left:0; right:0; text-align:center; font-size:140px; }
.divider { position:absolute; top:850px; left:0; right:0; height:8px; background:#fff; }
.bottom { position:absolute; top:858px; left:0; right:0; bottom:0; display:flex; align-items:center; justify-content:center; gap:40px; }
.bottom .face { font-size:260px; }
.bottom .say { font-size:66px; font-weight:800; color:#2b2218; max-width:520px; line-height:1.1; }
""", f"""
<div class="wall"></div>
<div class="line1">Compliance needs you to find the differences between this picture and this picture.</div>
<div class="frames">{frame("legacy plan's get_audit_log()")}{frame("get_audit_log() with the audit log off")}</div>
<div class="person">🧑‍💼</div>
<div class="divider"></div>
<div class="bottom"><div class="face">😐</div><div class="say">They're the same picture.</div></div>
"""


def stonks():
    return 1080, 1080, """
body { background:radial-gradient(circle at 60% 40%,#1b3a73 0%,#0a1633 70%); position:relative; }
svg { position:absolute; inset:0; }
.top { position:absolute; top:40px; left:40px; right:40px; text-align:center; font-size:70px; line-height:1.05; }
.me { position:absolute; top:220px; left:60px; right:60px; text-align:center; color:#dfe8ff; font-size:40px; font-weight:600; }
.me code { background:rgba(255,255,255,0.12); padding:2px 12px; border-radius:8px; font-size:36px; }
.man { position:absolute; left:80px; bottom:170px; font-size:340px; }
.word { position:absolute; bottom:40px; right:70px; font-size:150px; }
""", """
<svg viewBox="0 0 1080 1080" width="1080" height="1080">
  <g stroke="rgba(255,255,255,0.08)" stroke-width="2">
    <line x1="0" y1="400" x2="1080" y2="400"/><line x1="0" y1="560" x2="1080" y2="560"/>
    <line x1="0" y1="720" x2="1080" y2="720"/><line x1="0" y1="880" x2="1080" y2="880"/>
    <line x1="300" y1="300" x2="300" y2="1080"/><line x1="540" y1="300" x2="540" y2="1080"/><line x1="780" y1="300" x2="780" y2="1080"/>
  </g>
  <polyline points="380,860 470,800 540,830 620,700 690,730 770,560 840,590 930,380" fill="none" stroke="#2bd46a" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/>
  <polygon points="990,300 900,340 960,420" fill="#2bd46a"/>
</svg>
<div class="top impact">Pat: “can we go back to email?”</div>
<div class="me">Me: <em>changes one line in</em> <code>wiring.py</code></div>
<div class="man">🕴️</div>
<div class="word impact">Stonks</div>
"""


# ---------------------------------------------------------------------------------- Pat on Slack

def chat(channel, messages):
    """messages: list of (author, time, text_html, reactions) or ("divider", label)."""
    avatars = {"Pat": ("P", "linear-gradient(135deg,#ff8a5b,#e0457b)", "Product"), "You": ("Y", "linear-gradient(135deg,#4f8cff,#6b3be0)", "Engineering")}
    rows, previous = [], None
    for message in messages:
        if message[0] == "divider":
            rows.append(f'<div class="divider"><span>{e(message[1])}</span></div>')
            previous = None
            continue
        author, time, text, reactions = message
        initial, gradient, team = avatars[author]
        reaction_html = "".join(f'<span class="reaction">{r}</span>' for r in reactions)
        if author == previous:
            rows.append(f'<div class="msg cont"><div class="gutter">{time}</div><div class="body"><div class="text">{text}</div>{"<div class=reactions>" + reaction_html + "</div>" if reactions else ""}</div></div>')
        else:
            rows.append(
                f'<div class="msg"><div class="avatar" style="background:{gradient}">{initial}</div><div class="body">'
                f'<div class="meta"><b>{author}</b><span class="team">{team}</span><span class="time">{time}</span></div>'
                f'<div class="text">{text}</div>{"<div class=reactions>" + reaction_html + "</div>" if reactions else ""}</div></div>'
            )
        previous = author
    return 1080, None, """
body { background:#ffffff; color:#1d1c1d; }
.header { height:92px; display:flex; align-items:center; padding:0 40px; border-bottom:2px solid #ececec; font-size:34px; font-weight:800; }
.header span { color:#8a8a8e; font-weight:400; margin-right:6px; }
.msg { display:flex; gap:24px; padding:26px 40px 10px; }
.msg.cont { padding-top:6px; }
.avatar { width:80px; height:80px; flex:none; border-radius:18px; color:#fff; font-size:42px; font-weight:800; display:flex; align-items:center; justify-content:center; }
.gutter { width:80px; flex:none; color:#a0a0a5; font-size:20px; text-align:right; padding-top:10px; }
.meta { display:flex; align-items:baseline; gap:14px; margin-bottom:6px; }
.meta b { font-size:32px; }
.team { font-size:20px; font-weight:700; color:#6d6d72; background:#f0f0f2; border-radius:8px; padding:3px 10px; }
.time { font-size:22px; color:#8a8a8e; }
.text { font-size:34px; line-height:1.42; max-width:880px; }
.text code { font-size:28px; background:#f6f6f8; border:1px solid #e3e3e6; border-radius:6px; padding:1px 8px; color:#c7254e; }
.reactions { display:flex; gap:10px; margin-top:12px; }
.reaction { font-size:24px; border:2px solid #e3e3e6; border-radius:30px; padding:4px 14px; background:#f8f8fa; }
.divider { margin:26px 40px 4px; border-top:2px solid #ececec; text-align:center; height:0; }
.divider span { position:relative; top:-20px; background:#fff; border:2px solid #ececec; border-radius:30px; padding:6px 22px; font-size:22px; font-weight:700; }
.diff { margin-top:14px; font-family:Menlo,monospace; font-size:22px; border:2px solid #e3e3e6; border-radius:10px; overflow:hidden; width:860px; white-space:pre; }
.diff div { padding:6px 16px; } .diff .file { background:#f6f6f8; color:#555; } .diff .del { background:#ffecec; color:#b31d28; } .diff .add { background:#e6ffed; color:#22863a; }
""", f'<div id="content" style="padding-bottom:28px"><div class="header"><span>#</span>{e(channel)}</div>{"".join(rows)}</div>'


SLACK = {
    "intro": lambda: chat("product-eng", [
        ("Pat", "9:02 AM", "Hey! 👋 super small thing, can we add notifications to the app? Should be quick 🙏", ["👀 1"]),
    ]),
    "s": lambda: chat("product-eng", [
        ("Pat", "3:12 PM", "QA says they can't test the new email template without spinning up the <i>entire</i> notifier 😅 can we fix by EOD?", ["😅 2"]),
    ]),
    "o": lambda: chat("product-eng", [
        ("Pat", "10:00 AM", "BIG NEWS 🚀 customers hate email. We're pivoting to SMS! That's a one-line change right??", ["🚀 4", "😐 1"]),
        ("Pat", "2:15 PM", "update: push notifications are the future", []),
        ("Pat", "4:30 PM", "update 2: every enterprise lives in Slack 🤯", ["🫠 3"]),
    ]),
    "d": lambda: chat("product-eng", [
        ("divider", "Friday"),
        ("Pat", "4:47 PM", "Finance found a cheaper SMS vendor 🎉 TextBlaster! Already signed the contract, we go live Monday 🙃", ["💀 5"]),
    ]),
    "l": lambda: chat("product-eng", [
        ("Pat", "11:00 AM", "The board asked about our AI strategy 👀 can notifications be AI-powered by Friday? Just make them ✨pop✨", ["✨ 6"]),
        ("divider", "Monday"),
        ("Pat", "9:14 AM", "Compliance is asking why the audit log is empty 😬 did something change??", ["😬 4"]),
    ]),
    "i": lambda: chat("product-eng", [
        ("Pat", "6:58 PM", "HUGE enterprise demo tomorrow 🤝 they want the legacy email plan, the compliance plan and the AI plan side by side. One campaign runner for all three, easy right?", ["🙏 2", "😰 3"]),
    ]),
    "outro": lambda: chat("product-eng", [
        ("Pat", "10:31 AM", "So… customers actually kind of liked email 😅 can we go back?", []),
        ("You", "10:32 AM", "sure 👍"
         '<div class="diff"><div class="file">notifications/wiring.py</div>'
         '<div class="del">-        channel=ChannelFactory.create_slack_channel_v1(),</div>'
         '<div class="add">+        channel=ChannelFactory.create_email_channel_v1(),</div></div>', ["🎉 7"]),
    ]),
}

MEMES = {
    "intro_iceberg": iceberg,
    "s_drake": drake,
    "o_expanding_brain": expanding_brain,
    "d_this_is_fine": this_is_fine,
    "l_two_buttons": two_buttons,
    "i_same_picture": same_picture,
    "outro_stonks": stonks,
}

IMAGES = {
    **{name: (ROOT / "images" / "memes" / f"{name}.png", build) for name, build in MEMES.items()},
    **{f"slack_{name}": (ROOT / "images" / "slack" / f"{name}.png", build) for name, build in SLACK.items()},
}


def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", *args],
                          check=True, capture_output=True, text=True)


def page_html(width, height, css, body, measure=False):
    size_css = BASE_CSS.replace("WIDTH", str(width)).replace("HEIGHT", str(height or 10000))
    script = ("<script>addEventListener('load',()=>document.body.setAttribute('data-height',"
              "Math.ceil(document.getElementById('content').getBoundingClientRect().bottom)))</script>") if measure else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{size_css}{css}</style></head>'
            f'<body style="position:relative">{body}{script}</body></html>')


def render(output, build):
    width, height, css, body = build()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        page_path = Path(tmp) / "page.html"
        if height is None:
            page_path.write_text(page_html(width, None, css, body, measure=True))
            dom = chrome("--virtual-time-budget=2000", "--dump-dom", page_path.as_uri()).stdout
            height = int(re.search(r'data-height="(\d+)"', dom).group(1))
        page_path.write_text(page_html(width, height, css, body))
        chrome("--force-device-scale-factor=2", f"--window-size={width},{height}", f"--screenshot={output}", page_path.as_uri())
    print(f"rendered {output.relative_to(ROOT)} ({width}x{height})")


def main():
    names = sys.argv[1:] or list(IMAGES)
    unknown = set(names) - set(IMAGES)
    if unknown:
        sys.exit(f"Unknown images: {', '.join(sorted(unknown))}. Choose from: {', '.join(IMAGES)}")
    for name in names:
        render(*IMAGES[name])


if __name__ == "__main__":
    main()
