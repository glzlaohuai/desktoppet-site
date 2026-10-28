# Existing-server deployment with certbot

Use an existing Nginx server with authorization, a working SSH login, and ports 80/443 reachable. This repository never provisions paid resources. Do not alter the apex domain or other virtual hosts.

The current deployment is complete at `https://desktoppet.hiimobapps.cn/`. The AliDNS A record points to `101.200.38.45`; certbot issued a trusted Let's Encrypt certificate valid through January 26, 2027. The certificate-specific renewal dry run succeeded, the existing renewal timer is active, and the renewal hook checks and reloads Nginx. The final TLS configuration and completion script are also stored under `/var/www/desktoppet/deploy/` on the server.

1. Add only the `desktoppet` A record in the existing `hiimobapps.cn` AliDNS zone, pointing to the chosen server's public IPv4 address. Add AAAA only if that server actually supports public IPv6. Check CAA and any existing record before changing this subdomain.
2. Build with `SITE_URL=https://desktoppet.hiimobapps.cn python3 scripts/build.py`, then run `SITE_URL=https://desktoppet.hiimobapps.cn python3 scripts/check.py`.
3. Copy `_site/` into a new timestamped directory under `/var/www/desktoppet/releases/`. Set `/var/www/desktoppet/current` as a symlink to this release. Preserve the previous release for rollback. Give Nginx read access only.
4. Install `desktoppet.nginx.conf` as its own virtual host using the server's existing Nginx include convention. Check the root and server name, then run `nginx -t` before reloading Nginx. Do not replace or disable other virtual hosts.
5. Once public DNS points to the server and HTTP is reachable, copy `finish-tls.sh` and `desktoppet.tls.nginx.conf` into one server directory, then run the script as root:

```sh
bash /var/www/desktoppet/deploy/finish-tls.sh
```

The script uses certbot's webroot authenticator and the existing ACME account. It preserves the dedicated HTTP configuration, obtains the certificate, installs the dedicated TLS configuration, checks Nginx before reload, tests only this certificate's renewal, and verifies HTTPS support and privacy routes. Certificate keys stay under the server's protected `/etc/letsencrypt/` tree, outside this repository and web root.

6. Verify all six languages, `/support/`, `/privacy/`, HTTP-to-HTTPS redirection, public DNS, certificate issuer/SAN/expiry, and renewal.

## Updating the live server

Build and check with the primary domain's `SITE_URL`, upload `_site/` to a new directory under `/var/www/desktoppet/releases/`, then atomically replace the `current` symlink. Preserve the previous release for rollback. Static-content updates do not require replacing the TLS virtual host or reissuing a certificate. GitHub Actions updates the Pages backup automatically; it does not upload releases to this server.

## GitHub Pages fallback

The included Actions workflow publishes at `https://glzlaohuai.github.io/desktoppet-site/`. GitHub Pages manages its own HTTPS certificate and cannot load a certificate or private key made with certbot. Keeping Pages on its default domain provides a separate public backup. The primary custom domain is served by Nginx using the actual certbot certificate.

To bind the custom domain to Pages instead, point only the subdomain CNAME to `glzlaohuai.github.io`, set the Pages custom domain and `SITE_URL`, redeploy, and enable HTTPS enforcement after its managed certificate is issued. This alternative does not satisfy a requirement to use certbot on the serving endpoint.
