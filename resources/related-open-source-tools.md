# Related Open-Source Incident Response Tools

This repository focuses on playbooks, working execution tooling, and templates built from direct practitioner experience — it intentionally doesn't try to be a comprehensive tool index. For that, the community-maintained [awesome-incident-response](https://github.com/meirwah/awesome-incident-response) list is the canonical, far more comprehensive resource.

What follows is a short, opinionated pointer list — organized around where each tool would fit alongside what's already in this repo — for anyone wanting to go from "playbook on paper" to "full IR program tooling."

## Case & Incident Management Platforms
This repo's [`playbook-tracker`](tooling/playbook-tracker/) is intentionally lightweight — a single-analyst CLI, not a team platform. For multi-analyst case management with a web UI:
- **[TheHive](https://thehive-project.org/)** — scalable, widely-deployed open-source incident management platform built for SOCs/CSIRTs
- **[Fast Incident Response (FIR)](https://github.com/certsocietegenerale/FIR/)** — lightweight, agile incident tracking and reporting
- **[DFIRTrack](https://github.com/dfirtrack/dfirtrack)** — incident tracking across cases, tasks, and affected systems at scale

## SOAR / Automation Platforms
Where this repo's playbooks describe the *decisions* to make, a SOAR platform automates the *execution* of the containment/response actions themselves:
- **[Shuffle](https://github.com/frikky/Shuffle)** — general-purpose open-source security automation platform
- **[Catalyst](https://github.com/SecurityBrewery/catalyst)** — free SOAR system for alert handling and IR process automation
- **[Cortex XSOAR](https://www.paloaltonetworks.com/cortex/xsoar)** — commercial SOAR with extensive integration library, common in enterprise environments (see also [siem-soar-detection-engineering](https://github.com/mrezwanulbari/siem-soar-detection-engineering) for the detection-side playbooks that feed a SOAR platform)

## Fleet-Wide Remote Forensics
Beyond single-host response, for investigating across many endpoints at once:
- **[GRR Rapid Response](https://github.com/google/grr)** — Google's remote live forensics framework
- **[Velociraptor](https://github.com/Velocidex/velociraptor)** — endpoint visibility and evidence collection at scale (also referenced in [digital-forensics-dfir-toolkit](https://github.com/mrezwanulbari/digital-forensics-dfir-toolkit/blob/main/resources/related-open-source-tools.md))
- **[osquery](https://osquery.io/)** — SQL-queryable endpoint state across Linux/macOS/Windows fleets, ships with an incident-response query pack out of the box

## Forensic Collection Orchestration
- **[DFTimewolf](https://github.com/log2timeline/dftimewolf)** — orchestrates forensic collection, processing, and export across a case, complementing the manual chain-of-custody approach in this repo's companion [digital-forensics-dfir-toolkit](https://github.com/mrezwanulbari/digital-forensics-dfir-toolkit)

---

For comprehensive coverage across every IR category (knowledge bases, communities, books, sandboxing tools, and dozens more), see [awesome-incident-response](https://github.com/meirwah/awesome-incident-response).

*Part of the [incident-response-playbooks](README.md) repository.*
