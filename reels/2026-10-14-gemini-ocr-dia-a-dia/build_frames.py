"""Render the 8 scene frames (1080x1920) for the GF Code reel 'Gemini lê o mundo pela câmera'."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "frames"
OUT.mkdir(exist_ok=True)

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px}
body{background:#0a0d12;font-family:Inter,sans-serif;color:#e8ecf2;position:relative;overflow:hidden;
 background-image:linear-gradient(#ffffff06 1px,transparent 1px),linear-gradient(90deg,#ffffff06 1px,transparent 1px);
 background-size:60px 60px}
.tag{position:absolute;top:210px;left:50%;transform:translateX(-50%);padding:26px 34px;border-radius:22px;
 font-family:'Inter Display',Inter;font-weight:900;font-size:80px;line-height:.98;letter-spacing:-2px;text-align:center;
 color:#0a0d12;white-space:nowrap}
.y{background:#ffd60a}.g{background:#22c55e}.b{background:#60a5fa}.r{background:#ef4444;color:#fff}
.stage{position:absolute;top:520px;left:90px;right:90px}
.cap{position:absolute;top:1410px;left:100px;right:100px;text-align:center;font-family:'Inter Display',Inter;
 font-weight:800;font-size:54px;line-height:1.2;letter-spacing:-.5px}
.cap b{color:#ffd60a}
.card{background:#161b24;border:2px solid #263040;border-radius:34px;overflow:hidden}
.mono{font-family:'DejaVu Sans Mono',monospace}
/* camera view */
.cam{position:relative;height:560px;border-radius:30px;overflow:hidden;background:#1b2230;border:3px solid #2f3b50}
.cam .lbl{position:absolute;top:18px;left:22px;font-size:24px;color:#9fb0c8;display:flex;gap:10px;align-items:center}
.cam .lbl i{width:14px;height:14px;border-radius:50%;background:#ef4444;display:inline-block}
.ocr{position:absolute;border:4px solid #ffd60a;border-radius:8px;box-shadow:0 0 0 2000px #00000000}
.hl{outline:4px solid #ffd60a;outline-offset:8px;border-radius:4px;position:relative;display:inline-block}
.hl::before{content:attr(data-l);position:absolute;top:-52px;left:-10px;background:#ffd60a;color:#0a0d12;font:800 22px Inter;font-style:normal;padding:4px 10px;border-radius:6px;white-space:nowrap}
.ocr span{position:absolute;top:-38px;left:-4px;background:#ffd60a;color:#0a0d12;font-size:22px;font-weight:800;padding:4px 10px;border-radius:6px;white-space:nowrap}
.act{margin-top:30px;display:flex;align-items:center;gap:24px;padding:28px 34px;border-radius:28px;background:#0f1a12;border:3px solid #22c55e}
.act .ic{width:84px;height:84px;border-radius:22px;flex:none;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:900;color:#fff}
.act .t1{font-size:26px;color:#86efac}
.act .t2{font-size:38px;font-weight:800;color:#fff;line-height:1.2}
.spark{font-size:30px;color:#c4b5fd;margin-top:26px;display:flex;gap:12px;align-items:center}
"""

GEM = '<span style="color:#a78bfa;font-weight:900">✦</span>'


def scene(tag, tagcls, cam, act_color, act_letter, act_t1, act_t2, cap):
    return f"""
<div class="tag {tagcls}">{tag}</div>
<div class="stage">
 <div class="cam"><div class="lbl"><i></i>Gemini Live · câmera</div>{cam}</div>
 <div class="spark">{GEM} Gemini leu o texto e…</div>
 <div class="act"><div class="ic" style="background:{act_color}">{act_letter}</div>
  <div><div class="t1">{act_t1}</div><div class="t2">{act_t2}</div></div></div>
</div>
<div class="cap">{cap}</div>
"""


POSTER = """
<div style="position:absolute;left:190px;top:80px;width:520px;height:440px;background:#f5efe0;border-radius:6px;padding:34px;color:#1a1a1a">
 <div style="font-size:30px;font-weight:700;color:#b91c1c">MEETUP</div>
 <div style="font-size:56px;font-weight:900;line-height:1;margin-top:60px"><span class="hl" data-l="título">IA na Prática</span></div>
 <div style="font-size:30px;margin-top:70px"><span class="hl" data-l="data + hora">📅 <b>22/10 · 19h</b></span></div>
 <div style="font-size:28px;margin-top:18px">Auditório Central</div>
</div>
"""

LIST = """
<div style="position:absolute;left:230px;top:90px;width:440px;height:440px;background:#fff9c4;padding:56px 44px;color:#1e3a8a;
 font-family:'DejaVu Serif',serif;font-style:italic;font-size:40px;line-height:1.55">
 <span class="hl" data-l="texto manuscrito">leite<br>ovos (12)<br>café<br>pão de forma<br>banana</span>
</div>
"""

BOARD = """
<div style="position:absolute;left:70px;top:70px;width:760px;height:440px;background:#f8fafc;border:10px solid #9ca3af;border-radius:6px;padding:26px 40px;color:#1f2937;
 font-size:38px;line-height:1.55">
 <b style="color:#2563eb">Sprint 14</b><br><span class="hl" data-l="3 tarefas + responsáveis" style="margin-top:50px">• Ana — revisar API<br>• Léo — deploy sexta<br>• Bia — testes login</span>
</div>
"""

CARD = """
<div style="position:absolute;left:180px;top:100px;width:540px;height:360px;background:#fff;border-radius:16px;padding:40px;color:#111;box-shadow:0 20px 40px #0006">
 <div style="font-size:44px;font-weight:900">Café Grão Bom</div>
 <div style="font-size:28px;color:#555;margin-top:6px">torrefação artesanal</div>
 <div style="font-size:30px;margin-top:70px"><span class="hl" data-l="endereço">Rua das Palmeiras, 410<br>Centro</span></div>
</div>
"""

SCENES = {
"s1": """
<div class="tag r">AINDA DIGITA<br>TUDO À MÃO?</div>
<div class="stage" style="top:640px">
 <div class="card" style="padding:44px">
  <div style="font-size:30px;color:#8b97a8;margin-bottom:22px">Você, copiando de um cartaz:</div>
  <div class="mono" style="background:#0f131a;border:2px solid #3b82f6;border-radius:22px;padding:30px 32px;font-size:46px;color:#fff">
   Meetup IA na Prát<span style="display:inline-block;width:4px;height:48px;background:#ffd60a;vertical-align:-8px;margin-left:4px"></span></div>
  <div style="font-size:32px;color:#fca5a5;margin-top:28px">⏱ 2 min · 3 erros de digitação</div>
 </div>
</div>
<div class="cap">Para com isso.<br>A <b>câmera</b> faz por você.</div>
""",

"s2": f"""
<div class="tag y">GEMINI + OCR</div>
<div class="stage" style="display:flex;flex-direction:column;align-items:center">
 <div class="card" style="padding:30px 50px;font-size:44px;text-align:center"><div style="font-weight:800">📷 Câmera</div>
  <div style="font-size:28px;color:#8b97a8;margin-top:6px">você aponta para qualquer texto</div></div>
 <div style="width:6px;height:70px;background:#4b5565"></div>
 <div class="card" style="padding:30px 50px;font-size:44px;text-align:center;border-color:#ffd60a;background:#1d1a0b">
  <div style="font-weight:800;color:#ffd60a">OCR</div>
  <div style="font-size:28px;color:#c9b77a;margin-top:6px">Optical Character Recognition<br>(reconhecimento óptico de caracteres)</div></div>
 <div style="width:6px;height:70px;background:#4b5565"></div>
 <div class="card" style="padding:30px 50px;font-size:44px;text-align:center;border-color:#a78bfa;background:#17132a">
  <div style="font-weight:800;color:#c4b5fd">{GEM} IA entende</div>
  <div style="font-size:28px;color:#a99bd6;margin-top:6px">e age nos seus apps</div></div>
</div>
<div class="cap">Ler texto não é novidade.<br>Novidade é a IA <b>agir</b> com ele.</div>
""",

"s3": scene("CARTAZ → AGENDA", "b", POSTER, "#3b82f6", "31",
            "Google Agenda", "Evento criado: 22/10 · 19h", "Aponta pro cartaz:<br>vira <b>compromisso</b> na Agenda."),
"s4": scene("LISTA → KEEP", "y", LIST, "#f59e0b", "K",
            "Google Keep", "Nota “Compras” · 5 itens", "Lista escrita à mão:<br>vira <b>nota</b> no Keep."),
"s5": scene("QUADRO → TASKS", "g", BOARD, "#2563eb", "✓",
            "Google Tasks", "3 tarefas adicionadas", "Quadro da reunião:<br>tarefas direto no <b>Tasks</b>."),
"s6": scene("CARTÃO → MAPS", "b", CARD, "#16a34a", "⌖",
            "Google Maps", "Rota até Rua das Palmeiras, 410", "Endereço num cartão:<br><b>rota</b> aberta no Maps."),

"s7": f"""
<div class="tag g">SEM TROCAR DE APP</div>
<div class="stage" style="top:560px;display:flex;flex-direction:column;align-items:center">
 <div style="width:260px;height:260px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#c4b5fd,#6d28d9 70%);
  display:flex;align-items:center;justify-content:center;font-size:130px;color:#fff;box-shadow:0 0 120px #7c3aed88">✦</div>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:60px;width:100%">
  {''.join(f'<div class="card" style="padding:28px;display:flex;gap:20px;align-items:center;font-size:38px;font-weight:800"><span style="width:62px;height:62px;border-radius:16px;background:{c};display:flex;align-items:center;justify-content:center;color:#fff;font-size:30px">{l}</span>{n}</div>'
           for n, c, l in [("Agenda", "#3b82f6", "31"), ("Keep", "#f59e0b", "K"), ("Tasks", "#2563eb", "✓"), ("Maps", "#16a34a", "⌖")])}
 </div>
</div>
<div class="cap">Tudo numa <b>conversa só</b>.</div>
""",

"s8": """
<div class="tag y">SALVA PRA TESTAR</div>
<div class="stage" style="display:flex;flex-direction:column;gap:36px">
 <div class="card" style="padding:36px 40px">
  <div style="font-size:30px;color:#8b97a8;margin-bottom:14px">Como testar</div>
  <div style="font-size:38px;line-height:1.55">1. Abra o <b>Gemini Live</b><br>2. Toque na <b>câmera</b><br>3. Aponte e peça:<br>
   <span class="mono" style="color:#ffd60a;font-size:34px">“salva isso na minha agenda”</span></div>
 </div>
 <div class="card" style="padding:32px 40px;display:flex;gap:26px;align-items:center;border-color:#22c55e">
  <div style="width:96px;height:96px;border-radius:50%;background:#3b82f6;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:44px;flex:none">GF</div>
  <div><div style="font-size:30px;color:#86efac">segue pra mais IA no dia a dia</div><div style="font-size:60px;font-weight:900;color:#fff">@gf.code</div></div>
 </div>
</div>
<div class="cap">Salva esse vídeo<br>e segue o <b>@gf.code</b>.</div>
""",
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    for name, body in SCENES.items():
        page.set_content(f"<html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head><body>{body}</body></html>")
        page.wait_for_timeout(150)
        page.screenshot(path=str(OUT / f"{name}.png"))
        print("rendered", name)
    browser.close()
