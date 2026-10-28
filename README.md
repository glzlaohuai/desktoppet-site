# DesktopPet website

The public marketing, support and privacy website for DesktopPet, a macOS 14+ pixel companion app. Six complete static languages: English, Simplified Chinese, Japanese, Korean, French and German. DesktopPet is preparing for its first App Store release; no download or unverified pricing is advertised.

- Repository: https://github.com/glzlaohuai/desktoppet-site
- Website: https://glzlaohuai.github.io/desktoppet-site/
- Support: https://glzlaohuai.github.io/desktoppet-site/support/
- Privacy: https://glzlaohuai.github.io/desktoppet-site/privacy/
- Intended custom domain: `desktoppet.hiimobapps.cn`, pending access to existing AliDNS and server configuration.

## Build and preview

Python 3.10+ only. No build dependencies, analytics, external font requests or runtime framework. Every page works without JavaScript; JavaScript adds the language dropdown and an optional pet preview. Language links remain in the footer without JavaScript.

```sh
SITE_URL=http://127.0.0.1:8765 python3 scripts/build.py
SITE_URL=http://127.0.0.1:8765 python3 scripts/check.py
python3 -m http.server 8765 --directory _site --bind 127.0.0.1
```

For production, use the actual HTTPS `SITE_URL`. The builder handles a project subpath as well as a domain root. Every push to `main` builds, checks internal links and deploys GitHub Pages. Set the repository variable `SITE_URL` to change its canonical origin; this alone does not configure DNS or Pages custom domains.

## Sources

- `content/marketing.json`: the app's reviewed six-language descriptions from `docs/app-store/LOCALIZATIONS.md`.
- `content/privacy/`: verbatim reviewed app privacy policies; website hosting and support disclosures are added separately by the template.
- `content/locales.json`: translated website labels, support answers, availability notice and website privacy disclosure.
- `assets/pets/`: original 32×32 artwork exported from the app's `PixelArt.swift`, without changing the app repository.
- `assets/settings-*.webp`: actual localized app settings captures.
- `assets/fonts/`: self-hosted Bricolage Grotesque under its included SIL Open Font License.

No app code, personal review contact information, API keys, signing material, certificate private keys or server credentials are included. Public support uses this repository's GitHub Issues. This repository does not license the DesktopPet application or original companion artwork for redistribution.

See [deploy/README.md](deploy/README.md) for dedicated Nginx and certbot deployment using an existing server. GitHub Pages uses GitHub-managed HTTPS and cannot install a certbot certificate.
