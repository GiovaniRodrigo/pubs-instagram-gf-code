"""Corrige a legenda queimada 'I.A. não faz o seu trabajo' -> 'trabalho' (1,4 s a 8,7 s):
desfoca o fundo sob a frase antiga e escreve a frase correta com Inter Bold no mesmo lugar."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
SRC = HERE / "gfcode_2026-10-16_ia_nao_faz_seu_trabalho_original.mp4"
OUT = HERE / "gfcode_2026-10-16_ia_nao_faz_seu_trabalho.mp4"
TXT, MASK, MASK2 = HERE / "_fix_txt.png", HERE / "_fix_mask.png", HERE / "_fix_mask2.png"
PX, PY, PW, PH = 70, 596, 580, 96          # área apagada
T0, T1 = 1.40, 8.70                        # janela da frase original
T2 = 9.10                                  # fim da transição para "mas..." (só laterais)

font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 42)
s = "I.A. não faz o seu trabalho"
b = font.getbbox(s); w = b[2] - b[0]
x = round(359 - w / 2) - b[0]; y = 621 - 8
img = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
ImageDraw.Draw(sh).text((x + 1, y + 2), s, font=font, fill=(0, 0, 0, 150))
img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(3)))
ImageDraw.Draw(img).text((x, y), s, font=font, fill=(255, 255, 255, 255))
img.save(TXT)

m = Image.new("L", (PW, PH), 0)
ImageDraw.Draw(m).rounded_rectangle((14, 14, PW - 14, PH - 14), 20, fill=255)
m.filter(ImageFilter.GaussianBlur(9)).save(MASK)
m2 = Image.new("L", (PW, PH), 0); d2 = ImageDraw.Draw(m2)
d2.rounded_rectangle((14, 14, 222, PH - 14), 20, fill=255)      # "I.A. não fa"
d2.rounded_rectangle((372, 14, PW - 14, PH - 14), 20, fill=255) # "trabajo"
m2.filter(ImageFilter.GaussianBlur(9)).save(MASK2)

fc = (f"[0:v]split=3[a][b][b2];[b2]crop={PW}:{PH}:{PX}:{PY},boxblur=24:4,format=rgba[bl2];"
      f"[3:v]format=gray[m2];[bl2][m2]alphamerge,fade=t=out:st={T2-0.1}:d=0.1:alpha=1[patch2];"
      f"[b]crop={PW}:{PH}:{PX}:{PY},boxblur=24:4,format=rgba[bl];"
      f"[2:v]format=gray[m];[bl][m]alphamerge,fade=t=in:st={T0}:d=0.15:alpha=1,fade=t=out:st={T1-0.12}:d=0.12:alpha=1[patch];"
      f"[1:v]format=rgba,fade=t=in:st={T0+0.05}:d=0.25:alpha=1,fade=t=out:st={T1-0.1}:d=0.3:alpha=1[txt];"
      f"[a][patch]overlay={PX}:{PY}:enable='between(t,{T0},{T1})'[c];"
      f"[c][patch2]overlay={PX}:{PY}:enable='between(t,{T1},{T2})'[c2];"
      f"[c2][txt]overlay=0:0:enable='between(t,{T0},{T1}+0.2)',format=yuv420p[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC),
                "-loop", "1", "-framerate", "24", "-t", "15.1", "-i", str(TXT),
                "-loop", "1", "-framerate", "24", "-t", "15.1", "-i", str(MASK),
                "-loop", "1", "-framerate", "24", "-t", "15.1", "-i", str(MASK2),
                "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "17",
                "-preset", "slow", "-c:a", "copy", "-movflags", "+faststart", "-shortest", str(OUT)], check=True)
TXT.unlink(); MASK.unlink(); MASK2.unlink()
print(OUT)
