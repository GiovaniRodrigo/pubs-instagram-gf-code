"""Render the 7 scene frames (1080x1920) for the GF Code reel 'Chatbot x Agente de IA'."""
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
 font-family:'Inter Display',Inter;font-weight:900;font-size:76px;line-height:.98;letter-spacing:-2px;text-align:center;
 color:#0a0d12;white-space:nowrap}
.y{background:#ffd60a}.g{background:#22c55e}.b{background:#60a5fa}.r{background:#ef4444;color:#fff}.c{background:#06e5f8}
.stage{position:absolute;top:470px;left:80px;right:80px}
.cap{position:absolute;top:1430px;left:90px;right:90px;text-align:center;font-family:'Inter Display',Inter;
 font-weight:800;font-size:54px;line-height:1.2;letter-spacing:-.5px}
.cap b{color:#ffd60a}
.card{background:#161b24;border:2px solid #263040;border-radius:30px;padding:30px 34px}
.lbl{font-size:26px;color:#8b97a8;margin-bottom:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase}
.bub{border-radius:22px;padding:20px 24px;font-size:34px;line-height:1.35;margin-top:14px}
.u{background:#263040;margin-left:120px}
.bot{background:#1e2533;margin-right:80px}
.step{display:flex;gap:20px;align-items:center;font-size:34px;padding:16px 0;border-bottom:1px solid #263040}
.step:last-child{border-bottom:0}
.ic{width:62px;height:62px;border-radius:16px;flex:none;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:900;color:#0a0d12}
.ok{color:#22c55e;font-weight:900;margin-left:auto}
"""

SCENES = {
"s1": """
<div class="tag r">NÃO É A MESMA COISA</div>
<div class="stage" style="top:560px;display:flex;gap:30px;justify-content:center;align-items:center">
 <div class="card" style="flex:1;text-align:center;padding:60px 20px">
  <div style="font-size:120px">💬</div><div style="font-size:52px;font-weight:900;margin-top:20px">Chatbot</div></div>
 <div style="font-size:90px;font-weight:900;color:#ef4444">≠</div>
 <div class="card" style="flex:1;text-align:center;padding:60px 20px;border-color:#06e5f8">
  <div style="font-size:120px">🤖</div><div style="font-size:52px;font-weight:900;margin-top:20px;color:#06e5f8">Agente</div></div>
</div>
<div class="cap">Chatbot e agente de IA<br><b>não</b> são a mesma coisa.</div>
""",

"s2": """
<div class="tag b">CHATBOT RESPONDE</div>
<div class="stage">
 <div class="card">
  <div class="lbl">💬 Chatbot</div>
  <div class="bub u">Qual o prazo de entrega?</div>
  <div class="bub bot">Entregas levam até 7 dias úteis após a confirmação do pagamento.</div>
  <div style="margin-top:30px;font-size:30px;color:#8b97a8;text-align:center">— fim da conversa —</div>
 </div>
</div>
<div class="cap">Você pergunta, ele explica.<br><b>E para por aí.</b></div>
""",

"s3": """
<div class="tag c">AGENTE EXECUTA</div>
<div class="stage">
 <div class="card" style="border-color:#06e5f8">
  <div class="lbl" style="color:#06e5f8">🤖 Agente · objetivo</div>
  <div style="font-size:40px;font-weight:800;margin-bottom:24px">“Resolver o pedido atrasado”</div>
  <div class="step"><div class="ic" style="background:#06e5f8">1</div>Decide os passos</div>
  <div class="step"><div class="ic" style="background:#06e5f8">2</div>Usa as ferramentas da empresa</div>
  <div class="step"><div class="ic" style="background:#06e5f8">3</div>Entrega o resultado</div>
 </div>
</div>
<div class="cap">Recebe um <b>objetivo</b>,<br>decide os passos e age.</div>
""",

"s4": """
<div class="tag y">PEDIDO ATRASADO</div>
<div class="stage">
 <div class="card" style="margin-bottom:26px">
  <div class="lbl">💬 Chatbot</div>
  <div style="font-size:34px;line-height:1.4">“Nossa política prevê até 7 dias úteis…”</div>
 </div>
 <div class="card" style="border-color:#06e5f8">
  <div class="lbl" style="color:#06e5f8">🤖 Agente</div>
  <div class="step"><div class="ic" style="background:#60a5fa">🔎</div>Consulta o pedido no sistema<span class="ok">✓</span></div>
  <div class="step"><div class="ic" style="background:#ffd60a">🚚</div>Verifica a transportadora<span class="ok">✓</span></div>
  <div class="step"><div class="ic" style="background:#f59e0b">🎫</div>Abre o chamado<span class="ok">✓</span></div>
  <div class="step"><div class="ic" style="background:#22c55e">✉</div>Avisa o cliente<span class="ok">✓</span></div>
 </div>
</div>
<div class="cap">Um <b>explica</b>.<br>O outro <b>resolve</b>.</div>
""",

"s5": """
<div class="tag r">AGENTE SEM LIMITE = RISCO</div>
<div class="stage" style="display:flex;flex-direction:column;gap:24px">
 <div class="card" style="display:flex;gap:24px;align-items:center"><div class="ic" style="background:#ffd60a;width:80px;height:80px;font-size:40px">📏</div>
  <div><div style="font-size:40px;font-weight:800">Regras claras</div><div style="font-size:28px;color:#8b97a8">o que pode e o que não pode fazer</div></div></div>
 <div class="card" style="display:flex;gap:24px;align-items:center"><div class="ic" style="background:#60a5fa;width:80px;height:80px;font-size:40px">📄</div>
  <div><div style="font-size:40px;font-weight:800">Fonte confiável</div><div style="font-size:28px;color:#8b97a8">dados e documentos da empresa</div></div></div>
 <div class="card" style="display:flex;gap:24px;align-items:center"><div class="ic" style="background:#22c55e;width:80px;height:80px;font-size:40px">🙋</div>
  <div><div style="font-size:40px;font-weight:800">Humano aprova</div><div style="font-size:28px;color:#8b97a8">tudo que for crítico</div></div></div>
</div>
<div class="cap">Autonomia <b>com controle</b>.</div>
""",

"s6": """
<div class="tag g">REGRA PRÁTICA</div>
<div class="stage" style="top:560px;display:flex;flex-direction:column;gap:34px">
 <div class="card" style="padding:44px;display:flex;justify-content:space-between;align-items:center">
  <div style="font-size:30px;color:#8b97a8">A tarefa é<br><span style="font-size:58px;font-weight:900;color:#fff">RESPONDER?</span></div>
  <div style="font-size:52px;font-weight:900">💬 Chatbot</div></div>
 <div class="card" style="padding:44px;display:flex;justify-content:space-between;align-items:center;border-color:#06e5f8">
  <div style="font-size:30px;color:#8b97a8">A tarefa é<br><span style="font-size:58px;font-weight:900;color:#fff">EXECUTAR?</span></div>
  <div style="font-size:52px;font-weight:900;color:#06e5f8">🤖 Agente</div></div>
</div>
<div class="cap">Responder: <b>chatbot</b>.<br>Executar: <b>agente</b>.</div>
""",

"s7": """
<div class="tag y">SALVA PRA LEMBRAR</div>
<div class="stage" style="top:600px">
 <div class="card" style="padding:40px;display:flex;gap:30px;align-items:center;border-color:#06e5f8">
  <div style="width:120px;height:120px;border-radius:50%;background:#12202f;border:4px solid #06e5f8;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:50px;color:#06e5f8;flex:none">GF</div>
  <div><div style="font-size:32px;color:#8be9f5">segue pra mais IA aplicada</div><div style="font-size:72px;font-weight:900;color:#fff">@gf.code</div></div>
 </div>
</div>
<div class="cap">Salva esse vídeo<br>e segue a <b>GF Code</b>.</div>
""",
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    for name, body in SCENES.items():
        page.set_content(f"<html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head><body>{body}</body></html>")
        page.wait_for_timeout(200)
        page.screenshot(path=str(OUT / f"{name}.png"))
        print("rendered", name)
    browser.close()
