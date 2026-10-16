"""Acrescenta um cartão final de CTA (3 s) ao reel 'I.A. não faz o seu trabalho', no visual GF Code."""
import subprocess, base64
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
SRC = HERE / "gfcode_2026-10-16_ia_nao_faz_seu_trabalho.mp4"
OUT = HERE / "gfcode_2026-10-16_ia_nao_faz_seu_trabalho_cta.mp4"
CARD = HERE / "cta_card.png"
LOGO = HERE.parent.parent / "site/assets/logo-mark.png"
logo = base64.b64encode(LOGO.read_bytes()).decode()

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif;color:#e8ecf2;
 background:radial-gradient(110% 70% at 50% 42%,#13202f 0%,#0a0f17 60%,#05080d 100%)}}
.wrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}}
img{{width:200px;height:200px;object-fit:contain;margin-bottom:70px}}
.k{{font-size:46px;color:#8b97a8;font-weight:700}}
.h{{font-size:104px;font-weight:900;letter-spacing:-2px;line-height:1.05;margin:18px 0 70px}}
.h span{{color:#06e5f8}}
.row{{display:flex;gap:26px;justify-content:center;margin-bottom:80px}}
.chip{{font-size:44px;font-weight:800;padding:20px 36px;border-radius:999px;border:3px solid #2a3547;background:#0f1520}}
.handle{{font-size:120px;font-weight:900;color:#06e5f8}}
.sub{{font-size:40px;color:#8b97a8;margin-top:14px}}
</style></head><body><div class="wrap">
<img src="data:image/png;base64,{logo}">
<div class="k">A IA faz o rascunho.</div>
<div class="h">O trabalho<br>é <span>seu</span>.</div>
<div class="row"><div class="chip">💾 Salva</div><div class="chip">📤 Compartilha</div></div>
<div class="sub">segue pra mais IA aplicada</div>
<div class="handle">@gf.code</div>
</div></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.set_content(HTML); pg.wait_for_timeout(300); pg.screenshot(path=str(CARD)); b.close()

CTA = 3.0
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(SRC)]))
off = dur - 0.4  # transição de 0,4 s
subprocess.run(["ffmpeg","-v","error","-y","-i",str(SRC),"-loop","1","-t",str(CTA+0.4),"-framerate","24","-i",str(CARD),
 "-filter_complex",
 f"[0:v]fps=24,format=yuv420p,setsar=1[v0];[1:v]scale=720:1280,fps=24,format=yuv420p,setsar=1[v1];"
 f"[v0][v1]xfade=transition=fade:duration=0.4:offset={off}[v];"
 f"[0:a]aresample=44100,apad=pad_dur={CTA},afade=t=out:st={dur-0.3}:d=0.6[a]",
 "-map","[v]","-map","[a]","-c:v","libx264","-crf","19","-preset","slow","-pix_fmt","yuv420p",
 "-c:a","aac","-b:a","160k","-movflags","+faststart",str(OUT)],check=True)
print(OUT)
