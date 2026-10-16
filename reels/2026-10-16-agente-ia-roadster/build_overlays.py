"""Reel 'agente de IA x carro voador': aplica os textos (gancho, AMBIENTE, PERCEPÇÃO, RACIOCÍNIO,
AÇÃO, 'Leia a legenda') sobre o vídeo gerado sem texto no OpenArt e acrescenta o cartão de CTA.
Uso: python3 build_overlays.py <video_sem_texto.mp4>   (tempos em CUES; ajuste se os cortes mudarem)"""
import subprocess, sys, base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "gfcode_2026-10-16_agente_ia_roadster_semtexto.mp4"
OUT = HERE / "gfcode_2026-10-16_agente_ia_roadster.mp4"
TMP = HERE / "_ov"; TMP.mkdir(exist_ok=True)
W, H = 720, 1280
BOLD = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
BLACK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
CYAN = (6, 229, 248, 255)

# (início, fim, tipo, texto)
CUES = [
    (0.15, 3.0,  "hook", "O carro da Tesla “voa”.\nMas não sozinho."),
    (3.0,  5.0,  "word", "AMBIENTE"),
    (5.0,  7.0,  "word", "PERCEPÇÃO"),
    (7.0,  9.0,  "word", "RACIOCÍNIO"),
    (9.0,  10.5, "word", "AÇÃO"),
    (10.8, 15.0, "pill", "Leia a legenda \U0001F447"),
]
STEP = {"AMBIENTE": 1, "PERCEPÇÃO": 2, "RACIOCÍNIO": 3, "AÇÃO": 4}


def shadow_text(img, xy, text, font, fill=(255, 255, 255, 255), anchor="mm", spacing=10, blur=6):
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).multiline_text((xy[0] + 2, xy[1] + 4), text, font=font, fill=(0, 0, 0, 200),
                                      anchor=anchor, align="center", spacing=spacing)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).multiline_text(xy, text, font=font, fill=fill, anchor=anchor, align="center", spacing=spacing)


def render_png(kind, text, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if kind == "hook":
        shadow_text(img, (W // 2, 560), text, ImageFont.truetype(BLACK, 54), spacing=14)
    elif kind == "word":
        f = ImageFont.truetype(BLACK, 92 if len(text) <= 8 else 78)
        shadow_text(img, (W // 2, 600), text, f)
        n = STEP[text]
        d = ImageDraw.Draw(img)
        for i in range(4):  # indicador de etapa 1-4
            x = W // 2 - 66 + i * 44
            d.rounded_rectangle((x, 668, x + 32, 676), 4, fill=CYAN if i < n else (255, 255, 255, 110))
    elif kind == "pill":
        img.save(path)  # o pill tem emoji: renderizado via Chromium abaixo
        return
    img.save(path)


def render_pill(text, path):
    html = f"""<html><body style="margin:0;width:{W}px;height:{H}px;background:transparent;font-family:Inter">
    <div style="position:absolute;left:50%;top:1010px;transform:translateX(-50%);background:#0b0f16d9;
    color:#fff;font-weight:800;font-size:34px;padding:16px 30px;border-radius:999px;white-space:nowrap;
    box-shadow:0 6px 24px #0007">{text}</div></body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(html); pg.screenshot(path=str(path), omit_background=True); b.close()


inputs, chains = [], []
for i, (t0, t1, kind, text) in enumerate(CUES):
    png = TMP / f"cue{i}.png"
    render_pill(text, png) if kind == "pill" else render_png(kind, text, png)
    inputs += ["-loop", "1", "-framerate", "24", "-t", "15.1", "-i", str(png)]
    chains.append(f"[{i+1}:v]format=rgba,fade=t=in:st={t0}:d=0.18:alpha=1,fade=t=out:st={t1-0.15}:d=0.15:alpha=1[o{i}]")
fc = ";".join(chains)
prev = "[0:v]"
for i, (t0, t1, *_r) in enumerate(CUES):
    fc += f";{prev}[o{i}]overlay=0:0:enable='between(t,{t0},{t1})'[v{i}]"
    prev = f"[v{i}]"
fc += f";{prev}format=yuv420p[v]"
NOCTA = TMP / "sem_cta.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), *inputs, "-filter_complex", fc,
                "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
                "-c:a", "aac", "-b:a", "160k", "-shortest", str(NOCTA)], check=True)

# cartão de CTA (mesmo visual dos outros reels)
logo = base64.b64encode((HERE.parent.parent / "site/assets/logo-mark.png").read_bytes()).decode()
CARD = TMP / "cta.png"
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif;color:#e8ecf2;
 background:radial-gradient(110% 70% at 50% 42%,#13202f 0%,#0a0f17 60%,#05080d 100%)}}
.wrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 80px}}
.prof{{display:flex;align-items:center;gap:34px;background:#0f1520;border:3px solid #2a3547;border-radius:40px;padding:34px 44px;margin-bottom:90px}}
.prof img{{width:150px;height:150px;border-radius:50%;background:#05080d;border:4px solid #06e5f8;object-fit:contain;padding:18px}}
.prof .n{{font-size:58px;font-weight:900;text-align:left}}.prof .d{{font-size:32px;color:#8b97a8;text-align:left;margin-top:6px}}
.h{{font-size:150px;font-weight:900;letter-spacing:-4px;line-height:.95}}.h span{{color:#06e5f8}}
.sub{{font-size:46px;color:#b8c2d0;font-weight:600;margin:34px 0 80px}}
.btn{{font-size:68px;font-weight:900;color:#05080d;background:#06e5f8;border-radius:999px;padding:34px 110px;box-shadow:0 0 70px #06e5f866}}
.hand{{font-size:110px;margin-top:-18px;transform:translateX(150px)}}
.alt{{font-size:44px;font-weight:800;margin-top:50px}}
</style></head><body><div class="wrap">
<div class="prof"><img src="data:image/png;base64,{logo}"><div><div class="n">@gf.code</div><div class="d">IA aplicada de verdade</div></div></div>
<div class="h">SEGUE<br>o <span>@gf.code</span></div>
<div class="sub">pra montar seu primeiro agente de IA</div>
<div class="btn">Seguir</div><div class="hand">👆</div>
<div class="alt">💾 E salva esse vídeo pra consultar depois</div>
</div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path=str(CARD)); b.close()

dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(NOCTA)]))
CTA = 3.0
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(NOCTA), "-loop", "1", "-t", str(CTA + 0.4), "-framerate", "24", "-i", str(CARD),
    "-filter_complex",
    f"[0:v]fps=24,format=yuv420p,setsar=1[v0];[1:v]scale=720:1280,fps=24,format=yuv420p,setsar=1[v1];"
    f"[v0][v1]xfade=transition=fade:duration=0.4:offset={dur-0.4}[v];"
    f"[0:a]aresample=44100,apad=pad_dur={CTA},afade=t=out:st={dur-0.3}:d=0.6[a]",
    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "19", "-preset", "slow", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(OUT)], check=True)
for f in TMP.iterdir(): f.unlink()
TMP.rmdir()
print(OUT)
