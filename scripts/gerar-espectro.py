#!/usr/bin/env python3
"""Gera o espectro punk de 35 barras. Python 3.9+, sem dependências."""

import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/espectro-punk-35.svg"

WIDTH, HEIGHT = 960, 238
BAR_COUNT = 35
BAR_WIDTH, GAP = 17, 8
BOTTOM = 185

# Dois compassos em 4/4. O andamento reduzido permite enxergar cada barra
# percorrendo o caminho completo, sem o efeito de poucos quadros.
BPM = 84
FRAMES = 64
LOOP_SECONDS = (60 / BPM) * 8
TAU = math.tau

random.seed(1995)


def bar_sequence(index: int) -> list[int]:
    """Cria uma onda viajante: barras vizinhas seguem direções diferentes."""
    frequency = index / (BAR_COUNT - 1)
    low = 1 - frequency
    middle = math.exp(-((frequency - 0.50) / 0.29) ** 2)
    high = frequency
    silhouette = 17 + 24 * math.sin(math.pi * frequency) ** 0.82
    values = []

    for frame in range(FRAMES + 1):
        position = frame / FRAMES

        # Ondas em sentidos opostos impedem que todas as barras subam juntas.
        travelling = 0.5 + 0.5 * math.sin(TAU * (position + frequency))
        returning = 0.5 + 0.5 * math.sin(TAU * (2 * position - 2 * frequency))
        breath = 0.5 + 0.5 * math.sin(TAU * (position + index / BAR_COUNT))
        beat = 0.5 + 0.5 * math.sin(TAU * (4 * position + 1.5 * frequency))
        height = (
            silhouette
            + 76 * travelling * (0.38 + 0.62 * middle)
            + 34 * returning * (0.38 + 0.62 * high)
            + 28 * breath * (0.42 + 0.58 * low)
            + 15 * beat * (0.30 + 0.70 * high)
        )
        values.append(max(19, min(158, round(height))))

    return values


left = (WIDTH - (BAR_COUNT * BAR_WIDTH + (BAR_COUNT - 1) * GAP)) / 2
key_times = ";".join(f"{frame / FRAMES:.6f}" for frame in range(FRAMES + 1))


def make_wall_marks() -> str:
    marks = []
    for index in range(210):
        x = 8 + (index * 137 + index * index * 3) % 944
        y = 8 + (index * 83 + index * index * 5) % 220
        opacity = 0.07 + (index % 7) * 0.025
        if index % 4 == 0:
            length = 5 + (index * 11) % 24
            tilt = -8 + (index % 17)
            marks.append(
                f'    <path d="M{x} {y}l{length} {tilt}" stroke="#fff" '
                f'stroke-width="{1 + index % 3}" opacity="{opacity:.3f}"/>'
            )
        else:
            radius = (0.7, 1.0, 1.5, 2.1)[index % 4]
            marks.append(
                f'    <circle cx="{x}" cy="{y}" r="{radius}" fill="#fff" '
                f'opacity="{opacity:.3f}"/>'
            )
    return "\n".join(marks)


def make_spray() -> str:
    drops = []
    centers = ((98, 70), (245, 190), (476, 54), (708, 185), (868, 74))
    for index in range(115):
        cx, cy = centers[index % len(centers)]
        angle = (index * 137.5) * math.pi / 180
        distance = 7 + (index * 19) % 76
        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance * 0.52
        radius = (0.8, 1.2, 1.8, 2.8, 4.1)[index % 5]
        opacity = 0.30 + (index % 4) * 0.16
        drops.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" '
            f'fill="#fff" opacity="{opacity:.2f}"/>'
        )
    return "\n".join(drops)


masks = []
bars = []
bar_shadows = []
for index in range(BAR_COUNT):
    x = left + index * (BAR_WIDTH + GAP)
    heights = bar_sequence(index)
    ys = [BOTTOM - height for height in heights]
    lean = (-1.5, 0.7, -0.8, 1.2, -0.2, 0.9)[index % 6]

    # Falhas de tinta dentro de cada barra, como spray gasto sobre concreto.
    chips = []
    for chip in range(3):
        chip_x = x + 2 + ((index * 5 + chip * 7) % max(3, BAR_WIDTH - 7))
        chip_y = 37 + ((index * 29 + chip * 47) % 126)
        chip_w = 4 + ((index + chip * 3) % 8)
        chip_h = 2 + ((index + chip) % 3)
        chips.append(
            f'      <rect x="{chip_x:.1f}" y="{chip_y}" width="{chip_w}" '
            f'height="{chip_h}" fill="#000" transform="rotate({-16 + (index + chip) % 25} '
            f'{x + BAR_WIDTH / 2:.1f} {chip_y + chip_h / 2:.1f})"/>'
        )
    masks.append(
        f'''    <mask id="chip-{index}" maskUnits="userSpaceOnUse" x="{x - 7:.1f}" y="20" width="{BAR_WIDTH + 14}" height="170">
      <rect x="{x - 4:.1f}" y="22" width="{BAR_WIDTH + 8}" height="166" fill="#fff"/>
{chr(10).join(chips)}
    </mask>'''
    )

    common = (
        f'dur="{LOOP_SECONDS:.3f}s" begin="-{(index % 9) * 0.017:.3f}s" '
        f'repeatCount="indefinite" calcMode="linear" keyTimes="{key_times}"'
    )
    values = ";".join(map(str, heights))
    y_values = ";".join(map(str, ys))
    bar_shadows.append(
        f'    <rect x="{x - 3:.1f}" y="35" width="{BAR_WIDTH + 6}" height="150" '
        f'fill="#fff" opacity=".055" filter="url(#spray-halo)"/>'
    )
    bars.append(
        f'''    <rect x="{x:.1f}" y="{ys[0]}" width="{BAR_WIDTH}" height="{heights[0]}" fill="#fff"
      mask="url(#chip-{index})" transform="rotate({lean} {x + BAR_WIDTH / 2:.1f} {BOTTOM})">
      <animate attributeName="height" values="{values}" {common}/>
      <animate attributeName="y" values="{y_values}" {common}/>
    </rect>'''
    )

drips = []
for index, x in enumerate((73, 128, 211, 325, 418, 548, 652, 771, 846, 901)):
    length = (18, 31, 13, 39, 24)[index % 5]
    width = (3, 5, 2, 4)[index % 4]
    drips.append(
        f'    <path d="M{x} 184v{length}" stroke="#fff" stroke-width="{width}" '
        f'stroke-linecap="round" opacity="{0.58 + (index % 3) * 0.14:.2f}"/>'
    )
    drips.append(
        f'    <circle cx="{x}" cy="{184 + length + 3}" r="{1.4 + index % 3}" '
        f'fill="#fff" opacity=".72"/>'
    )

checkers = []
for side in (0, 1):
    origin_x = 17 if side == 0 else 883
    for row in range(3):
        for column in range(5):
            if (row + column + side) % 2 == 0:
                checkers.append(
                    f'    <rect x="{origin_x + column * 12}" y="{196 + row * 11}" '
                    f'width="13" height="12" fill="#fff" opacity=".42" '
                    f'transform="rotate({-4 if side == 0 else 4} {origin_x + 30} 212)"/>'
                )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="238" viewBox="0 0 960 238" role="img" aria-label="Analisador de espectro punk em preto e branco com trinta e cinco barras animadas">
  <defs>
    <filter id="rough" x="-7%" y="-4%" width="114%" height="108%">
      <feTurbulence type="fractalNoise" baseFrequency="0.025 0.20" numOctaves="2" seed="23" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="3.8" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="spray-halo" x="-30%" y="-10%" width="160%" height="120%">
      <feGaussianBlur stdDeviation="5 1.8"/>
    </filter>
{chr(10).join(masks)}
  </defs>

  <rect width="960" height="238" fill="#030303"/>

  <g aria-hidden="true">
{make_wall_marks()}
    <path d="M-12 30L71 17L143 29L216 13L300 26L378 10L451 28L526 14L603 25L681 11L764 28L842 15L972 30" fill="none" stroke="#fff" stroke-width="7" opacity=".28"/>
    <path d="M-8 221L82 207L164 222L249 209L329 226L415 211L502 225L587 208L674 223L758 210L846 225L970 211" fill="none" stroke="#fff" stroke-width="9" opacity=".34"/>
    <path d="M47 151C129 43 230 45 299 132S476 207 550 106S731 34 908 137" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity=".075" filter="url(#rough)"/>
    <path d="M80 117C214 196 340 39 475 117S735 191 886 76" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".12"/>
    <path d="M39 91L92 52L75 113L132 69M819 87L892 47L866 112L930 72" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="square" stroke-linejoin="bevel" opacity=".66"/>
{make_spray()}
{chr(10).join(checkers)}
{chr(10).join(bar_shadows)}
  </g>

  <g filter="url(#rough)" shape-rendering="geometricPrecision">
{chr(10).join(bars)}
  </g>

  <g aria-hidden="true">
    <path d="M45 185C147 180 241 191 342 184S549 190 651 183S850 192 918 184" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" filter="url(#rough)"/>
    <path d="M57 191C175 187 283 196 400 190S640 196 902 190" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".74"/>
{chr(10).join(drips)}
    <path d="M27 55L54 31M30 31L56 58M903 33L934 61M932 31L904 65" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="square" opacity=".78"/>
  </g>
</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")
print(f"Espectro gerado: {OUTPUT}")
