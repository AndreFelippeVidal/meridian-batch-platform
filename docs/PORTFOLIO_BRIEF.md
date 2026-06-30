# Meridian Platform — Build Brief (for Claude Code, Plan Mode)

> Paste this whole document into Claude Code in **plan mode**. Read §0 first, then propose a
> plan for **Layer 0 only** (§7) and wait for my approval before writing any files.
> Sections §1–§6 and §8 are durable context for the whole portfolio, not part of the first task.

---

## 0. How to use this document

- This is the source of truth for a personal portfolio of data + AI projects. It defines the
  mission, the locked decisions, the full roadmap, and a precise spec for the first thing to build.
- **Operate in plan mode.** First task = build **Layer 0** (the build system), spec'd in §7.
- After we finish Layer 0, later sessions will tackle Projects 1–6 (§3) one at a time.
- Recommended: once Layer 0 exists, save a trimmed version of §1–§6 into the template repo's
  `CLAUDE.md`, and keep this full file as `docs/PORTFOLIO_BRIEF.md` in the profile/hub repo.
- Where exact tool versions are given, treat them as a floor — pin the latest stable at build time.

---

## 1. Mission & context

I'm a Data Engineer / GenAI & agentic-systems engineer based in Rio de Janeiro, working toward
international / remote-first roles. I'm building a public portfolio with three simultaneous goals:

1. **Build genuinely useful things** that prove senior-level data + AI platform engineering.
2. **Learn current technologies** (streaming, lakehouse, RAG with evals, agentic systems, IaC, Spark).
3. **Attract recruiters on LinkedIn** via a coherent, well-documented body of work + build-in-public posts.

I build AI-assisted with Claude Code and want a tight, repeatable loop:
**Brainstorm → Define (ADR) → Build → Test/eval → Ship (README + diagram + CI) → Capture (notes) → Post.**

Audience = international recruiters and hiring managers who skim. Optimize for clarity, production
discipline, and a strong README on every repo.

---

## 2. Locked decisions

- **Shared domain:** one fictional company, **Meridian**, a global online marketplace (§4). Every
  project uses the same entities so the portfolio reads as ONE platform, not scattered demos.
- **Constraints:** everything must run **free and locally**; **cloud-agnostic**; prefer open standards
  (Iceberg, dbt-core, OSS) over single-vendor lock-in. All content in **English**.
- **Vector database:** **Qdrant** (chosen to learn it) — used in Project 3 (RAG) and Project 4 (agent memory). Run locally via Docker.
- **Python toolchain:** `uv` (env/deps/lock), `ruff` (lint+format), `mypy --strict` (types),
  `pytest` (+coverage), `pre-commit` with **gitleaks** secret scanning, **GitHub Actions** CI.
- **Repo strategy:** multiple repos + a profile hub README (one repo per project; a GitHub *template*
  repo they all start from; a public global-skills repo; a private Obsidian knowledge base).
- **Diagrams:** Mermaid in READMEs (render natively on GitHub). **ADRs:** MADR-style, one file per decision.

---

## 3. The portfolio roadmap (forward context — do NOT build these yet)

| # | Project | What it proves | Core stack (free/local) |
|---|---------|----------------|--------------------------|
| **L0** | **Build system** | Consistency, AI-assisted workflow | template repo · global skills · Obsidian KB |
| 1 | Batch data platform | Modern data stack, end to end | dlt · DuckDB/Iceberg · dbt-core · Dagster · Evidence |
| 2 | Streaming pipeline | Real-time, CDC, stream processing | Redpanda · Debezium · Bytewax/RisingWave · ClickHouse |
| 3 | RAG with evals | GenAI done with measurement | **Qdrant** · Ragas/DeepEval · Langfuse · text-to-SQL over P1 |
| 4 | Agentic data system | Multi-agent, MCP tools, HITL | LangGraph · MCP servers · **Qdrant** memory · Pydantic AI |
| 5 | Platform & IaC | Productionization + a live demo | Terraform · LocalStack · Docker/k3d · GH Actions |
| 6 | PySpark at scale | Distributed compute when warranted | Spark · Structured Streaming (reads P2) |

Projects compose: P1 builds the warehouse; P2 streams into it; P3 puts RAG/text-to-SQL on top of it;
P4 wraps it in agents; P5 deploys it; P6 re-implements a transform at scale.

---

## 4. The Meridian domain model

A single synthetic-data module is the source of truth for the whole platform, so ids/skus/events
align across every project. **Never hardcode the domain elsewhere — always import from it.**

**Entities** (and which project consumes them):

- `customers` (customer_id, name, email, country, signup_date, segment) — P1
- `products` (product_id/sku, title, category, price, cost, supplier_id) — P1
- `orders` (order_id, customer_id, ordered_at, status, channel) — P1
- `order_items` (order_id, product_id, qty, unit_price) — P1
- `payments` (payment_id, order_id, amount, method, status, ts) — P1 + P2 (fraud signals)
- `events` / clickstream (event_id, customer_id, session_id, event_type, product_id, ts) — P2
- `support_tickets` (ticket_id, customer_id, order_id, subject, body, created_at, status) — P3 (text)
- `reviews` (review_id, customer_id, product_id, rating, body, created_at) — P3 (text)
- `product_docs` / policies (markdown corpus: shipping, returns, FAQ) — P3 (RAG corpus)

Synthetic generation: `Faker` for static dims, a small deterministic event simulator for clickstream
and payments (feeds P2). Keep generation seeded so runs are reproducible.

---

## 5. Engineering standards (apply to every repo)

**README — fixed section order, never reorder:**
1. Title + one-line value prop (written for an 8-second skim; lead with the outcome, not the tech)
2. Badges (CI, Python, license) + live-demo / write-up links + demo GIF
3. **Why this exists** — the problem + what a senior cares about (scale, cost, correctness, observability)
4. **Architecture** — Mermaid diagram + link to `docs/adr/`
5. **Stack** — table of tool → one-line why
6. **Quickstart** — `make setup / test / run`
7. **What I learned** — honest tradeoffs; the real differentiator. Never a placeholder.
8. Roadmap / status

**ADRs:** one short MADR-style file per non-obvious decision in `docs/adr/` (Context → Decision →
Consequences). Scaffold via the `/adr` command. ADRs show architectural reasoning — they matter to
reviewers as much as the code.

**Quality (CI-enforced):** `uv` env, `ruff` lint+format, `mypy --strict` on `src`, `pytest`.
pre-commit + gitleaks must pass. **Never commit a secret** (use a local `.env`, never committed).

**Definition of done:** CI green · README complete incl. diagram · ADR(s) for key choices ·
a demo artifact (GIF or live link) · a knowledge-base note · a LinkedIn draft.

---

## 6. Claude Code setup & the five extension layers

Use the right layer for each need (don't conflate them):

- **CLAUDE.md** — always-loaded durable project context (conventions, structure). Facts, not procedures.
- **Slash commands** (`.claude/commands/*.md`) — user-invoked (`/name`). Saved prompts for explicit actions.
- **Skills** (`.claude/skills/<name>/SKILL.md`) — model-invoked automatically when the task matches the
  `description`. On-demand expertise (~100 tokens until triggered). The `description` IS the trigger:
  make it specific and slightly "pushy" or it silently never fires. Skills can bundle `scripts/`,
  `references/`, `assets/` loaded only when needed (progressive disclosure).
- **Hooks** — deterministic enforcement in the harness (future use, e.g. guard rails).
- **Subagents** — isolate a noisy sub-task in its own context (future use, e.g. research with Explore).

Skill placement: **project skills** live in `.claude/skills/` (committed with the repo);
**personal skills** live in `~/.claude/skills/` (available across all projects).

**Plan-mode loop per task:** I paste a spec → you produce a plan and list files → I approve →
you build → run `make lint typecheck test` until green → stop for review. Then I capture + post.

---

## 7. LAYER 0 — BUILD THIS NOW (detailed spec)

Goal: a reusable build system so every later project inherits the same polish. Produce a plan to
create the following, then build it. Pin latest stable versions at build time.

### 7.1 Repositories to create
1. `de-ai-platform-template` — a GitHub **template** repo; the skeleton every project starts from.
2. `<github-username>` — the profile hub repo (name must equal my GitHub username so it renders on my profile).
3. `claude-engineering-os` — public mirror of my personal/global skills (showcase).
4. `knowledge-base` — private Obsidian vault (the notes → posts pipeline).

### 7.2 `de-ai-platform-template` — file-by-file spec

**`pyproject.toml`**
- `requires-python = ">=3.12"`; deps: `faker`, `polars`, `duckdb`; dev group: `ruff`, `mypy`, `pytest`, `pytest-cov`.
- `[tool.ruff]` line-length 100, target py312; lint `select = ["E","F","I","UP","B","SIM"]`.
- `[tool.mypy]` `strict = true`, `ignore_missing_imports = true`.
- `[tool.pytest.ini_options]` `addopts = "-q --cov=src --cov-report=term-missing"`, `testpaths=["tests"]`.
- hatchling build backend; wheel packages = `src/meridian`.

**`Makefile`** targets (all via `uv run`):
- `setup` → `uv sync` + `uv run pre-commit install`
- `lint` → `ruff check .` · `fmt` → `ruff format .` + `ruff check --fix .`
- `typecheck` → `mypy src` · `test` → `pytest` · `run` → `python -m meridian` · `clean`

**`.pre-commit-config.yaml`** — ruff (with `--fix`), ruff-format, end-of-file-fixer,
trailing-whitespace, check-yaml, check-added-large-files, and **gitleaks**.

**`.github/workflows/ci.yml`** — on push to main + PRs: checkout → `astral-sh/setup-uv` →
`uv sync` → `ruff check` → `ruff format --check` → `mypy src` → `pytest`.

**`Dockerfile`** — python:3.12-slim, copy `uv` binary, `uv sync --no-dev`, default CMD runs `python -m meridian`.
**`docker-compose.yml`** — placeholder for per-project infra (Postgres/MinIO/Redpanda/Qdrant added per project).
**`.gitignore`** — `.venv`, caches, `data/*.parquet`, `data/*.duckdb`, `.env`. **`LICENSE`** — MIT.

**`src/meridian/`**
- `__init__.py` (`__version__`), `__main__.py` (prints a sample), and `synthetic.py` — the domain
  source of truth. Start with a deterministic, seeded `generate_customers(n)` returning a Polars
  DataFrame with `customer_id` like `C000001`. Structure it so other entities (§4) are added later.
- `tests/test_synthetic.py` — assert determinism (same seed → equal frames) and basic shape.

**`docs/`**
- `STANDARDS.md` — the §5 standards verbatim (README order, ADRs, quality, DoD, the Meridian rule).
- `architecture.md` — a Mermaid placeholder + pointer to ADRs.
- `adr/0001-record-architecture-decisions.md` — MADR-style; this file is also the ADR template.

**`CLAUDE.md`** (always-loaded) — canonical content:
```
# CLAUDE.md — project context for Claude Code
## What this project is
A component of the Meridian marketplace data + AI platform portfolio. Audience: international/remote
recruiters. Optimize for production discipline and a clear README.
## Conventions
- Python 3.12 via uv; ruff lint/format; mypy strict; pytest. Run everything via the Makefile.
- Synthetic data comes from meridian.synthetic — never hardcode the domain elsewhere.
- Every non-obvious decision gets an ADR in docs/adr/ (use /adr). README section order is fixed (docs/STANDARDS.md).
## Definition of done
CI green (lint+types+tests), README updated incl. Mermaid diagram, ADRs for key choices, a demo
(GIF or live link). Then a vault note + a LinkedIn draft.
## Guardrails
- Never commit secrets (gitleaks in pre-commit; use a local .env). Prefer open standards over one cloud vendor.
```

**`.claude/commands/`**
- `adr.md` — `description: Scaffold a new ADR from the template`. Body: create the next sequential
  ADR in `docs/adr/` following 0001's format; topic `$ARGUMENTS`; status Proposed.
- `ship.md` — `description: Pre-ship checklist before a commit/post`. Body: run lint/typecheck/test;
  verify README completeness (value prop, badges, demo/write-up links, Mermaid, Stack table, real
  "What I learned"); verify ≥1 ADR; verify a demo artifact; draft a commit message; stage but don't push.

**`.claude/skills/dbt-model/SKILL.md`** (project skill — worked example of authoring)
- Frontmatter:
  - `name: dbt-model`
  - `description: Scaffold a new dbt model with staging/marts layering, schema tests, and docs for the Meridian project. Use this whenever the user asks to add, create, or scaffold a dbt model, a staging model, a mart, a fact or dimension table, or mentions dbt transformations — even if they only describe the table they want rather than saying "dbt".`
- Body: layering rules (staging `stg_<source>__<entity>` as views, marts `(fct|dim)_<name>` as tables,
  marts never read sources directly); steps (pick layer+entity → write SQL with `ref()`/`source()` →
  add sibling `_<name>.yml` with model+column descriptions and tests: unique+not_null on key,
  relationships for FKs, accepted_values for enums → register new sources → remind to `dbt build --select`).
- Bundle `references/model_template.sql` (a canonical mart CTE shape) and tell the skill to read it for the SQL pattern.

### 7.3 Global skills → install into `~/.claude/skills/` (and mirror to `claude-engineering-os`)

For each, write a `SKILL.md` with a specific, pushy `description` (the trigger) and a tight body.

1. **`repo-readme-generator`** — *description:* generate/upgrade a README matching the portfolio
   standard (fixed section order, badges, Mermaid diagram, stack table, honest "What I learned").
   Trigger on any request to write/improve/polish/fix a README or "document this repo". Body: read the
   repo (deps, source tree, ADRs, Makefile), write sections in the fixed order, lead the one-liner with
   the outcome not the tech, generate Mermaid from real components, fill the stack table from real deps,
   draft "What I learned" then ask me to confirm (never invent it), never invent a live-demo link.

2. **`linkedin-post-drafter`** — *description:* draft a build-in-public LinkedIn post from a milestone,
   commit history, or ADR. Trigger on finishing a feature/project, "share on LinkedIn", build-in-public,
   or "how do I talk about this". Body: structure = hook → context → the interesting tradeoff (why) →
   lesson → soft CTA with repo link; first person, confident not boastful, 0–2 emoji, 120–200 words,
   English by default (offer a PT version), suggest 3–5 specific hashtags, note the best diagram/GIF to attach.

3. **`architecture-diagram`** — *description:* produce a clean Mermaid architecture diagram for a
   data/AI project from code or a description. Trigger on "architecture diagram", "system diagram",
   "data flow", "draw the pipeline". Body: identify real components, flowchart LR for pipelines /
   sequenceDiagram for agent flows, group with subgraphs, label edges with what flows, 6–12 boxes max,
   output a paste-ready fenced mermaid block + 2 sentences. No invented components.

### 7.4 Profile hub (`<github-username>/README.md`)
A recruiter landing page: one-line positioning (Data Engineer & GenAI/agentic, remote/international),
a short "I'm building Meridian…" intro, the §3 roadmap table (with Project 3 listing **Qdrant**), a
"How I build" line linking the skills repo and knowledge base, certifications (MCP, Snowflake Cortex,
AI agents), and LinkedIn/write-up links. Keep placeholder links until repos exist.

### 7.5 Knowledge base (`knowledge-base/`, Obsidian vault, private)
Folders: `00-inbox`, `10-projects`, `20-tech`, `30-adr`, `40-posts`, `90-meta`.
Templates: `10-projects/_project-template.md` (goal, decisions, what was hard, lessons→posts, ship
checklist); `20-tech/_tech-deep-dive-template.md` (problem it solves, mental model, minimal example,
gotchas, when to use, sources); `40-posts/_post-template.md` (hook/context/tradeoff/lesson/CTA/attach/
hashtags); `90-meta/conventions.md` (kebab-case files, tags like `#tech/dbt`, link with `[[wikilinks]]`).
A `README.md` explaining the build → inbox → process → post loop.

### 7.6 Acceptance criteria for Layer 0
- `de-ai-platform-template` exists with every file above; `make setup && make lint && make typecheck
  && make test` all pass locally; CI workflow present.
- The `dbt-model` project skill and the 3 global skills exist with valid frontmatter.
- Profile hub README and the Obsidian vault skeleton exist.
- Nothing from Projects 1–6 is built yet.

---

## 8. Qdrant primer (so you know where it lands — not built in Layer 0)

- Qdrant is an open-source vector database (Rust). Runs free locally via Docker:
  `docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant`. Python client: `qdrant-client`.
- Concepts I want to learn through use: **collections**, **points** (id + vector + JSON **payload**),
  distance metrics (Cosine/Dot), **HNSW** indexing, **payload filtering**, named/multiple vectors,
  and hybrid (dense + sparse) search.
- **Project 3 (RAG):** Qdrant stores embeddings of `support_tickets` + `reviews` + `product_docs`;
  retrieval → reranking → generation, measured with Ragas/DeepEval and traced in Langfuse. A second
  track is "chat with the warehouse" (text-to-SQL over the P1 marts).
- **Project 4 (agent):** Qdrant as the agent's long-term semantic memory alongside LangGraph + MCP tools.
- When we reach P3, add a `qdrant` service to that project's `docker-compose.yml` and (likely) a
  project skill `qdrant-collection` to scaffold collections with consistent payload schemas.

---

## 9. Your immediate task (plan mode)

Operate in **plan mode**. Produce a step-by-step plan to create **Layer 0** exactly as specified in
§7: list the files you will create per repo, call out anything ambiguous or any version you'll pin,
and **wait for my approval before writing anything**. After I approve, build it, run
`make lint typecheck test` until green, and stop for review. **Do not start Project 1.**
