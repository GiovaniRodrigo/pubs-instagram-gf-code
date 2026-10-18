import asyncio, os
from playwright.async_api import async_playwright

OUT = os.path.dirname(os.path.abspath(__file__))

SLIDES = [
    {"kind": "cover",
     "title": "Você faz o marketing de <em>4 pessoas</em> sozinho?",
     "sub": "Abri 20 vagas para quem quer parar de se afogar."},
    {"kind": "text",
     "title": "Post, story, anúncio, <span style='white-space:nowrap'>e&#8209;mail</span>, relatório.",
     "body": "Tudo com você.",
     "quote": "E no fim do mês ainda ouve: <b>“mas o que o marketing trouxe?”</b>"},
    {"kind": "text",
     "title": "Por isso criei o <em>Solo Marketer OS</em>.",
     "body": "Você conta o que a empresa faz.<br>Ele entrega um <b>plano de 30 dias</b> e as postagens prontas para você aprovar."},
    {"kind": "text",
     "title": "E o relatório que o seu chefe entende:",
     "big": "o retorno do marketing em <em>uma página</em>.",
     "body": "Sem planilha montada à mão."},
    {"kind": "offer",
     "kicker": "Membros Fundadores",
     "title": "Só <em>20 vagas</em>.",
     "body": "Até 50% de desconto, para sempre.",
     "old": "R$ 197", "new": "R$ 118", "per": "por mês no plano Pro"},
    {"kind": "list",
     "title": "Em troca, eu peço duas coisas:",
     "items": ["Sua opinião a cada 15 dias", "Um depoimento depois de 30 dias de uso"]},
    {"kind": "cta",
     "title": "Comente",
     "word": "PLANO",
     "body": "Eu te mando o acesso por mensagem,<br>com <b>7 dias grátis</b>."},
]

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{background:#0B0F1A;color:#F4F5F7;font-family:'Inter',sans-serif;position:relative;overflow:hidden}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;filter:blur(140px);opacity:.35;background:#6C5CE7;right:-380px;top:-380px}
.glow2{position:absolute;width:700px;height:700px;border-radius:50%;filter:blur(160px);opacity:.18;background:#00D68F;left:-320px;bottom:-320px}
.wrap{position:absolute;inset:0;padding:110px 96px;display:flex;flex-direction:column;justify-content:center}
.top{position:absolute;top:64px;left:96px;right:96px;display:flex;justify-content:space-between;font:600 30px 'Inter';color:#9AA0B4;letter-spacing:.5px}
.brand b{color:#F4F5F7}
.bottom{position:absolute;bottom:64px;left:96px;right:96px;display:flex;justify-content:space-between;align-items:center;font:500 28px 'Inter';color:#9AA0B4}
.dots{display:flex;gap:12px}.dots i{width:14px;height:14px;border-radius:50%;background:#2A3044}.dots i.on{background:#00D68F;width:40px;border-radius:8px}
h1{font-family:'Poppins';font-weight:700;font-size:96px;line-height:1.08;letter-spacing:-1.5px}
h2{font-family:'Poppins';font-weight:700;font-size:76px;line-height:1.12;letter-spacing:-1px}
em{font-style:normal;color:#00D68F}
p{font-size:46px;line-height:1.4;color:#C9CDDA;margin-top:44px}
p b{color:#F4F5F7}
.quote{margin-top:60px;padding:40px 44px;border-left:8px solid #6C5CE7;background:rgba(108,92,231,.12);border-radius:0 20px 20px 0;font-size:46px;line-height:1.4;color:#C9CDDA}
.quote b{color:#F4F5F7}
.big{font-family:'Poppins';font-weight:700;font-size:92px;line-height:1.1;margin-top:40px;letter-spacing:-1.5px}
.kicker{display:inline-block;align-self:flex-start;font:700 32px 'Inter';text-transform:uppercase;letter-spacing:4px;color:#0B0F1A;background:#00D68F;padding:14px 28px;border-radius:12px;margin-bottom:44px}
.price{margin-top:70px;display:flex;align-items:baseline;gap:36px}
.old{font:600 56px 'Poppins';color:#6B7189;text-decoration:line-through}
.new{font:700 150px 'Poppins';color:#F4F5F7;letter-spacing:-3px}
.per{font-size:40px;color:#9AA0B4;margin-top:8px}
ul{list-style:none;margin-top:70px}
li{display:flex;gap:32px;align-items:center;font-size:52px;line-height:1.3;margin-bottom:46px;color:#F4F5F7}
li span{flex:none;width:84px;height:84px;border-radius:22px;background:#00D68F;color:#0B0F1A;font:700 46px 'Poppins';display:flex;align-items:center;justify-content:center}
.word{margin:30px 0 10px;font:800 210px 'Poppins';letter-spacing:6px;color:#00D68F;line-height:1}
.arrow{font-size:110px;margin-top:20px}
.swipe{color:#00D68F;font-weight:700}
"""

def body(s):
    k = s["kind"]
    if k == "cover":
        return f"<h1>{s['title']}</h1><p>{s['sub']}</p>"
    if k == "text":
        h = f"<h2>{s['title']}</h2>"
        if "big" in s: h += f"<div class='big'>{s['big']}</div>"
        if "body" in s: h += f"<p>{s['body']}</p>"
        if "quote" in s: h += f"<div class='quote'>{s['quote']}</div>"
        return h
    if k == "offer":
        return (f"<span class='kicker'>{s['kicker']}</span><h1>{s['title']}</h1><p>{s['body']}</p>"
                f"<div class='price'><span class='old'>{s['old']}</span><span class='new'>{s['new']}</span></div>"
                f"<div class='per'>{s['per']}</div>")
    if k == "list":
        items = "".join(f"<li><span>{i+1}</span>{t}</li>" for i, t in enumerate(s["items"]))
        return f"<h2>{s['title']}</h2><ul>{items}</ul>"
    if k == "cta":
        return f"<h2>{s['title']}</h2><div class='word'>{s['word']}</div><p>{s['body']}</p><div class='arrow'>👇</div>"

def page(i, s):
    n = len(SLIDES)
    dots = "".join(f"<i class='{'on' if j == i else ''}'></i>" for j in range(n))
    right = "<span class='swipe'>arraste →</span>" if i < n - 1 else "<span>solomarketeros.gfcode.com.br</span>"
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>
<body><div class='glow'></div><div class='glow2'></div>
<div class='top'><span class='brand'><b>gf.code</b></span><span>{i+1}/{n}</span></div>
<div class='wrap'>{body(s)}</div>
<div class='bottom'><div class='dots'>{dots}</div>{right}</div>
</body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(SLIDES):
            await pg.set_content(page(i, s))
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=os.path.join(OUT, f"slide_{i+1:02d}.jpg"), type="jpeg", quality=92)
        await b.close()

asyncio.run(main())
