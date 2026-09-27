# Scaler AI Labs — Tech QA Take-Home Assignment: DocuSign Clone

**Candidate:** Vandana Basani  
**Target Viewport:** 1280 × 960 (Google Chrome, 100% Zoom)  
**Reference Environment:** DocuSign Enterprise Free Trial vs Scaler AI Labs Clone (`http://13.207.185.159`)

---

## 📌 Deliverables Overview

This repository contains the complete technical QA audit deliverables for the DocuSign clone environment:

1. **`bug_tracker_Vandana_Basani.xlsx`**: Detailed bug tracker spreadsheet with 15 verified, triaged bugs across P1–P4 severities including reproduction steps, computed CSS measurements, and root-cause hypotheses.
2. **`summary_note.pdf`**: Half-page executive summary covering overall product impression, prioritized top 5 fixes for RL task grader reliability, scope boundaries, and assumptions.
3. **`DEVELOPER_FIX_SUGGESTIONS.md`**: Technical root-cause suggestions and TypeScript / React / Tailwind code patches for engineering team review.
4. **`qa_automation_scripts/`**: Automated diagnostic Python scripts used to probe backend APIs, inspect DOM attributes, and programmatically verify bugs.

---

## 🔍 Bug Triage Summary

| Bug ID | Title | Severity | Category | Module |
| :--- | :--- | :---: | :--- | :--- |
| **BUG-001** | Send flow: Envelope can be submitted with 0 recipients without validation | **P1** | Functional / Validation | Prepare → Send |
| **BUG-002** | Field Placement: Placed signature tags do not persist on page refresh | **P1** | Functional / Persistence | Prepare → Canvas |
| **BUG-003** | Manage screen: Envelopes display static, hardcoded timestamps ("14/05/2024") | **P2** | Data Seeding / Stale Data | Manage → Agreements |
| **BUG-004** | Recipients form: Malformed email strings accepted without RFC regex validation | **P2** | Functional / Validation | Prepare → Add Recipients |
| **BUG-005** | Field Placement: Signature tag can be dropped outside document canvas bounds | **P2** | Functional / Canvas | Prepare → Canvas |
| **BUG-006** | Navigation: Browser 'Back' button drops draft envelope without confirmation modal | **P2** | Functional / Navigation | Prepare → Canvas |
| **BUG-007** | Agreements list: Status filter count badge displays static number contradictory to table rows | **P3** | Data Seeding / Sync | Dashboard & Agreements |
| **BUG-008** | Dashboard Header: Primary CTA 'Start' button has color #1e3a8a instead of DocuSign #005cb9 | **P3** | UI / Pixel Fidelity | Dashboard / Header |
| **BUG-009** | Search input: Search bar in Agreements table lacks icon padding causing text overlap | **P3** | UI / Layout & Alignment | Agreements → Table Header |
| **BUG-010** | Recipients section: Duplicate recipient emails accepted without parallel routing warning | **P3** | Functional / Edge Case | Prepare → Add Recipients |
| **BUG-011** | Document Upload: 100+ character filename overflows thumbnail card without ellipsis | **P4** | UI / Boundary Edge Case | Prepare → Document Upload |
| **BUG-012** | Footer Links: Legal and footer navigation links point to dummy '#' anchors | **P4** | Functional / Navigation | Global / Footer |
| **BUG-013** | Field Placement: 'Delete' / 'Backspace' keyboard shortcut fails to remove selected tag | **P3** | Functional / UX Interaction | Prepare → Canvas |
| **BUG-014** | DevTools Console: Uncaught TypeError logged during document thumbnail generation | **P2** | Functional / Runtime Error | Prepare → Add Documents |
| **BUG-015** | Auth / Session: Hard refresh on /send/documents prompts repeated basic auth dialog | **P2** | Functional / Session | Global / Auth |

---

## ⚡ QA Automation & Diagnostic Suite

Located in `qa_automation_scripts/`:
- **`test_envelope_creation_flow.py`**: Automated probe for `/api/v1/envelopes` to verify zero-recipient submission bug (BUG-001).
- **`audit_seeded_envelopes_api.py`**: Automated audit script checking timestamp consistency across seeded records (BUG-003).
- **`inspect_ui_elements.py`**: Automated DOM crawler checking link targets and anchor attributes (BUG-012).
- **`generate_sample_contract.py`**: Lightweight PDF generation script to produce standard test assets.

---

## 🛠️ Testing Methodology & Scope
- **In-Scope Audited:** Core envelope lifecycle, Drag-and-Drop canvas interactions, Recipient routing, Seeded data consistency, and DevTools computed styles.
- **Out-of-Scope (Deliberately Excluded):** PDF/CSV export downloads, third-party integrations (Drive, Slack), and security/penetration testing per assignment brief.
