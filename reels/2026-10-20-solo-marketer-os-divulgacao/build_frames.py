import math, os, sys
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
OUT = sys.argv[1]
FD = "/usr/share/fonts/truetype/google-fonts/"
def F(w, s): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)

SKY = (14, 165, 233); SKY2 = (56, 189, 248); WHITE = (241, 245, 249)
MUTED = (148, 163, 184); CARD = (17, 27, 45); LINE = (37, 52, 78)
RED = (248, 113, 113); GREEN = (52, 211, 153)

def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease(p): p = clamp(p); return 1 - (1 - p) ** 3
def appear(t, s, d=0.55): return ease((t - s) / d)

# ---------- background ----------
def make_bg():
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(6 + 6 * k), int(10 + 8 * k), int(20 + 18 * k)))
    return bg.convert("RGBA")
BG = make_bg()
def make_glow(color, r):
    g = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([r * .3, r * .3, r * 1.7, r * 1.7], fill=color + (95,))
    return g.filter(ImageFilter.GaussianBlur(r * 0.32))
GLOW1 = make_glow(SKY, 520); GLOW2 = make_glow((99, 102, 241), 440)
GRID = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(GRID)
for x in range(0, W, 90): gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 9))
for y in range(0, H, 90): gd.line([(0, y), (W, y)], fill=(255, 255, 255, 9))

def background(T):
    img = BG.copy()
    img.alpha_composite(GRID)
    x1 = int(-260 + 160 * math.sin(T * 0.35)); y1 = int(150 + 220 * math.sin(T * 0.22))
    x2 = int(420 + 140 * math.cos(T * 0.3)); y2 = int(1150 + 200 * math.cos(T * 0.25))
    img.alpha_composite(GLOW1, (x1, y1)); img.alpha_composite(GLOW2, (x2, y2))
    return img

# ---------- drawing helpers ----------
def layer(img, alpha, fn):
    if alpha <= 0.01: return
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn(ImageDraw.Draw(L))
    bb = L.getbbox()
    if not bb: return
    L = L.crop(bb)
    if alpha < 0.999:
        a = L.getchannel("A").point(lambda v: int(v * alpha)); L.putalpha(a)
    img.alpha_composite(L, (bb[0], bb[1]))

def ctext(d, y, s, font, fill, x=None):
    tw = d.textlength(s, font=font)
    d.text(((W - tw) / 2 if x is None else x, y), s, font=font, fill=fill)
    return tw

def el(img, t, start, sa, fn, dy=50, d=0.55):
    p = appear(t, start, d)
    layer(img, p * sa, lambda dr: fn(dr, (1 - p) * dy))

def pill(d, cx, y, s, font, fg, bg, padx=34, h=72, outline=None):
    tw = d.textlength(s, font=font)
    x0 = cx - tw / 2 - padx
    d.rounded_rectangle([x0, y, cx + tw / 2 + padx, y + h], radius=h / 2, fill=bg, outline=outline, width=2)
    bb = font.getbbox(s)
    d.text((cx - tw / 2, y + (h - (bb[3] + bb[1])) / 2), s, font=font, fill=fg)

# ---------- scenes ----------
def s_hook(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: pill(d, W / 2, 640 + o, "PARA O MARQUETEIRO SOLO", F("Medium", 30), SKY2, (14, 165, 233, 40), outline=(14, 165, 233, 120)))
    f = F("Bold", 96)
    el(img, t, 0.25, sa, lambda d, o: ctext(d, 780 + o, "Você faz o trabalho", f, WHITE))
    el(img, t, 0.5, sa, lambda d, o: ctext(d, 900 + o, "de um time inteiro.", f, WHITE))
    el(img, t, 1.2, sa, lambda d, o: ctext(d, 1060 + o, "Sozinho.", F("Bold", 120), SKY2), dy=0, d=0.35)

def s_chaos(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 420 + o, "SEGUNDA-FEIRA, 8h47", F("Medium", 34), SKY2))
    el(img, t, 0.15, sa, lambda d, o: ctext(d, 480 + o, "Três incêndios", F("Bold", 84), WHITE))
    el(img, t, 0.3, sa, lambda d, o: ctext(d, 585 + o, "antes do café.", F("Bold", 84), WHITE))
    items = [("Anúncios queimando verba", "Placements lixo e bots"),
             ("Cold e-mail travado", "Respostas abaixo de 1%"),
             ("Redes sem calendário", "Post no improviso"),
             ("Relatório às 23h", "Planilha atrás de planilha")]
    for i, (a, b) in enumerate(items):
        st = 0.7 + i * 0.45
        def draw(d, o, i=i, a=a, b=b, st=st):
            jit = 6 * math.sin((t - st) * 22 + i) * clamp(1.2 - (t - st))
            x0, y0 = 110 + jit + (i % 2) * 30, 790 + i * 175 + o
            d.rounded_rectangle([x0, y0, x0 + 830, y0 + 145], 28, fill=CARD + (235,), outline=LINE, width=2)
            d.ellipse([x0 + 34, y0 + 42, x0 + 94, y0 + 102], fill=(248, 113, 113, 45), outline=RED, width=3)
            d.text((x0 + 56, y0 + 44), "!", font=F("Bold", 40), fill=RED)
            d.text((x0 + 125, y0 + 26), a, font=F("SemiBold" if False else "Bold", 40), fill=WHITE)
            d.text((x0 + 125, y0 + 82), b, font=F("Regular", 30), fill=MUTED)
        el(img, t, st, sa, draw, dy=70, d=0.4)

def s_ceo(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 520 + o, "11h20. Mensagem do CEO:", F("Medium", 38), MUTED))
    msg = ["Quanto o marketing", "deu de retorno", "este mês?"]
    full = " ".join(msg); n = int(clamp((t - 0.5) / 1.3) * len(full))
    def bubble(d, o):
        x0, y0 = 120, 640 + o
        d.rounded_rectangle([x0, y0, x0 + 840, y0 + 400], 44, fill=(255, 255, 255, 245))
        d.polygon([(x0 + 60, y0 + 400), (x0 + 60, y0 + 460), (x0 + 130, y0 + 400)], fill=(255, 255, 255, 245))
        d.ellipse([x0 + 40, y0 + 40, x0 + 110, y0 + 110], fill=SKY)
        d.text((x0 + 51, y0 + 58), "CEO", font=F("Bold", 21), fill=(255, 255, 255))
        d.text((x0 + 130, y0 + 55), "Diretoria", font=F("Bold", 32), fill=(15, 23, 42))
        k = n
        for i, line in enumerate(msg):
            part = line[:max(0, k)]; k -= len(line) + 1
            d.text((x0 + 45, y0 + 145 + i * 74), part, font=F("Bold", 60), fill=(15, 23, 42))
    el(img, t, 0.2, sa, bubble, dy=60)
    el(img, t, 2.1, sa, lambda d, o: ctext(d, 1170 + o, "Você trabalhou muito.", F("Medium", 46), WHITE))
    el(img, t, 2.35, sa, lambda d, o: ctext(d, 1235 + o, "Provar em números é outra história.", F("Medium", 46), SKY2))

def wordmark(d, cx, y, size, alpha_fill=255):
    f = F("Bold", size)
    a, b = "Solo Marketer ", "OS"
    wa, wb = d.textlength(a, font=f), d.textlength(b, font=f)
    x = cx - (wa + wb) / 2
    d.text((x, y), a, font=f, fill=WHITE + (alpha_fill,)); d.text((x + wa, y), b, font=f, fill=SKY2 + (alpha_fill,))

def s_reveal(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 640 + o, "Por isso eu desenvolvi o", F("Medium", 46), MUTED))
    def logo(d, o):
        s = 200
        x0, y0 = W / 2 - s / 2, 730 + o
        d.rounded_rectangle([x0, y0, x0 + s, y0 + s], 52, fill=SKY)
        d.text((x0 + 32, y0 + 40), "OS", font=F("Bold", 100), fill=(255, 255, 255))
    el(img, t, 0.35, sa, logo, dy=0, d=0.5)
    el(img, t, 0.7, sa, lambda d, o: wordmark(d, W / 2, 970 + o, 104))
    el(img, t, 1.1, sa, lambda d, o: ctext(d, 1125 + o, "O sistema operacional autônomo", F("Regular", 42), WHITE))
    el(img, t, 1.25, sa, lambda d, o: ctext(d, 1180 + o, "para quem faz marketing sozinho.", F("Regular", 42), WHITE))
    for i, w in enumerate(["Autônomo", "Calibrado", "Mensurável"]):
        cx = W / 2 + (i - 1) * 300
        el(img, t, 1.7 + i * 0.18, sa, lambda d, o, w=w, cx=cx: pill(d, cx, 1300 + o, w, F("Medium", 32), WHITE, CARD + (230,), padx=30, h=70, outline=LINE))

def s_steps(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 360 + o, "DO CAOS AO RESULTADO", F("Medium", 34), SKY2))
    el(img, t, 0.15, sa, lambda d, o: ctext(d, 415 + o, "Três passos.", F("Bold", 88), WHITE))
    el(img, t, 0.3, sa, lambda d, o: ctext(d, 520 + o, "Zero planilha.", F("Bold", 88), MUTED))
    steps = [("Diga o que você vende", ["Empresa, o que resolve e nicho.", "Só três campos."]),
             ("Receba a esteira pronta", ["Copy calibrada numa dor real para", "Meta, LinkedIn, e-mail, Reels e LP."]),
             ("Prove o ROI ao CEO", ["Relatório de 1 página.", "Sem métrica de vaidade."])]
    for i, (h, sub) in enumerate(steps):
        st = 0.9 + i * 1.5
        def draw(d, o, i=i, h=h, sub=sub):
            x0, y0 = 90, 720 + i * 255 + o
            d.rounded_rectangle([x0, y0, x0 + 900, y0 + 220], 32, fill=CARD + (240,), outline=LINE, width=2)
            d.ellipse([x0 + 40, y0 + 55, x0 + 140, y0 + 155], fill=SKY)
            n = str(i + 1); f = F("Bold", 52); tw = d.textlength(n, font=f)
            d.text((x0 + 90 - tw / 2, y0 + 68), n, font=f, fill=(255, 255, 255))
            d.text((x0 + 175, y0 + 32), h, font=F("Bold", 44), fill=WHITE)
            for j, s in enumerate(sub):
                d.text((x0 + 175, y0 + 100 + j * 46), s, font=F("Regular", 31), fill=MUTED)
        el(img, t, st, sa, draw, dy=80)
        # highlight current step
    k = int(clamp((t - 0.9) / 1.5, 0, 2.99))
    def ring(d):
        x0, y0 = 90, 720 + k * 255
        d.rounded_rectangle([x0 - 3, y0 - 3, x0 + 903, y0 + 223], 34, outline=SKY + (220,), width=4)
    layer(img, sa * appear(t, 0.9), ring)

def fmt_brl(v): return "R$ " + f"{int(v):,}".replace(",", ".")

def s_report(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 400 + o, "16h30. A resposta ao CEO:", F("Medium", 38), MUTED))
    el(img, t, 0.15, sa, lambda d, o: ctext(d, 460 + o, "Relatório do CEO", F("Bold", 92), WHITE))
    p = ease((t - 0.8) / 1.6)
    tiles = [("Faturamento bruto", fmt_brl(30000 * p), WHITE),
             ("Investimento total", fmt_brl(5000 * p), WHITE),
             ("Lucro líquido", fmt_brl(25000 * p), GREEN),
             ("ROAS", f"{6.0 * p:.1f}x".replace(".", ","), SKY2)]
    for i, (lab, val, col) in enumerate(tiles):
        def draw(d, o, i=i, lab=lab, val=val, col=col):
            x0 = 90 + (i % 2) * 465; y0 = 640 + (i // 2) * 290 + o
            d.rounded_rectangle([x0, y0, x0 + 435, y0 + 260], 30, fill=CARD + (240,), outline=LINE, width=2)
            d.text((x0 + 36, y0 + 40), lab, font=F("Medium", 32), fill=MUTED)
            d.text((x0 + 36, y0 + 110), val, font=F("Bold", 66 if i < 3 else 80), fill=col)
        el(img, t, 0.5 + i * 0.12, sa, draw, dy=60)
    el(img, t, 1.0, sa, lambda d, o: ctext(d, 1235 + o, "Exemplo ilustrativo", F("Regular", 26), (100, 116, 139)))
    el(img, t, 2.5, sa, lambda d, o: ctext(d, 1310 + o, "Só o que paga as contas:", F("Medium", 42), WHITE))
    el(img, t, 2.7, sa, lambda d, o: ctext(d, 1368 + o, "faturamento, lucro, CAC e ROAS.", F("Medium", 42), SKY2))

def s_integr(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 420 + o, "INTEGRAÇÕES", F("Medium", 34), SKY2))
    el(img, t, 0.12, sa, lambda d, o: ctext(d, 475 + o, "Conecta com o que", F("Bold", 84), WHITE))
    el(img, t, 0.25, sa, lambda d, o: ctext(d, 575 + o, "você já usa.", F("Bold", 84), WHITE))
    rows = [["Meta Ads", "Google Ads", "LinkedIn Ads"], ["TikTok Ads", "HubSpot", "Pipedrive"],
            ["Salesforce", "Hotmart", "Kiwify"], ["Shopify", "VTEX", "GA4"], ["ActiveCampaign", "Omie", "Conta Azul"]]
    f = F("Medium", 34); k = 0
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for r, row in enumerate(rows):
        widths = [probe.textlength(s, font=f) + 64 for s in row]
        gap = 22; total = sum(widths) + gap * (len(row) - 1); x = (W - total) / 2
        for s, w in zip(row, widths):
            cx = x + w / 2
            el(img, t, 0.6 + k * 0.09, sa, lambda d, o, s=s, cx=cx, r=r: pill(d, cx, 760 + r * 110 + o, s, f, WHITE, CARD + (240,), padx=32, h=82, outline=LINE), dy=40, d=0.4)
            x += w + gap; k += 1
    el(img, t, 2.2, sa, lambda d, o: ctext(d, 1340 + o, "Ou planilha e números digitados.", F("Regular", 38), MUTED))

def s_plans(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 330 + o, "Planos que crescem com você", F("Bold", 62), WHITE))
    plans = [("Essencial", "97", "Automação, integrações e relatório de ROI", False),
             ("Pro", "197", "Assistente de IA que vê a tela e age por você", True),
             ("Max", "397", "Tudo do Pro + imagens e vídeos com IA", False)]
    for i, (n, p, desc, rec) in enumerate(plans):
        def draw(d, o, i=i, n=n, p=p, desc=desc, rec=rec):
            x0, y0 = 90, 480 + i * 300 + o
            d.rounded_rectangle([x0, y0, x0 + 900, y0 + 265], 32, fill=(14, 40, 66, 245) if rec else CARD + (240,),
                                outline=SKY if rec else LINE, width=4 if rec else 2)
            d.text((x0 + 44, y0 + 36), n, font=F("Bold", 54), fill=WHITE)
            if rec:
                pill(d, x0 + 44 + d.textlength(n, font=F("Bold", 54)) + 140, y0 + 46, "Recomendado", F("Medium", 26), (255, 255, 255), SKY, padx=24, h=52)
            fp = F("Bold", 58); pr = "R$ " + p
            pw = d.textlength(pr, font=fp)
            d.text((x0 + 856 - pw - 120, y0 + 32), pr, font=fp, fill=SKY2)
            d.text((x0 + 856 - 112, y0 + 58), "/mês", font=F("Regular", 30), fill=MUTED)
            d.text((x0 + 44, y0 + 140), desc, font=F("Regular", 32), fill=MUTED)
            d.line([(x0 + 44, y0 + 120), (x0 + 856, y0 + 120)], fill=LINE, width=2)
        el(img, t, 0.4 + i * 0.35, sa, draw, dy=70)
    el(img, t, 1.8, sa, lambda d, o: ctext(d, 1420 + o, "Cada plano inclui o anterior.", F("Medium", 38), WHITE))

def s_cta(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: wordmark(d, W / 2, 470 + o, 70))
    el(img, t, 0.3, sa, lambda d, o: ctext(d, 640 + o, "7 dias grátis.", F("Bold", 120), WHITE))
    el(img, t, 0.55, sa, lambda d, o: ctext(d, 800 + o, "Sem cartão. Cancele quando quiser.", F("Medium", 44), MUTED))
    pulse = 1 + 0.03 * math.sin(max(0, t - 1.2) * 5)
    def btn(d, o):
        w, h = 880 * pulse, 130 * pulse
        x0, y0 = W / 2 - w / 2, 960 + o
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h / 2, fill=SKY)
        ctext(d, y0 + h / 2 - 34, "Começar teste grátis", F("Bold", 50), (255, 255, 255))
    el(img, t, 0.9, sa, btn, dy=40)
    el(img, t, 1.2, sa, lambda d, o: ctext(d, 1135 + o, "solomarketeros.gfcode.com.br", F("Bold", 50), SKY2))
    el(img, t, 1.8, sa, lambda d, o: ctext(d, 1330 + o, "Menos operação. Mais crescimento mensurável.", F("Regular", 34), WHITE))
    el(img, t, 2.3, sa, lambda d, o: ctext(d, 1440 + o, "Desenvolvido por Giovani · GF Code  @gf.code", F("Medium", 30), MUTED))

SCENES = [(0.0, 3.4, s_hook), (3.4, 7.6, s_chaos), (7.6, 11.4, s_ceo), (11.4, 14.8, s_reveal),
          (14.8, 21.4, s_steps), (21.4, 26.2, s_report), (26.2, 29.8, s_integr), (29.8, 33.8, s_plans), (33.8, 39.0, s_cta)]
DUR = SCENES[-1][1]

def frame(i):
    T = i / FPS
    img = background(T)
    for (a, b, fn) in SCENES:
        if a - 0.01 <= T < b + 0.35:
            t = T - a
            sa = clamp(t / 0.3) * (1 if fn is s_cta else clamp((b - T) / 0.35 + 0.0001))
            if T >= b: sa = 0
            fn(img, t, sa)
    if T > 14.8 and T < 33.8:
        a = clamp((T - 14.8) / 0.5) * clamp((33.8 - T) / 0.4)
        layer(img, a, lambda d: wordmark(d, W / 2, 150, 40))
    # progress bar
    layer(img, 1, lambda d: d.rectangle([0, 0, W * T / DUR, 8], fill=SKY + (230,)))
    img.convert("RGB").save(f"{OUT}/f{i:05d}.jpg", quality=92)
    return i

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    n = int(DUR * FPS)
    if len(sys.argv) > 2:
        for s in sys.argv[2].split(","): frame(int(s))
    else:
        with Pool(2) as p:
            for _ in p.imap_unordered(frame, range(n), chunksize=8): pass
    print("frames", n, "dur", DUR)
