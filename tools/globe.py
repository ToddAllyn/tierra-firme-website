#!/usr/bin/env python3
"""Draws globe.svg: the Americas, Latin America highlighted, routes from Dallas across Central and South America.
Needs: pip install "geopandas==0.14.4" (bundles the Natural Earth low-res world outlines)."""
import math, os, warnings
warnings.filterwarnings('ignore')
import geopandas
from shapely.geometry import MultiPolygon

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'globe.svg')
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
lon0, lat0 = math.radians(-76), math.radians(4)   # centre on the Americas, tilted south
R, C = 148, 150

def proj(lon, lat):
    l, p = math.radians(lon), math.radians(lat)
    cosc = math.sin(lat0)*math.sin(p) + math.cos(lat0)*math.cos(p)*math.cos(l-lon0)
    x = R*math.cos(p)*math.sin(l-lon0)
    y = R*(math.cos(lat0)*math.sin(p) - math.sin(lat0)*math.cos(p)*math.cos(l-lon0))
    return C+x, C-y, cosc >= 0

def path(coords, close=True):
    segs, cur = [], []
    for lon, lat in coords:
        x, y, v = proj(lon, lat)
        if v: cur.append(f"{x:.1f},{y:.1f}")
        elif cur: segs.append(cur); cur = []
    if cur: segs.append(cur)
    return ''.join('M' + ' '.join(s) + ('Z' if close and len(segs) == 1 else '') for s in segs if len(s) > 2)

grat = [path([(lon, la) for la in range(-90, 91, 3)], False) for lon in range(-180, 180, 20)]
grat += [path([(lo, lat) for lo in range(-180, 181, 3)], False) for lat in range(-60, 81, 20)]

LATAM = {'South America'}
CENTRAL = {'Mexico', 'Guatemala', 'Belize', 'Honduras', 'El Salvador', 'Nicaragua', 'Costa Rica', 'Panama',
           'Cuba', 'Dominican Rep.', 'Haiti', 'Jamaica', 'Puerto Rico', 'Bahamas', 'Trinidad and Tobago'}
hi, lo = [], []
for _, row in world.iterrows():
    g = row.geometry
    polys = g.geoms if isinstance(g, MultiPolygon) else [g]
    target = hi if (row['continent'] in LATAM or row['name'] in CENTRAL) else lo
    for p in polys:
        d = path(list(p.exterior.coords))
        if d: target.append(d)

HUB = ('Dallas', -96.8, 32.78)
DESTS = [  # (name, lon, lat, emphasis)
    ('Mexico City', -99.13, 19.43, 0), ('Panama City', -79.52, 8.98, 0), ('Bogotá', -74.07, 4.71, 1),
    ('Lima', -77.04, -12.05, 0), ('São Paulo', -46.63, -23.55, 1), ('Buenos Aires', -58.38, -34.60, 0),
    ('Santiago', -70.67, -33.45, 0),
]
hx, hy, _ = proj(HUB[1], HUB[2])
arcs, dots = [], []
for name, lon, lat, em in DESTS:
    x, y, v = proj(lon, lat)
    if not v: continue
    mx, my = (hx+x)/2, (hy+y)/2
    dx, dy = x-hx, y-hy
    L = math.hypot(dx, dy) or 1
    bend = 0.10*L + 0.9*abs(x-hx)  # bow east, more for eastern destinations, so routes fan out
    cx, cy = mx + dy/L*bend, my - dx/L*bend
    w = 1.4 if em else 1.0
    op = 0.9 if em else 0.6
    arcs.append(f'<path d="M{hx:.1f} {hy:.1f} Q{cx:.1f} {cy:.1f} {x:.1f} {y:.1f}" stroke-width="{w}" stroke-opacity="{op}"/>')
    r = 4.2 if em else 2.8
    dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#e0693a"{"" if em else " fill-opacity=\"0.85\""}/>')

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
<circle cx="150" cy="150" r="148" fill="none" stroke="rgba(255,255,255,0.28)" stroke-width="1.2"/>
<path d="{' '.join(grat)}" fill="none" stroke="rgba(255,255,255,0.11)" stroke-width="0.7"/>
<path d="{' '.join(lo)}" fill="rgba(240,178,62,0.16)" stroke="rgba(240,178,62,0.45)" stroke-width="0.4" stroke-linejoin="round"/>
<path d="{' '.join(hi)}" fill="rgba(240,178,62,0.5)" stroke="rgba(240,178,62,0.95)" stroke-width="0.5" stroke-linejoin="round"/>
<g fill="none" stroke="#ffffff" stroke-dasharray="3 5" stroke-linecap="round">{''.join(arcs)}</g>
{''.join(dots)}
<circle cx="{hx:.1f}" cy="{hy:.1f}" r="4.2" fill="#fff"/>
</svg>"""
open(OUT, 'w').write(svg)
print('wrote', OUT, len(svg))
