# Scope

Maintain the public MIT Multisim MCP core in this repo.

Commercial features (installation support, upgrades, multi-board joint parameter search, topology search, advanced layout/routing optimization) belong to a separate private checkout. Never implement, import, or publish them here, and never copy product packages, customer data, private models, commercial prompts, evaluation sets, credentials, or deployment configs from that checkout. A shared folder or git branch does not constitute release authorization. Review the origin of any patch from the commercial checkout before importing; untrusted assets stay local until the owner defines their public scope.

Keep electrical-correctness fixes and published-API compatibility forever. Pin connectivity and honest verification are the core duty. Keep original licenses on published code; never strip attribution, rewrite public history, or call private work public.

Performance claims require current, comparable measured baselines; no comparison, no claim.

Before external delivery: stage only reviewed files, run `python tools/release_audit.py --json`, and validate wheel/sdist with `tools/check_mcp_package.py`. Scope details: `docs/OPEN_SOURCE_SCOPE.md`; publishing: `docs/PUBLISHING.md`.

# Figures

Take device symbols from a stock symbol library; never hand-draw them from circles and lines.

For LaTeX: use circuitikz with the `european` option for IEC box gates (`node[npn]`, `to[R]`, `to[C]`, `to[cI]`, `node[ground]`). If unsure how a device is written in the loaded package, first compile a five-line probe to PNG and confirm the shape matches the textbook before drawing the final figure.

Phasors, complex planes, waveforms, and impedance triangles are pure geometry: use basic TikZ primitives. Any electrical device silhouette switches back to rule 1.

A figure passes only when both hold: it looks like an engineering diagram (correct symbols, correct geometry), and the mechanical checks are clean. Mechanical checks alone prove only the absence of low-level errors.

Prefer schemdraw (Python, MIT) for circuit diagrams; its symbol inventory is complete and iteration is faster than hand-written TikZ. Note: schemdraw SVG bakes text into outlines (no text nodes); if text nodes are required, use circuitikz with `dvisvgm --font-format=woff2`.

Matplotlib config for CJK and opaque white background:

```python
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"] + matplotlib.rcParams["font.sans-serif"]
matplotlib.rcParams["savefig.transparent"] = False
```

Every delivered PNG must pass `deliverables/figures-src/whiten.py` (converts to opaque white RGB; `--check` gates). Transparent-background PNGs render CJK as mosaic, which readers misdiagnose as missing glyphs.

Write formulas with matplotlib mathtext inside the same text call as CJK, e.g. `r"Z = $\sqrt{R^{2}+X^{2}}$"`. Verified: radical bar complete, φ/Ω intact, CJK intact.

Text-over-line collisions are never judged by eye. Use `deliverables/figures-src/collide3.py --all` (ink-diff between full render and text-only render; reports which text is crossed and by how many pixels). Gate: `crossed_texts=0`.

Delegate figure work end-to-end to subagents: give each one the requirements, available tools, and a hard cap of 5 iteration rounds in the task prompt. At round 5 it stops and delivers with a leftover-issues report regardless of outcome; an uncapped subagent burns to timeout. The main thread only sets requirements, prepares tooling, and does final acceptance; it never touches first drafts.

# Outgoing mail

Mail to other repos goes into that repo's `mail/` root, numbered after that repo's latest mail number. `mail/sent/` is the recipient's own outbox; writing there is a misdelivery.

# Push path

Push goes straight to the branch (no PRs). The gate is the push itself: SSH signs via the akr FIDO2 agent, the phone shows an approval prompt, and the push completes only after the operator taps Allow. HTTPS push fails (HTTP 403, tokens are read-only), so use SSH.

Approval does not go through wo-u (wo-u carries only task dispatch and rulings). Write the change summary and the code-review skill's verdict into the final output of your session (the commit message carries them too), then stop. The operator patrols sessions, reads final outputs, and replies with approval before any push happens. A push whose commit message lacks the review verdict and change summary is ignored.

Remotes are split: origin fetch = `https://github.com/ArchivalEra/multisim-mcp.git` (read-only PAT via gh keyring, silent), origin push = `ssh://git@github-ArchivalEra/ArchivalEra/multisim-mcp.git` (SK key + MFA). Never configure an `ssh://` URL as a fetch URL: every ssh fetch fires a phone approval prompt — forbidden. Daily `git fetch` / `git pull` is approval-free; only push pages the phone.

Proxy, and repo-specific gate knobs follow the shape of reviewly-nsh's AGENTS.md, adapted to this repo's own Einfacht configuration (reference, never copy). Set the proxy variables before pushing: `export https_proxy=http://127.0.0.1:2080 http_proxy=http://127.0.0.1:2080`.

Reading GitHub resources (repos, issues, PRs, Actions, releases, private included) goes through the gh CLI (`gh api`, `gh repo view`, ...) with the read-only PATs. For actually fetching objects, fall back to plain `git fetch` over HTTPS (`https://github.com/...`, read-only PAT works). Never use `gh repo sync` (it needs write access; HTTP 403 on a read-only PAT). The SSH aliases are push-only: `git push` via the `github-ArchivalEra` alias with MFA approval.

Delivery without a pending push = local edit → report the change via wo-u → wait. Do not run experimental pushes to test the path.
