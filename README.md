# ORCA Agentic Dev — Founder Voice Team

FastAPI starter for ORCA's four role agents with AI-generated speech. Python 3.11+, no Docker.

- **Atlas** — CTO / Developer: architecture, implementation, debugging.
- **Astra** — CSO / Strategist: product direction, roadmap, prioritization.
- **Nova** — CIO / Researcher: evidence, options, risks and costs.
- **Miles** — COO / Scrum Master / Host: meeting turns, blockers, decisions and actions.

## Run locally or in Codespaces
Set `OPENAI_API_KEY` as an environment secret, then:
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open port 8000. Use the microphone or run the founder stand-up.

## Deployment
Render blueprint is included. Set `OPENAI_API_KEY` in service environment. Never commit secrets.

## Meet limitation
This app generates sequential speech in a browser voice room; it does **not** join Google Meet as a native participant. A Meet URL alone does not connect agents.