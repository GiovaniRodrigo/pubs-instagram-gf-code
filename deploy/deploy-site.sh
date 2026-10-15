#!/usr/bin/env bash
# Publica o site da GF Code na VPS (Ubuntu/Debian com nginx).
# Uso: sudo bash deploy/deploy-site.sh            -> copia arquivos e configura nginx (sem HTTPS)
#      sudo bash deploy/deploy-site.sh --https    -> também emite o certificado com certbot
# Rode a partir da raiz do repositório pubs-instagram-gf-code.
set -euo pipefail

DOMAIN="gfcode.com.br"
WEBROOT="/var/www/${DOMAIN}"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v nginx >/dev/null 2>&1; then
  apt-get update -y && apt-get install -y nginx
fi

mkdir -p "$WEBROOT"
rsync -a --delete "$REPO_DIR/site/" "$WEBROOT/"
chown -R www-data:www-data "$WEBROOT"

cp "$REPO_DIR/deploy/nginx-gfcode.conf" "/etc/nginx/sites-available/${DOMAIN}"
ln -sf "/etc/nginx/sites-available/${DOMAIN}" "/etc/nginx/sites-enabled/${DOMAIN}"
nginx -t
systemctl reload nginx

if [[ "${1:-}" == "--https" ]]; then
  if ! command -v certbot >/dev/null 2>&1; then
    apt-get install -y certbot python3-certbot-nginx
  fi
  certbot --nginx -d "$DOMAIN" -d "www.${DOMAIN}" --redirect --non-interactive --agree-tos -m "giovani@${DOMAIN}"
fi

echo "OK: site publicado em $WEBROOT"
