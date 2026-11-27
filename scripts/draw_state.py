#!/usr/bin/env python3
"""Draws the current state of model v1 as an SVG block diagram.

    python3 scripts/draw_state.py        # writes analysis/model-state.svg

Standard library only. Every number in the picture is read from
output/series-v1.csv and output/events-v1.csv; the wording of the boxes is
fixed here. Friday's diagram (analysis/causal-diagram.png) is a record of
13 November and is not touched. Not part of the frozen model.
"""
import csv, os
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def table(name):
    with open(os.path.join(ROOT, "output", name), newline="") as f:
        f.readline()
        return list(csv.DictReader(f))


def pct(x):
    x = 100 * float(x)
    return f"{x:.2f}%" if x < 0.1 else f"{x:.1f}%" if x < 10 else f"{x:.0f}%"


last = table("series-v1.csv")[-1]
ev = {r["event_id"]: r for r in table("events-v1.csv")}
INK, GREY, LINE, BLUE, ORANGE = "#1a1a1a", "#5f5e5a", "#c9c8bf", "#2a78d6", "#e8622c"
out = []


def text(x, y, s, size=15, weight=400, fill=INK, anchor="middle"):
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
               f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')


def box(x, y, w, h, title, lines, stroke=LINE, fill="#fff", dash="", big=None, tsize=16):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="2"{d}/>')
    cy = y + 26
    text(x + w / 2, cy, title, tsize, 700)
    for ln in lines:
        cy += 19
        text(x + w / 2, cy, ln, 13, 400, GREY)
    if big:
        text(x + w / 2, y + h - 14, big, 20, 700, INK)


def line(x1, y1, x2, y2, stroke=GREY, dash="2 5", arrow=True, width=2):
    m = ' marker-end="url(#a)"' if arrow else ""
    if stroke == ORANGE and arrow:
        m = ' marker-end="url(#ao)"'
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
               f'stroke-width="{width}"{d}{m}/>')


W, H = 1320, 1030
text(40, 44, "Seven outages, no wire between them, and one question above them", 25, 700, INK, "start")
text(40, 72, f"What the frozen model (version 1) holds as of {last['as_of'].replace('T', ' ').replace('Z', ' UTC')}. "
     "Percentages on the outages are the middle observer's chance that it was an attack.", 14, 400, GREY, "start")

# the campaign question
box(40, 100, 1240, 104, "One campaign behind several of them?",
    ["the only week-level question version 1 asks",
     f"calm {pct(last['p_campaign_calm'])}   ·   middle {pct(last['p_campaign_middle'])}   ·   "
     f"suspicious {pct(last['p_campaign_suspicious'])}"], stroke=GREY, dash="2 5", tsize=18)

E = [("ms365-nov12", "Microsoft 365", "12 to 13 Nov", ["own gateway software;", "final report out"]),
     ("faa-ground-stop", "FAA ground stop", "13 Nov", ["a new router flooded", "the network, says FAA"]),
     ("chase-nov16", "Chase", "16 Nov", ["software bug, says Chase;", "vendor attack \"separate\""]),
     ("united-nov16", "United Airlines", "16 Nov", ["weight system; no cause;", "\"no indication\""]),
     ("nsanet-nov17", "NSA Net", "17 Nov", ["patching, say the NSA", "and the director"]),
     ("delta-nov22", "Delta Air Lines", "22 Nov", ["weight system; no cause;", "\"no sign\" of cyber"]),
     ("fincen-nov24", "Treasury FinCEN", "24 Nov", ["shut down after", "unauthorised access"])]
cx = []
for i, (eid, name, when, lines) in enumerate(E):
    bw = (1240 - 16 * (len(E) - 1)) / len(E)
    x = 40 + i * (bw + 16)
    cx.append(x + bw / 2)
    line(x + bw / 2, 204, x + bw / 2, 296)
    box(x, 300, bw, 132, name, [when] + lines, big=pct(ev[eid]["p_attack_middle"]), tsize=14)
mx = (cx[0] + cx[1]) / 2
text(mx, 244, "no shared", 12, 400, GREY)
text(mx, 260, "vendor or wire", 12, 400, GREY)
out.append(f'<path d="M{mx - 6} 270 l12 12 m0 -12 l-12 12" stroke="{INK}" stroke-width="2" fill="none"/>')

# context rows
text(40, 650, "Logged around them as context. Version 1 does not score these, apart from the ransomware claim.", 14, 700, GREY, "start")
S = [("Two federal systems", ["hit by security", "incidents in October,", "before the window"], None, ""),
     ("Amtrak", ["booking down during", "the ground stop:", "a knock-on"], 1, "solid"),
     ("Weather Service", ["reported down;", "the agency denied it"], 1, "dot"),
     ("Six other banks", ["named from user", "reports; most", "denied any fault"], 2, "dot"),
     ("Ransomware claim", ["Chase confirms a data", "theft at its vendors;", "denies a link to the outage"], 2, "orange"),
     ("Apple", ["internal update,", "says Apple;", "not on the panel"], None, ""),
     ("Optimizely", ["a confirmed attack", "on 178 websites,", "news sites among them"], None, "")]
for i, (name, lines, target, kind) in enumerate(S):
    x = 40 + i * 179
    orange = kind == "orange"
    box(x, 520, 166, 104, name, lines, stroke=ORANGE if orange else LINE,
        dash="" if orange else "6 5", tsize=14)
    if target is not None:
        if kind == "solid":
            line(cx[target] - 30, 432, x + 83, 516, stroke=GREY, dash="")
        elif orange:
            line(x + 83, 520, cx[target] + 40, 436, stroke=ORANGE, dash="7 5", width=2.5)
        else:
            line(x + 83, 520, cx[target] + (10 if target == 1 else 0), 436)

# the missing layer
out.append(f'<rect x="40" y="684" width="1240" height="92" rx="10" fill="#fcebe3" stroke="{ORANGE}" '
           f'stroke-width="2" stroke-dasharray="7 5"/>')
text(660, 714, "Not in version 1: the news layer, and the intrusions", 18, 700)
text(660, 738, "Are the reports themselves the event? A wave of coverage, organic or pushed, with phantom outages in it.", 14, 400, GREY)
text(660, 758, "Also outside it: the reported intrusions (Chase's vendor, FBI, USDA, CIA, Air Force) that are not outages. Both are for version 2.", 14, 400, GREY)

# outputs
O = [("At least one of the seven was an attack",
      [f"calm {pct(last['p_any_attack_calm'])}  ·  suspicious {pct(last['p_any_attack_suspicious'])}"],
      "middle " + pct(last["p_any_attack_middle"])),
     ("This many after a big one, nothing unusual",
      [f"{last['post_primer_count']} outages in the {float(last['exposure_days']):.1f} days since the ground stop"],
      pct(last["p_count_ordinary"])),
     ("Would have been national news in a quiet week", ["by the model's tier figures"],
      f"{float(last['quiet_week_visible']):.1f} of {last['events_counted']}")]
for i, (t, lines, big) in enumerate(O):
    box(40 + i * 420, 812, 400, 100, t, lines, big=big, tsize=15)

# legend
y = 960
out.append(f'<line x1="40" y1="{y-26}" x2="1280" y2="{y-26}" stroke="#e4e3dc" stroke-width="1.5"/>')
line(40, y, 90, y, stroke=GREY, dash="", arrow=False); text(102, y + 5, "led to: a knock-on", 14, 400, GREY, "start")
line(330, y, 380, y, arrow=False); text(392, y + 5, "asked or reported, not established", 14, 400, GREY, "start")
line(690, y, 740, y, stroke=ORANGE, dash="7 5", arrow=False, width=2.5); text(752, y + 5, "open: a claim or a denied link", 14, 400, GREY, "start")
out.append(f'<rect x="990" y="{y-9}" width="46" height="18" rx="5" fill="#fff" stroke="{LINE}" stroke-width="2" stroke-dasharray="6 5"/>')
text(1048, y + 5, "context, not scored", 14, 400, GREY, "start")
text(40, 1005, f"Model v1 frozen 18 Nov 2026, 10:00 UTC. Rows known before the freeze are scored in hindsight. Log row {last['row_id']}.", 12, 400, GREY, "start")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       'font-family="Inter, Helvetica Neue, Arial, sans-serif">'
       f'<defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
       f'<path d="M0 0 L9 4.5 L0 9 z" fill="{GREY}"/></marker>'
       f'<marker id="ao" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
       f'<path d="M0 0 L9 4.5 L0 9 z" fill="{ORANGE}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#fff"/>' + "".join(out) + "</svg>")
with open(os.path.join(ROOT, "analysis", "model-state.svg"), "w") as f:
    f.write(svg)
print("wrote analysis/model-state.svg")
