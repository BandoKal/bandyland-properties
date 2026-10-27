# Public rental dashboard

Only `site-dist/` is deployed. It is generated from an explicit public content catalog. Do not copy the workspace, sources folder, original budget, business plan, contractor emails or account records into this directory.

## Update project state

Run `python3 scripts/refresh_site.py` while authenticated with `gh` and read access to Project 7. It writes only issue number/title/status, target, priority, link and closure date—not bodies, comments or attachments. Review the diff, then commit/push `site/data/project.json` to main. The Pages workflow builds and deploys automatically after that push. This site is a timestamped snapshot, not a continuously synchronized connection to the private GitHub project.

Only issues carrying Rental or Operations labels (case-insensitive OR match) are included. Other labels alone do not qualify. Filtering happens before selecting the latest/next three; fewer than three are shown when fewer qualify.

Recent completions: project Done items, newest issue `closedAt` first. Active: all In progress items, with a visible warning above three (never conceal a fourth). On deck: Todo items from the curated `onDeck` sequence in `site/data/editorial.json`, then remaining Todo items by target date/issue number. It is a proposed queue; dependencies must still be checked before starting. On hold is separate. Archived/out-of-scope items are excluded.

Edit public notes in `site/content/` and the document/decision catalog in `site/data/editorial.json`. Decisions are editorial and have their own review date; live status does not automatically approve a decision. Only catalog entries with `file` are published/downloadable. Original six-pager and budget are catalog entries without files; the six-section overview is a public summary, not the original.

## Build and check

`npm ci && npm run build && npm run check`

Preview: `python3 -m http.server 8765 --directory site-dist --bind 127.0.0.1`.

The public site has no login and no access-control illusion. `noindex` is only a crawler request, not privacy. GitHub issue/board links retain their own GitHub permissions. Never put tokens into browser JavaScript or the snapshot. Automatic private-project polling would require a separate least-privilege authentication setup; it is not configured here.
