# Existing-server deployment with certbot

Use an existing Nginx server with authorization, a working SSH login, and ports 80/443 reachable. This repository never provisions paid resources. Do not alter the apex domain or other virtual hosts.

The current existing-server deployment has completed steps 2–4 and verified the webroot publicly using a Host header. DNS is the remaining prerequisite. The final TLS configuration and `finish-tls.sh` are prepared under `/var/www/desktoppet/deploy/`; run that script after adding the A record. It uses the existing ACME account, checks DNS, preserves the previous dedicated configuration, and tests only the new certificate’s renewal. The certificate has not yet been issued.

1. Add only the `desktoppet` A record in the existing `hiimobapps.cn` AliDNS zone, pointing to the chosen server's public IPv4 address. Add AAAA only if that server actually supports public IPv6. Check CAA and any existing record before changing this subdomain.
2. Build with `SITE_URL=https://desktoppet.hiimobapps.cn python3 scripts/build.py`, then run `SITE_URL=https://desktoppet.hiimobapps.cn python3 scripts/check.py`.
3. Copy `_site/` into a new timestamped directory under `/var/www/desktoppet/releases/`. Set `/var/www/desktoppet/current` as a symlink to this release. Preserve the previous release for rollback. Give Nginx read access only.
4. Install `desktoppet.nginx.conf` as its own virtual host using the server's existing Nginx include convention. Check the root and server name, then run `nginx -t` before reloading Nginx. Do not replace or disable other virtual hosts.
5. Once public DNS points to the server and HTTP is reachable, issue a free Let's Encrypt certificate:

```sh
certbot --nginx -d desktoppet.hiimobapps.cn --redirect
nginx -t
certbot renew --dry-run
```

Accept the Let's Encrypt terms using the server owner's existing ACME account. Reuse its existing account email where available; do not publish it here. Inspect the certbot-generated configuration and verify that the system's certbot renewal timer is active. Certificate keys stay under the server's protected `/etc/letsencrypt/` tree, outside this repository and web root.

6. Verify all six languages, `/support/`, `/privacy/`, HTTP-to-HTTPS redirection, public DNS, certificate issuer/SAN/expiry, and renewal. Update the website repository's `SITE_URL` GitHub variable if its canonical production domain changes.

## GitHub Pages fallback

The included Actions workflow publishes at `https://glzlaohuai.github.io/desktoppet-site/`. GitHub Pages manages its own HTTPS certificate and cannot load a certificate or private key made with certbot. Keeping Pages on its default domain provides a public fallback while existing-server access and AliDNS credentials are unavailable.

To bind the custom domain to Pages instead, point only the subdomain CNAME to `glzlaohuai.github.io`, set the Pages custom domain and `SITE_URL`, redeploy, and enable HTTPS enforcement after its managed certificate is issued. This alternative does not satisfy a requirement to use certbot on the serving endpoint.
