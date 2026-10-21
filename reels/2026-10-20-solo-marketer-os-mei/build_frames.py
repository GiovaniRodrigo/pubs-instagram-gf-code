import sys, os, math
OUTDIR = sys.argv[1]
sys.argv = [sys.argv[0], OUTDIR] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(__file__))
import render as R
from render import *  # noqa
from multiprocessing import Pool

AMBER = (251, 191, 36)

def s_hook(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: pill(d, W/2, 600+o, "MEI E MICROEMPREENDEDOR", F("Medium", 30), SKY2, (14,165,233,40), outline=(14,165,233,120)))
    f = F("Bold", 92)
    el(img, t, 0.25, sa, lambda d, o: ctext(d, 740+o, "Quanto tempo você", f, WHITE))
    el(img, t, 0.45, sa, lambda d, o: ctext(d, 855+o, "perde pensando no", f, WHITE))
    el(img, t, 0.65, sa, lambda d, o: ctext(d, 970+o, "que postar?", f, SKY2))

def s_pain(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 430+o, "TODO MÊS A MESMA COISA", F("Medium", 34), SKY2))
    el(img, t, 0.15, sa, lambda d, o: ctext(d, 490+o, "Você atende, vende,", F("Bold", 76), WHITE))
    el(img, t, 0.3, sa, lambda d, o: ctext(d, 585+o, "entrega... e o Instagram?", F("Bold", 76), WHITE))
    items = [("Sem ideia do que postar", "Trava na frente da tela"),
             ("Posta quando sobra tempo", "Ou seja: quase nunca"),
             ("Some por semanas", "E o algoritmo esquece de você"),
             ("Cliente não lembra de você", "E compra do concorrente")]
    for i, (a, b) in enumerate(items):
        st = 0.7 + i*0.45
        def draw(d, o, i=i, a=a, b=b, st=st):
            jit = 6*math.sin((t-st)*22+i)*clamp(1.2-(t-st))
            x0, y0 = 110+jit+(i % 2)*30, 790+i*175+o
            d.rounded_rectangle([x0, y0, x0+830, y0+145], 28, fill=CARD+(235,), outline=LINE, width=2)
            d.ellipse([x0+34, y0+42, x0+94, y0+102], fill=(248,113,113,45), outline=RED, width=3)
            d.text((x0+56, y0+44), "!", font=F("Bold", 40), fill=RED)
            d.text((x0+125, y0+26), a, font=F("Bold", 40), fill=WHITE)
            d.text((x0+125, y0+82), b, font=F("Regular", 30), fill=MUTED)
        el(img, t, st, sa, draw, dy=70, d=0.4)

def s_reveal(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 640+o, "Conheça o", F("Medium", 46), MUTED))
    def logo(d, o):
        s = 200; x0, y0 = W/2-s/2, 730+o
        d.rounded_rectangle([x0, y0, x0+s, y0+s], 52, fill=SKY)
        d.text((x0+32, y0+40), "OS", font=F("Bold", 100), fill=(255,255,255))
    el(img, t, 0.3, sa, logo, dy=0, d=0.5)
    el(img, t, 0.6, sa, lambda d, o: wordmark(d, W/2, 970+o, 104))
    el(img, t, 1.0, sa, lambda d, o: ctext(d, 1125+o, "O marketing do mês inteiro", F("Regular", 44), WHITE))
    el(img, t, 1.15, sa, lambda d, o: ctext(d, 1182+o, "planejado e postado pra você.", F("Regular", 44), SKY2))

def s_steps(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 360+o, "SIMPLES ASSIM", F("Medium", 34), SKY2))
    el(img, t, 0.15, sa, lambda d, o: ctext(d, 415+o, "Três passos.", F("Bold", 88), WHITE))
    el(img, t, 0.3, sa, lambda d, o: ctext(d, 520+o, "Zero dor de cabeça.", F("Bold", 76), MUTED))
    steps = [("Conte o que você vende", ["Seu negócio, o que resolve e", "pra quem. Só três campos."]),
             ("Receba o plano do mês", ["Calendário pronto, com posts", "escritos com a cara da sua marca."]),
             ("Poste no automático", ["Os posts saem sozinhos nas suas", "redes, no dia e hora certos."])]
    for i, (h, sub) in enumerate(steps):
        st = 0.9 + i*1.5
        def draw(d, o, i=i, h=h, sub=sub):
            x0, y0 = 90, 720+i*255+o
            d.rounded_rectangle([x0, y0, x0+900, y0+220], 32, fill=CARD+(240,), outline=LINE, width=2)
            d.ellipse([x0+40, y0+55, x0+140, y0+155], fill=SKY)
            n = str(i+1); f = F("Bold", 52); tw = d.textlength(n, font=f)
            d.text((x0+90-tw/2, y0+68), n, font=f, fill=(255,255,255))
            d.text((x0+175, y0+32), h, font=F("Bold", 44), fill=WHITE)
            for j, s in enumerate(sub):
                d.text((x0+175, y0+100+j*46), s, font=F("Regular", 31), fill=MUTED)
        el(img, t, st, sa, draw, dy=80)
    k = int(clamp((t-0.9)/1.5, 0, 2.99))
    def ring(d):
        x0, y0 = 90, 720+k*255
        d.rounded_rectangle([x0-3, y0-3, x0+903, y0+223], 34, outline=SKY+(220,), width=4)
    layer(img, sa*appear(t, 0.9), ring)

POSTS = {2, 4, 6, 9, 11, 13, 16, 18, 20, 23, 25, 27, 30}
def s_calendar(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: ctext(d, 330+o, "Seu mês inteiro,", F("Bold", 84), WHITE))
    el(img, t, 0.15, sa, lambda d, o: ctext(d, 430+o, "no calendário.", F("Bold", 84), SKY2))
    cw, ch, gx, gy = 128, 118, 12, 12
    x0 = (W - (7*cw + 6*gx))/2; y0 = 780
    def head(d, o):
        d.rounded_rectangle([x0-24, y0-110+o, W-x0+24, y0+5*(ch+gy)+30+o], 36, fill=CARD+(235,), outline=LINE, width=2)
        for i, s in enumerate(["D", "S", "T", "Q", "Q", "S", "S"]):
            f = F("Medium", 30); tw = d.textlength(s, font=f)
            d.text((x0+i*(cw+gx)+cw/2-tw/2, y0-75+o), s, font=f, fill=MUTED)
    el(img, t, 0.3, sa, head, dy=50)
    fill_p = clamp((t-0.9)/2.2)
    ordered = sorted(POSTS)
    shown = set(ordered[:int(fill_p*len(ordered)+0.001)])
    def grid(d, o):
        for day in range(1, 32):
            idx = day + 1  # month starts on Tuesday
            c, r = idx % 7, idx // 7
            x = x0 + c*(cw+gx); y = y0 + r*(ch+gy) + o
            on = day in shown
            d.rounded_rectangle([x, y, x+cw, y+ch], 20, fill=(14,165,233,60) if on else (255,255,255,10), outline=SKY if on else LINE, width=2)
            d.text((x+14, y+8), str(day), font=F("Medium", 28), fill=WHITE if on else MUTED)
            if on:
                d.ellipse([x+cw-44, y+ch-44, x+cw-12, y+ch-12], fill=GREEN)
                d.line([(x+cw-36, y+ch-28), (x+cw-30, y+ch-21), (x+cw-20, y+ch-35)], fill=(6, 30, 20), width=4)
    el(img, t, 0.5, sa, grid, dy=50)
    el(img, t, 3.0, sa, lambda d, o: ctext(d, 1500+o, "13 posts agendados e publicados", F("Medium", 42), WHITE))
    el(img, t, 3.2, sa, lambda d, o: ctext(d, 1560+o, "sem você abrir o Instagram.", F("Medium", 42), SKY2))

def s_offer(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: pill(d, W/2, 470+o, "OFERTA DE LANÇAMENTO", F("Medium", 32), AMBER, (251,191,36,35), outline=(251,191,36,140)))
    el(img, t, 0.2, sa, lambda d, o: ctext(d, 600+o, "Só para os", F("Bold", 84), WHITE))
    el(img, t, 0.35, sa, lambda d, o: ctext(d, 700+o, "20 primeiros", F("Bold", 120), AMBER))
    def badge(d, o):
        bw, bh = 820, 350; x0, y0 = W/2-bw/2, 900+o
        d.rounded_rectangle([x0, y0, x0+bw, y0+bh], 44, fill=(40, 30, 6, 235), outline=AMBER, width=4)
        ctext(d, y0+30, "até", F("Medium", 44), (253, 230, 138))
        ctext(d, y0+80, "50% OFF", F("Bold", 140), AMBER)
        ctext(d, y0+268, "vitalício na mensalidade", F("Medium", 40), WHITE)
    el(img, t, 0.8, sa, badge, dy=0, d=0.45)
    el(img, t, 1.4, sa, lambda d, o: ctext(d, 1310+o, "20 vagas de Membro Fundador", F("Medium", 42), WHITE))
    el(img, t, 1.7, sa, lambda d, o: ctext(d, 1375+o, "Desconto garantido enquanto for assinante.", F("Regular", 34), MUTED))

def s_cta(img, t, sa):
    el(img, t, 0.0, sa, lambda d, o: wordmark(d, W/2, 440+o, 70))
    el(img, t, 0.3, sa, lambda d, o: ctext(d, 590+o, "Comente", F("Bold", 90), WHITE))
    def word(d, o):
        bw, bh = 560, 170; x0, y0 = W/2-bw/2, 710+o
        d.rounded_rectangle([x0, y0, x0+bw, y0+bh], 40, fill=SKY)
        ctext(d, y0+18, "PLANO", F("Bold", 120), (255, 255, 255))
    el(img, t, 0.55, sa, word, dy=0, d=0.4)
    el(img, t, 0.9, sa, lambda d, o: ctext(d, 925+o, "que eu te mando o link no direct", F("Medium", 44), WHITE))
    el(img, t, 1.4, sa, lambda d, o: ctext(d, 1060+o, "7 dias grátis · sem cartão", F("Bold", 54), SKY2))
    el(img, t, 1.7, sa, lambda d, o: ctext(d, 1140+o, "solomarketeros.gfcode.com.br", F("Medium", 44), MUTED))
    el(img, t, 2.3, sa, lambda d, o: ctext(d, 1440+o, "Desenvolvido por Giovani · GF Code  @gf.code", F("Medium", 30), MUTED))

SC = [(0.0, 3.4, s_hook), (3.4, 7.6, s_pain), (7.6, 10.8, s_reveal), (10.8, 17.2, s_steps),
      (17.2, 22.2, s_calendar), (22.2, 27.4, s_offer), (27.4, 33.0, s_cta)]
DUR = SC[-1][1]

def frame(i):
    T = i / FPS
    img = background(T)
    for (a, b, fn) in SC:
        if a - 0.01 <= T < b:
            t = T - a
            sa = clamp(t/0.3) * (1 if fn is s_cta else clamp((b-T)/0.35 + 0.0001))
            fn(img, t, sa)
    if 10.8 < T < 27.4:
        a = clamp((T-10.8)/0.5)*clamp((27.4-T)/0.4)
        layer(img, a, lambda d: wordmark(d, W/2, 150, 40))
    layer(img, 1, lambda d: d.rectangle([0, 0, W*T/DUR, 8], fill=SKY+(230,)))
    img.convert("RGB").save(f"{OUTDIR}/f{i:05d}.jpg", quality=92)
    return i

if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    n = int(DUR*FPS)
    if len(sys.argv) > 2:
        for s in sys.argv[2].split(","): frame(int(s))
    else:
        with Pool(2) as p:
            for _ in p.imap_unordered(frame, range(n), chunksize=8): pass
    print("frames", n, "dur", DUR)
