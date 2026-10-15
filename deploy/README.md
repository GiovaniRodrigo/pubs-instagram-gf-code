# Deploy do site gfcode.com.br na VPS

O site estático fica em `site/`. Hoje o domínio **gfcode.com.br** aponta para outro servidor (LiteSpeed/Hostinger). Por isso, publique primeiro na VPS, teste, e só depois troque o DNS.

## 1. Publicar na VPS (sem afetar o site atual)

```bash
git clone https://github.com/GiovaniRodrigo/pubs-instagram-gf-code.git
cd pubs-instagram-gf-code
sudo bash deploy/deploy-site.sh
```

## 2. Testar antes de trocar o DNS

Substitua `IP_DA_VPS` pelo IP público da VPS:

```bash
curl -sI --resolve gfcode.com.br:80:IP_DA_VPS http://gfcode.com.br/ | head -1
for p in / /termos/ /privacidade/ /robots.txt /sitemap.xml /llms.txt /llms-full.txt /humans.txt /.well-known/security.txt /site.webmanifest /og-image.png /pagina-inexistente; do
  printf '%-28s ' "$p"; curl -s -o /dev/null -w '%{http_code} %{content_type}\n' --resolve gfcode.com.br:80:IP_DA_VPS "http://gfcode.com.br$p"
done
```

Esperado: 200 em tudo e 404 na página inexistente.

## 3. Trocar o DNS (decisão manual)

No painel do domínio, aponte os registros **A** de `gfcode.com.br` e `www` para o IP da VPS. **Não altere** os registros MX/TXT de e-mail (`giovani@gfcode.com.br` continua funcionando).

## 4. HTTPS

Depois que o DNS propagar:

```bash
sudo bash deploy/deploy-site.sh --https
```

## 5. Depois de no ar

- Google Search Console e Bing Webmaster Tools: enviar `https://gfcode.com.br/sitemap.xml`.
- TikTok for Developers: usar `https://gfcode.com.br/termos/` e `https://gfcode.com.br/privacidade/` e verificar o domínio em **URL properties** (registro TXT no DNS ou arquivo de verificação em `site/`).

## Atualizar o site

```bash
cd pubs-instagram-gf-code && git pull && sudo bash deploy/deploy-site.sh
```
