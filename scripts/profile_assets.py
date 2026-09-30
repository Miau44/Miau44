#!/usr/bin/env python3
"""Generate the local SVG labels, animated tagline and qualitative profile maps.

Run: python scripts/profile_assets.py
No third-party dependencies. The maps describe areas, not proficiency scores.
"""

from html import escape
from math import cos, sin, pi
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
FONT = "ui-monospace, SFMono-Regular, Consolas, monospace"
THEMES = {
    "dark": dict(bg="#0D1628", line="#25344C", text="#F0E6F0", muted="#8291A8",
                 pink="#F78CA0", purple="#C9B1D9", teal="#76D8D2"),
    "light": dict(bg="#FFF8FA", line="#E9CFDA", text="#382336", muted="#806575",
                  pink="#B84368", purple="#7B5EA7", teal="#237F83"),
}


def svg(width, height, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">\n'
            f'<title id="title">{escape(title)}</title>\n{body}\n</svg>\n')


def write(name, content):
    (ASSETS / name).write_text(content, encoding="utf-8")


def profile_map(theme, title, center, labels):
    t = THEMES[theme]
    cx, cy = 230, 196
    points = [(cx + 104 * cos(-pi / 2 + n * pi / 3),
               cy + 104 * sin(-pi / 2 + n * pi / 3)) for n in range(6)]
    parts = [
        f'<rect x="1" y="1" width="458" height="358" rx="16" fill="{t["bg"]}" stroke="{t["line"]}"/>',
        f'<g font-family="{FONT}" text-anchor="middle">',
        f'<text x="230" y="33" fill="{t["text"]}" font-size="17" font-weight="700">{escape(title)}</text>',
    ]
    for radius in (36, 70, 104):
        vertices = ' '.join(f'{cx + radius*cos(-pi/2+n*pi/3):.1f},{cy + radius*sin(-pi/2+n*pi/3):.1f}' for n in range(6))
        parts.append(f'<polygon points="{vertices}" fill="none" stroke="{t["line"]}"/>')
    for n, ((x, y), label) in enumerate(zip(points, labels)):
        color = t[("pink", "purple", "teal")[n % 3]]
        parts.append(f'<path d="M{cx} {cy}L{x:.1f} {y:.1f}" stroke="{t["line"]}"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}"/>')
        angle = -pi / 2 + n * pi / 3
        lx, ly = cx + 139 * cos(angle), cy + 133 * sin(angle) + 5
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{t["text"]}" font-size="13">{escape(label)}</text>')
    parts.extend([
        f'<circle cx="{cx}" cy="{cy}" r="38" fill="{t["bg"]}" stroke="{t["purple"]}"/>',
        f'<text x="{cx}" y="{cy+5}" fill="{t["pink"]}" font-size="12" font-weight="700">{escape(center)}</text>',
        '</g>',
    ])
    return svg(460, 360, title + ': ' + ', '.join(labels), '\n'.join(parts))


def main():
    ASSETS.mkdir(exist_ok=True)
    for theme in THEMES:
        write(f'radar-{theme}.svg', profile_map(theme, 'Áreas de trabajo', 'BUILD',
              ['Backend', 'APIs REST', 'Bases de datos', 'Frontend', 'Reportes', 'Automatización']))
        write(f'radar-langs-{theme}.svg', profile_map(theme, 'Lenguajes del perfil', 'CODE',
              ['C#', 'TypeScript', 'JavaScript', 'PHP', 'Python', 'SQL']))

    # Simple text tiles for tools without a matching skillicons.dev asset.
    for name, title, label, color in [
        ('oracle', 'Oracle Database', 'ORA', '#F07883'),
        ('sqlserver', 'SQL Server', 'SQL', '#F78CA0'),
        ('powerbi', 'Power BI', 'BI', '#F3D29B'),
        ('pandas', 'Pandas', 'Pd', '#C7A4F5'),
        ('numpy', 'NumPy', 'Np', '#76D8D2'),
        ('azuredevops', 'Azure DevOps', 'AzDO', '#77C8F0'),
    ]:
        body = (f'<rect width="48" height="48" rx="10" fill="#242938"/>'
                f'<rect x="1" y="1" width="46" height="46" rx="9" fill="none" stroke="{color}" stroke-opacity=".4"/>'
                f'<text x="24" y="29" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="15" fill="{color}">{label}</text>')
        write(f'icon-{name}.svg', svg(48, 48, title, body))

    for name, title, label, width, color in [
        ('linkedin', 'LinkedIn de Mauricio Morales', 'in  LINKEDIN', 142, '#C7A4F5'),
        ('email', 'Email de Mauricio Morales', '@  EMAIL', 118, '#76D8D2'),
        ('github', 'GitHub de Miau44', '&lt;/&gt;  GITHUB', 146, '#F78CA0'),
    ]:
        body = (f'<rect width="{width}" height="32" rx="4" fill="{color}"/>'
                f'<text x="{width/2}" y="21" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#1A1A2E">{label}</text>')
        write(f'social-{name}.svg', svg(width, 32, title, body))

    lines = ['Mauricio Morales · Full-Stack Developer',
             'C# / .NET · Angular · NestJS · Laravel',
             'Bases de datos · Chatbots · Inteligencia Artificial']
    body = '''<style>
      text { fill: #b84368; font-family: ui-monospace, Consolas, monospace; font-size: 24px; font-weight: 700; }
      .line { opacity: 0; animation: cycle 12s infinite; }
      .one { opacity: 1; } .two { animation-delay: 4s; } .three { animation-delay: 8s; }
      .cursor { animation: blink 1s steps(2, start) infinite; }
      @keyframes cycle { 0%, 27% { opacity: 1; } 33.33%, 100% { opacity: 0; } }
      @keyframes blink { to { opacity: 0; } }
      @media (prefers-color-scheme: dark) { text { fill: #f78ca0; } }
      @media (prefers-reduced-motion: reduce) { .line, .cursor { animation: none; } .one { opacity: 1; } }
    </style>'''
    for line, cls in zip(lines, ('one', 'two', 'three')):
        body += f'<text class="line {cls}" x="450" y="37" text-anchor="middle">{escape(line)}<tspan class="cursor"> ▍</tspan></text>'
    write('typing.svg', svg(900, 64, ' · '.join(lines), body))
    print('Generated profile maps, tool tiles, social badges and animated tagline.')


if __name__ == '__main__':
    main()
