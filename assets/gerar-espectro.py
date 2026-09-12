#!/usr/bin/env python3
"""Gera assets/espectro-punk.svg. Python 3.9+, sem dependências."""

import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/espectro-punk.svg"
WIDTH, HEIGHT = 960, 238
BPM = 190
LOOP = 60 / BPM * 8
BAR_COUNT = 47
BOTTOM = 188
random.seed(1996)


def sequence(index):
    center = 1 - abs(index - (BAR_COUNT - 1) / 2) / ((BAR_COUNT - 1) / 2)
    base = 18 + 35 * center
    values = []
    for beat in range(9):
        kick = 62 if beat in {0, 4, 8} else 24 if beat in {2, 6} else 8
        noise = random.uniform(-20, 26)
        ripple = 25 * abs(math.sin(index * 0.58 + beat * 1.7))
        height = base + kick * (0.4 + center * 0.7) + ripple + noise
        values.append(max(12, min(154, round(height))))
    return values


bars = []
bar_width, gap = 11, 7
left = (WIDTH - (BAR_COUNT * bar_width + (BAR_COUNT - 1) * gap)) / 2
for index in range(BAR_COUNT):
    heights = sequence(index)
    ys = [BOTTOM - height for height in heights]
    x = left + index * (bar_width + gap)
    begin = -((index % 7) * 0.021)
    common = (
        f'dur="{LOOP:.3f}s" begin="{begin:.3f}s" repeatCount="indefinite" '
        'calcMode="spline" keyTimes="0;.125;.25;.375;.5;.625;.75;.875;1" '
        'keySplines=".1 .8 .2 1;.7 0 .9 .2;.1 .8 .2 1;.7 0 .9 .2;'
        '.1 .8 .2 1;.7 0 .9 .2;.1 .8 .2 1;.7 0 .9 .2"'
    )
    bars.append(
        f'''  <rect x="{x:.1f}" y="{ys[0]}" width="{bar_width}" height="{heights[0]}" rx="2" fill="#fff">
    <animate attributeName="height" values="{";".join(map(str, heights))}" {common}/>
    <animate attributeName="y" values="{";".join(map(str, ys))}" {common}/>
  </rect>'''
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="238" viewBox="0 0 960 238" role="img" aria-labelledby="title description">
  <title id="title">Espectro punk</title>
  <desc id="description">Quarenta e sete barras brancas pulsam em um loop visual de 190 batidas por minuto.</desc>
  <rect width="960" height="238" rx="14" fill="#050505"/>
  <path d="M10 16L73 11L134 18L207 12L280 17L348 10L425 16L504 11L576 17L649 12L729 18L797 10L871 16L950 12M9 222L85 227L159 221L232 228L311 222L389 226L471 220L548 228L626 221L705 227L784 220L864 226L951 221" fill="none" stroke="#fff" stroke-width="4" opacity=".9"/>
  <g opacity=".22" fill="#fff" font-family="monospace" font-size="10">
    <text x="28" y="36">while (noise) &#123; create(); distort(); repeat(); &#125;</text>
    <text x="670" y="36">tempo = 190; gain++;</text>
    <text x="28" y="214">signal.filter(Boolean).map(make_it_louder);</text>
    <text x="716" y="214">// still alive</text>
  </g>
  <g shape-rendering="geometricPrecision">
{chr(10).join(bars)}
  </g>
  <path d="M18 188H942" stroke="#fff" stroke-width="3"/>
  <path d="M25 58L39 48L34 67L50 60M913 73L931 54L925 78L943 69" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
  <text x="28" y="55" fill="#fff" font-family="monospace" font-size="13" letter-spacing="2">190 BPM // LOOP VISUAL</text>
</svg>
'''
OUTPUT.write_text(svg, encoding="utf-8")
print(f"Espectro gerado: {OUTPUT}")
