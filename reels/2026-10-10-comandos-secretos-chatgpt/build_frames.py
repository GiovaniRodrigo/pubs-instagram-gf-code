"""Render the 5 scene frames (1080x1920) for the GF Code reel 'comandos secretos'."""
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
 font-family:'Inter Display',Inter;font-weight:900;font-size:84px;line-height:.98;letter-spacing:-2px;text-align:center;
 color:#0a0d12;white-space:nowrap}
.y{background:#ffd60a}.g{background:#22c55e}.r{background:#ef4444;color:#fff}
.stage{position:absolute;top:560px;left:90px;right:90px}
.cap{position:absolute;top:1390px;left:110px;right:110px;text-align:center;font-family:'Inter Display',Inter;
 font-weight:800;font-size:56px;line-height:1.2;letter-spacing:-.5px}
.cap b{color:#ffd60a}
.card{background:#161b24;border:2px solid #263040;border-radius:34px;overflow:hidden}
.mono{font-family:'DejaVu Sans Mono',monospace}
"""

SCENES = {
"s1": ("""
<div class="tag y">ESSES COMANDOS<br>NÃO EXISTEM</div>
<div class="stage">
 <div class="card" style="padding:44px">
  <div style="font-size:30px;color:#8b97a8;margin-bottom:22px">Mensagem para o ChatGPT</div>
  <div class="mono" style="background:#0f131a;border:2px solid #3b82f6;border-radius:22px;padding:30px 32px;font-size:52px;color:#fff">
   /PARETO<span style="display:inline-block;width:4px;height:52px;background:#ffd60a;vertical-align:-8px;margin-left:6px"></span></div>
  <div style="display:flex;flex-wrap:wrap;gap:18px;margin-top:34px">
   %s
  </div>
 </div>
</div>
<div class="cap">Comandos secretos do ChatGPT?<br><b>Não existem.</b></div>
""" % "".join(
    f'<span class="mono" style="font-size:38px;padding:14px 24px;border-radius:16px;background:#2a1316;color:#fca5a5;'
    f'text-decoration:line-through;text-decoration-thickness:4px;border:2px solid #7f1d1d">{c}</span>'
    for c in ["/ISHIKAWA", "/anatomy", "/5whY", "/explodedview", "/zerogravity"])),

"s2": ("""
<div class="tag y">É SÓ TEXTO</div>
<div class="stage" style="display:flex;flex-direction:column;align-items:center;gap:0">
 <div class="card mono" style="padding:30px 60px;font-size:54px;color:#fff">"/PARETO"</div>
 <div style="width:6px;height:80px;background:#4b5565"></div>
 <div class="card" style="padding:30px 50px;font-size:44px;text-align:center;border-color:#3b82f6">
  <div style="font-weight:800">Modelo</div><div style="font-size:30px;color:#8b97a8;margin-top:6px">lê como uma palavra qualquer</div></div>
 <div style="width:6px;height:80px;background:#4b5565"></div>
 <div class="card" style="padding:30px 50px;font-size:44px;text-align:center;border:3px dashed #ffd60a;background:#1d1a0b">
  <div style="font-weight:800;color:#ffd60a">Adivinha a intenção</div>
  <div style="font-size:30px;color:#c9b77a;margin-top:6px">"acho que ele quer um Pareto..."</div></div>
</div>
<div class="cap">Não tem atalho escondido.<br>A barra é só texto. Ele <b>adivinha.</b></div>
"""),

"s3": ("""
<div class="tag r">POR ISSO FALHA</div>
<div class="stage" style="display:flex;flex-direction:column;gap:36px">
 <div class="card" style="padding:34px 40px">
  <div style="font-size:30px;color:#8b97a8;margin-bottom:16px">Tentativa 1 · /PARETO</div>
  <div class="mono" style="font-size:32px;line-height:1.6;color:#d1d9e4">| Causa | % | Acum. |<br>| Atraso | 42 | 42 |<br>| Erro &nbsp;| 31 | 73 |</div>
 </div>
 <div class="card" style="padding:34px 40px;border-color:#7f1d1d">
  <div style="font-size:30px;color:#fca5a5;margin-bottom:16px">Tentativa 2 · /PARETO</div>
  <div style="font-size:34px;line-height:1.5;color:#d1d9e4">Claro! O Princípio de Pareto diz que 80% dos efeitos vêm de 20% das causas. Ele foi criado por...</div>
 </div>
</div>
<div class="cap">Mesmo "comando".<br>Cada vez um <b>formato diferente.</b></div>
"""),

"s4": ("""
<div class="tag g">O QUE FUNCIONA</div>
<div class="stage">
 <div class="card">
  <div style="display:flex;align-items:center;gap:14px;padding:24px 30px;border-bottom:2px solid #263040">
   <span style="width:20px;height:20px;border-radius:50%;background:#ef4444"></span>
   <span style="width:20px;height:20px;border-radius:50%;background:#f59e0b"></span>
   <span style="width:20px;height:20px;border-radius:50%;background:#22c55e"></span>
   <span style="margin-left:auto;font-size:28px;color:#8b97a8">prompt.txt</span></div>
  <div class="mono" style="padding:36px 38px;font-size:34px;line-height:1.75;color:#d1d9e4">
   {{LINES}}
  </div>
 </div>
</div>
<div class="cap">Papel, tarefa, formato<br>e de onde tirar a <b>fonte.</b></div>
""".replace("{{LINES}}", "<br>".join(
    f'<span style="color:{c};font-weight:700">{k}:</span> {v}' for k, v, c in [
        ("PAPEL", "analista de qualidade", "#60a5fa"),
        ("TAREFA", "análise de Pareto", "#c084fc"),
        ("FORMATO", "tabela: causa | % | acum.", "#ffd60a"),
        ("FONTE", "só os dados abaixo;", "#22c55e"),
        ("", "se faltar, diga que falta", "#22c55e"),
    ]).replace('<span style="color:#22c55e;font-weight:700">:</span>', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'))),

"s5": ("""
<div class="tag g">COMENTA "FONTE"</div>
<div class="stage" style="display:flex;flex-direction:column;gap:40px">
 <div class="card" style="padding:36px 40px;display:flex;gap:26px;align-items:center">
  <div style="width:96px;height:96px;border-radius:50%;background:#3b82f6;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:48px;flex:none">@</div>
  <div><div style="font-size:30px;color:#8b97a8">comentou agora</div><div style="font-size:64px;font-weight:900;color:#fff;letter-spacing:1px">FONTE</div></div>
 </div>
 <div class="card" style="padding:36px 40px;border-color:#22c55e">
  <div style="font-size:30px;color:#86efac;margin-bottom:14px">@gf.code · mensagem direta</div>
  <div style="font-size:40px;line-height:1.4">Aqui está o seu <b style="color:#22c55e">Checklist FONTE</b> pra montar prompts que não inventam.</div>
 </div>
</div>
<div class="cap">Comenta <b>FONTE</b> e recebe<br>o checklist completo.</div>
"""),
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
