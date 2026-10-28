#!/usr/bin/env bash
# Run on the existing server after only the desktoppet DNS record is configured.
set -euo pipefail
desktoppet_domain=desktoppet.hiimobapps.cn
desktoppet_expected_ip=101.200.38.45
desktoppet_conf=/etc/nginx/conf.d/desktoppet.hiimobapps.cn.conf
desktoppet_script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
test "$(id -u)" = 0
test -f "$desktoppet_conf"
test -d /var/www/desktoppet/current
python3 - "$desktoppet_domain" "$desktoppet_expected_ip" <<'PY'
import socket,sys
ips={x[4][0] for x in socket.getaddrinfo(sys.argv[1],80,socket.AF_INET)}
if ips != {sys.argv[2]}:
    raise SystemExit('DNS is not ready for this server: '+str(ips))
PY
nginx -t
certbot certonly --webroot -w /var/www/certbot \
  --cert-name "$desktoppet_domain" -d "$desktoppet_domain" \
  --non-interactive --agree-tos \
  --deploy-hook 'nginx -t && systemctl reload nginx'
desktoppet_backup="/var/www/desktoppet/nginx-before-tls-$(date -u +%Y%m%dT%H%M%SZ).conf"
cp "$desktoppet_conf" "$desktoppet_backup"
cp "$desktoppet_script_dir/desktoppet.tls.nginx.conf" "$desktoppet_conf"
if ! nginx -t; then
  cp "$desktoppet_backup" "$desktoppet_conf"
  exit 1
fi
systemctl reload nginx
certbot renew --cert-name "$desktoppet_domain" --dry-run
systemctl is-active certbot-renew.timer
curl --fail --retry 3 --retry-delay 1 "https://$desktoppet_domain/support/" -o /dev/null
curl --fail --retry 3 --retry-delay 1 "https://$desktoppet_domain/privacy/" -o /dev/null
