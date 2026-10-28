# DesktopPet website

The public marketing, support and privacy website for DesktopPet, a macOS 14+ pixel companion app. Six complete static languages: English, Simplified Chinese, Japanese, Korean, French and German. DesktopPet is preparing for its first App Store release; no download or unverified pricing is advertised.

- Repository: https://github.com/glzlaohuai/desktoppet-site
- Website: https://desktoppet.hiimobapps.cn/
- Support: https://desktoppet.hiimobapps.cn/support/
- Privacy: https://desktoppet.hiimobapps.cn/privacy/
- GitHub Pages backup: https://glzlaohuai.github.io/desktoppet-site/

## Build and preview

Python 3.10+ only. No build dependencies, analytics, external font requests or runtime framework. Every page works without JavaScript; JavaScript adds the language dropdown and an optional pet preview. Language links remain in the footer without JavaScript.

```sh
SITE_URL=http://127.0.0.1:8765 python3 scripts/build.py
SITE_URL=http://127.0.0.1:8765 python3 scripts/check.py
python3 -m http.server 8765 --directory _site --bind 127.0.0.1
```

For the primary server, build with `SITE_URL=https://desktoppet.hiimobapps.cn`. The builder handles a project subpath as well as a domain root. Every push to `main` builds, checks internal links and deploys the GitHub Pages backup. Keep that workflow's URL at its default project subpath; publish the primary server separately using the release procedure in `deploy/README.md`.

## Sources

- `content/marketing.json`: the app's reviewed six-language descriptions from `docs/app-store/LOCALIZATIONS.md`.
- `content/privacy/`: verbatim reviewed app privacy policies; website hosting and support disclosures are added separately by the template.
- `content/locales.json`: translated website labels, support answers, availability notice and website privacy disclosure.
- `assets/pets/`: original 32×32 artwork exported from the app's `PixelArt.swift`, without changing the app repository.
- `assets/settings-*.webp`: actual localized app settings captures.
- `assets/fonts/`: self-hosted Bricolage Grotesque under its included SIL Open Font License.

No app code, personal review contact information, API keys, signing material, certificate private keys or server credentials are included. Public support uses this repository's GitHub Issues. This repository does not license the DesktopPet application or original companion artwork for redistribution.

See [deploy/README.md](deploy/README.md) for dedicated Nginx and certbot deployment using an existing server. GitHub Pages uses GitHub-managed HTTPS and cannot install a certbot certificate.

## Deployment status (October 28, 2026)

The primary website is live on the custom domain with HTTP-to-HTTPS redirects and a certbot-issued Let's Encrypt certificate, valid through January 26, 2027. Certificate hostname and trust were verified. The existing `certbot-renew.timer` is active, the certificate has a successful renewal dry run, and its deploy hook reloads Nginx after renewal. GitHub Pages remains a separate HTTPS backup.

The existing server at `101.200.38.45` has a dedicated `/etc/nginx/conf.d/desktoppet.hiimobapps.cn.conf`, release directories under `/var/www/desktoppet/releases/`, and a `current` symlink. All 18 routes and the ACME webroot were verified, including from outside the server. Browser checks passed at 1440, 768, 390 and 320 pixels; pet selection, greetings, pause, Reduce Motion, language-preserving navigation, FAQ expansion and privacy access without JavaScript were verified.

AliDNS was configured using the existing local CLI OAuth profile: only `desktoppet` A → `101.200.38.45` was added (TTL 600). Google DNS, Cloudflare DNS and the server resolver confirmed it. All nine pre-existing DNS records and all six pre-existing Nginx configuration files were checked and remain unchanged. No paid resource was created. Keys and CLI credentials remain outside the repository.
