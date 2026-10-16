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
.wrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 80px}}
.prof{{display:flex;align-items:center;gap:34px;background:#0f1520;border:3px solid #2a3547;border-radius:40px;padding:34px 44px;margin-bottom:90px}}
.prof img{{width:150px;height:150px;border-radius:50%;background:#05080d;border:4px solid #06e5f8;object-fit:contain;padding:18px}}
.prof .n{{font-size:58px;font-weight:900;text-align:left}}.prof .d{{font-size:32px;color:#8b97a8;text-align:left;margin-top:6px}}
.h{{font-size:150px;font-weight:900;letter-spacing:-4px;line-height:.95}}
.h span{{color:#06e5f8}}
.sub{{font-size:46px;color:#b8c2d0;font-weight:600;margin:34px 0 80px}}
.btn{{font-size:68px;font-weight:900;color:#05080d;background:#06e5f8;border-radius:999px;padding:34px 110px;box-shadow:0 0 70px #06e5f866}}
.hand{{font-size:110px;margin-top:-18px;transform:translateX(150px)}}
.alt{{font-size:44px;font-weight:800;margin-top:50px;color:#e8ecf2}}
</style></head><body><div class="wrap">
<div class="prof"><img src="data:image/png;base64,{logo}"><div><div class="n">@gf.code</div><div class="d">IA aplicada de verdade</div></div></div>
<div class="h">SEGUE<br>o <span>@gf.code</span></div>
<div class="sub">pra usar IA sem repassar erro pro cliente</div>
<div class="btn">Seguir</div>
<div class="hand">👆</div>
<div class="alt">💾 E salva esse vídeo pra consultar depois</div>
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
