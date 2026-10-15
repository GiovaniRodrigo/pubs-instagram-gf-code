"""Reel 'câmera dupla' (visual Dual Camera simulado): mesma IA, dois pedidos, dois resultados.
Renderiza frames com Playwright (HTML animado por tempo) e monta o MP4 com ffmpeg. Sem narração:
o som entra pela biblioteca do TikTok na publicação."""
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
FR = HERE / "frames"
FR.mkdir(exist_ok=True)
FPS = 15
DUR = 26.0

PROMPT_A = "Escreve um e-mail pro cliente sobre o atraso."
RESP_A = ("Prezado cliente,\nPedimos desculpas pelo inconveniente. "
          "Estamos trabalhando para resolver a situação o mais rápido possível.\nAtenciosamente,\nEquipe")
PROMPT_B = ("Você é atendente da loja. Avise a cliente Marina que o pedido #4821 atrasou. "
            "Até 5 linhas, tom gentil. Use os dados do rastreio abaixo.\n📎 rastreio_4821.pdf")
RESP_B = ("Oi, Marina! Seu pedido #4821 ficou retido no centro de distribuição de Campinas. "
          "A nova previsão de entrega é quinta, 16/10.\nVocê acompanha aqui: rastreio BR4821XZ.\n"
          "Qualquer dúvida, é só responder. 💙")

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;background:#05080d;font-family:Inter,sans-serif;color:#e8ecf2;overflow:hidden}
.cam{position:absolute;left:30px;right:30px;border-radius:44px;overflow:hidden;
 background:radial-gradient(120% 90% at 50% 40%,#1a2433 0%,#0b1018 70%,#05080d 100%);border:3px solid #1f2a3a}
#c1{top:30px;height:915px}#c2{top:975px;height:915px}
.hud{position:absolute;top:26px;left:30px;right:30px;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:700;color:#cfd8e6;z-index:5}
.rec{display:flex;gap:12px;align-items:center}.rec i{width:18px;height:18px;border-radius:50%;background:#ef4444;display:inline-block}
.lens{background:#00000080;border:2px solid #ffffff40;border-radius:999px;padding:6px 16px;font-size:24px}
.lab{position:absolute;bottom:26px;left:30px;background:#000000a0;border-radius:12px;padding:8px 16px;font-size:26px;font-weight:800;z-index:5}
.grain{position:absolute;inset:0;background:repeating-linear-gradient(0deg,#ffffff04 0 2px,transparent 2px 4px);pointer-events:none;z-index:4}
.vig{position:absolute;inset:0;box-shadow:inset 0 0 160px #000c;pointer-events:none;z-index:4}
.screen{position:absolute;left:70px;right:70px;top:110px;bottom:110px;border-radius:26px;background:#0f1520;border:2px solid #2a3547;padding:36px 40px;transform:rotate(var(--r,0deg))}
.screen h4{font-size:26px;color:#8b97a8;margin-bottom:18px;letter-spacing:.5px}
.txt{font-size:42px;line-height:1.38;white-space:pre-wrap}
.mono{font-family:'DejaVu Sans Mono',monospace;font-size:38px;color:#e8ecf2}
.caret{display:inline-block;width:4px;height:40px;background:#06e5f8;vertical-align:-6px;margin-left:4px}
.mail{background:#f4f6fa;color:#1a2230;border-color:#d9e0ea}
.mail h4{color:#6b7689}
.badge{position:absolute;right:40px;bottom:120px;padding:14px 22px;border-radius:16px;font-size:34px;font-weight:900;z-index:6}
.bad{background:#ef4444;color:#fff}.good{background:#22c55e;color:#04130d}
.title{position:absolute;left:50%;top:960px;transform:translate(-50%,-50%);z-index:20;padding:22px 34px;border-radius:22px;
 font-weight:900;font-size:68px;letter-spacing:-1.5px;white-space:nowrap;background:#ffd60a;color:#0a0d12;box-shadow:0 10px 40px #000a}
.chip{display:inline-block;margin:8px;padding:10px 18px;border-radius:12px;font-weight:800;font-size:30px;color:#0a0d12}
.full{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;z-index:30;background:#05080d}
.hidden{display:none}
</style></head><body>
<div class="cam" id="c1"><div class="hud"><span class="rec"><i></i><span id="t1">00:00</span></span><span class="lens">1x</span></div>
 <div class="screen" id="s1"><h4 id="h1">ChatGPT · você</h4><div class="txt mono" id="p1"></div></div>
 <div class="lab" id="l1">CAM 1 · O PEDIDO</div><div class="grain"></div><div class="vig"></div></div>
<div class="cam" id="c2"><div class="hud"><span class="rec"><i></i><span id="t2">00:00</span></span><span class="lens">0.5x</span></div>
 <div class="screen mail" id="s2" style="--r:-1deg"><h4>E-mail gerado pela IA</h4><div class="txt" id="p2"></div></div>
 <div class="badge hidden" id="b2"></div>
 <div class="lab" id="l2">CAM 2 · O RESULTADO</div><div class="grain"></div><div class="vig"></div></div>
<div class="title hidden" id="tt"></div>
<div class="full hidden" id="fd"></div>
<script>
const PA=%PA%,RA=%RA%,PB=%PB%,RB=%RB%;
function typ(s,t0,t,cps){const n=Math.max(0,Math.min(s.length,Math.floor((t-t0)*cps)));return s.slice(0,n)}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function car(on){return on?'<span class="caret"></span>':''}
function mmss(t){const s=Math.floor(t);return '00:'+String(s).padStart(2,'0')}
window.render=function(t){
 t1.textContent=mmss(t);t2.textContent=mmss(t);
 const tt=document.getElementById('tt'),fd=document.getElementById('fd'),b2=document.getElementById('b2');
 tt.className='title hidden';fd.className='full hidden';b2.className='badge hidden';
 let p1='',p2='';
 if(t<2.6){tt.className='title';tt.textContent='MESMA IA. DOIS PEDIDOS.';}
 else if(t<11){ // pedido A
   h1.textContent='Pedido A · você';
   const a=typ(PA,2.8,t,22);p1=esc(a)+car(a.length<PA.length);
   const r=typ(RA,5.2,t,40);p2=esc(r);
   if(t>8.3){b2.className='badge bad';b2.textContent='😐 genérico';}
 } else if(t<21){ // pedido B
   h1.textContent='Pedido B · você';
   const a=typ(PB,11.2,t,34);p1=esc(a)+car(a.length<PB.length);
   const r=typ(RB,15.6,t,48);p2=esc(r);
   if(t>18.7){b2.className='badge good';b2.textContent='✅ pronto pra enviar';}
   if(t<11.8){tt.className='title';tt.textContent='AGORA, O PEDIDO CERTO';}
 } else if(t<24){
   fd.className='full';
   fd.innerHTML='<div style="font-size:44px;color:#8b97a8;font-weight:700">A diferença não é a IA.</div>'+
   '<div style="font-size:96px;font-weight:900;letter-spacing:-2px;margin:14px 0 40px">É o <span style="color:#06e5f8">pedido</span>.</div>'+
   '<div><span class="chip" style="background:#ffd60a">Papel</span><span class="chip" style="background:#60a5fa">Tarefa</span>'+
   '<span class="chip" style="background:#22c55e">Formato</span><span class="chip" style="background:#f472b6">Fonte</span></div>';
 } else {
   fd.className='full';
   fd.innerHTML='<div style="font-size:60px;font-weight:900">Salva esse vídeo 💾</div>'+
   '<div style="font-size:40px;color:#8b97a8;margin:26px 0 10px">e segue pra mais IA aplicada</div>'+
   '<div style="font-size:110px;font-weight:900;color:#06e5f8">@gf.code</div>';
 }
 if(t>=2.6&&t<21){document.getElementById('p1').innerHTML=p1;document.getElementById('p2').innerHTML=p2;}
 else if(t<2.6){document.getElementById('p1').innerHTML='';document.getElementById('p2').innerHTML='';}
};
</script></body></html>"""

import json
html = (HTML.replace("%PA%", json.dumps(PROMPT_A)).replace("%RA%", json.dumps(RESP_A))
            .replace("%PB%", json.dumps(PROMPT_B)).replace("%RB%", json.dumps(RESP_B)))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(html)
    pg.wait_for_timeout(300)
    n = int(DUR * FPS)
    for i in range(n):
        pg.evaluate(f"render({i / FPS})")
        pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=88)
    b.close()

out = HERE / "gfcode_2026-10-15_dual_cam.mp4"
subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"),
    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "22",
    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out)], check=True)
print(out, out.stat().st_size)
