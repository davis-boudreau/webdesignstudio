# Security Policy

Please report vulnerabilities privately through GitHub's "Report a vulnerability" (Security Advisories) on this repository rather than a public issue. The app is fully client-side; areas of most interest are JSON import handling and any use of `innerHTML`.

System-font mode makes no external font requests. Optional Google Fonts mode
uses HTTPS stylesheets from `fonts.googleapis.com` and font files from
`fonts.gstatic.com`. Imported font settings accept curated family IDs and known
weights; they cannot supply arbitrary URLs, stylesheet content or scripts. The
fallback comparison is a preview setting and does not change exported font choices.

Imported Brand Palettes accept at most 24 entries, unique restricted token IDs
and six-digit HEX colours. Names are bounded and rendered as text or escaped in
reference markup; they cannot supply CSS declarations or HTML. Main Palette
dropdowns apply validated HEX values through the existing colour-role controls.
