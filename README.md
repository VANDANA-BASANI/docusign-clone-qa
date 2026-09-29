# Scaler AI Labs — Tech QA Take-Home Assignment: DocuSign Clone

**Candidate:** Vandana Basani  
**Target Viewport:** 1280 × 960 (Google Chrome, 100% Zoom)  
**Reference Environment:** DocuSign Enterprise Free Trial vs Scaler AI Labs Clone (`http://13.207.185.159`)  
**Audit Scope:** 38 High-Impact / Critical Quality Bugs

---

## 📌 Deliverables Overview

This repository contains the full technical QA audit deliverables for the DocuSign clone environment:

1. **`bug_tracker_Vandana_Basani.xlsx`**: Detailed bug tracker spreadsheet with **38 verified, triaged bugs** across P0–P3 severities including step-by-step reproduction flows, computed CSS measurements, and root-cause hypotheses.
2. **`summary_note.pdf`**: Half-page executive summary covering overall product impression, prioritized top 5 fixes for RL task grader reliability, scope boundaries, and assumptions.
3. **`DEVELOPER_FIX_SUGGESTIONS.md`**: Technical root-cause suggestions and TypeScript / React / Python code patches for engineering review.
4. **`qa_automation_scripts/`**: Automated diagnostic Python scripts used to probe backend APIs, inspect DOM attributes, and programmatically verify bugs.

---

## 🔍 Bug Triage Summary (38 Quality Bugs)

### Severity Breakdown:
- **P0 (Blocker):** 4 Bugs
- **P1 (Critical):** 14 Bugs
- **P2 (Major):** 16 Bugs
- **P3 (Minor / High-Impact Edge):** 4 Bugs

| Bug ID | Title | Severity | Category | Module |
| :--- | :--- | :---: | :--- | :--- |
| **BUG-001** | Send flow: Envelope can be submitted with 0 recipients without validation | **P1** | Functional / Validation | Prepare → Send |
| **BUG-002** | Field Placement: Placed signature tags do not persist on page refresh | **P1** | Functional / Persistence | Prepare → Canvas |
| **BUG-003** | Manage screen: Envelopes display static, hardcoded timestamps ("14/05/2024") | **P2** | Data Seeding / Stale Data | Manage → Agreements |
| **BUG-004** | Recipients form: Malformed email strings accepted without RFC regex validation | **P2** | Functional / Validation | Prepare → Add Recipients |
| **BUG-005** | Field Placement: Signature tag can be dropped outside document canvas bounds | **P2** | Functional / Canvas | Prepare → Canvas |
| **BUG-006** | Navigation: Browser 'Back' button drops draft envelope without confirmation modal | **P2** | Functional / Navigation | Prepare → Canvas |
| **BUG-007** | Agreements list: Status filter count badge displays static number contradictory to table rows | **P2** | Data Seeding / Sync | Dashboard & Agreements |
| **BUG-008** | Dashboard Header: Primary CTA 'Start' button has color #1e3a8a instead of DocuSign #005cb9 | **P2** | UI / Pixel Fidelity | Dashboard / Header |
| **BUG-009** | Search input: Search bar in Agreements table lacks icon padding causing text overlap | **P2** | UI / Layout & Alignment | Agreements → Table Header |
| **BUG-010** | Recipients section: Duplicate recipient emails accepted without parallel routing warning | **P3** | Functional / Edge Case | Prepare → Add Recipients |
| **BUG-011** | Document Upload: 100+ character filename overflows thumbnail card without ellipsis | **P3** | UI / Boundary Edge Case | Prepare → Document Upload |
| **BUG-012** | Footer Links: Legal and footer navigation links point to dummy '#' anchors | **P3** | Functional / Navigation | Global / Footer |
| **BUG-013** | Field Placement: 'Delete' / 'Backspace' keyboard shortcut fails to remove selected tag | **P3** | Functional / UX Interaction | Prepare → Canvas |
| **BUG-014** | DevTools Console: Uncaught TypeError logged during document thumbnail generation | **P2** | Functional / Runtime Error | Prepare → Add Documents |
| **BUG-015** | Auth / Session: Hard refresh on /send/documents prompts repeated basic auth dialog | **P2** | Functional / Session | Global / Auth |
| **BUG-016** | Envelope State Machine: PUT status='sent' succeeds on empty envelope (0 docs, 0 recipients) | **P0** | Functional / State Integrity | API / Lifecycle |
| **BUG-017** | Signing Session: Accessing /sign/[id] throws white-screen crash when envelope lacks fields | **P0** | Functional / Blocker Crash | Signer Flow → /sign/[id] |
| **BUG-018** | Document Upload: Password-protected or encrypted PDF hangs in permanent loading state | **P0** | Functional / File Handling | Prepare → Add Documents |
| **BUG-019** | Routing Engine: 'Set signing order' checkbox allows circular duplicate orders (1 -> 1 -> 1) | **P0** | Functional / Routing Rules | Prepare → Add Recipients |
| **BUG-020** | Recipient Role: 'Receives a Copy' recipient incorrectly blocks sending without signature | **P1** | Functional / Role Validation | Prepare → Recipients |
| **BUG-021** | Document Deletion: Removing primary document leaves envelope in orphaned unrecoverable state | **P1** | Functional / State Machine | Prepare → Add Documents |
| **BUG-022** | Void Envelope Flow: 'Void' modal accepts empty reason input bypassing compliance logging | **P1** | Functional / Form Validation | Manage → Details |
| **BUG-023** | Signing Signature Pad: 'Draw' tab in Adopt Signature modal fails to capture canvas strokes | **P1** | Functional / Canvas Interaction | Signer Flow → Adopt & Sign |
| **BUG-024** | Agreements Filter: Querying ?status=voided or ?status=declined returns unfiltered sent list | **P1** | Functional / API Filtering | Manage → Agreements |
| **BUG-025** | Field Duplication: Copying placed fields on canvas assigns duplicate IDs causing property sync bugs | **P1** | Functional / Canvas State | Prepare → Canvas |
| **BUG-026** | Template Application: Creating agreement from template via /use discards pre-configured roles | **P1** | Functional / Templates Workflow | Templates → Use Template |
| **BUG-027** | Multi-Document Canvas: Uploading multiple PDFs fails to concatenate pages in thumbnail rail | **P1** | Functional / Canvas Pagination | Prepare → Canvas |
| **BUG-028** | Quick Action: 'Sign a Document' dashboard action routes to prepare flow instead of signer session | **P1** | Functional / Routing | Dashboard → Quick Actions |
| **BUG-029** | Audit Trail: History / Certificate of Completion endpoint returns HTTP 404 Not Found | **P1** | Functional / Graders & Audit | API / History |
| **BUG-030** | Document Preview: Clicking 'View' on document thumbnail renders raw binary stream in modal | **P2** | UI / Component Rendering | Prepare → Add Documents |
| **BUG-031** | Page Title Fidelity: Browser tab title on signing screen renders internal string 'Rl_Docusign' | **P2** | UI / Branding Fidelity | Signer Flow → Title Tag |
| **BUG-032** | Envelope Resend: Triggering 'Resend' on an active envelope throws HTTP 400 Bad Request error | **P2** | Functional / Actions Flow | Manage → Agreements |
| **BUG-033** | Search Query: Entering special characters in agreements search breaks table rendering | **P2** | Functional / Boundary Case | Agreements → Search Bar |
| **BUG-034** | Date Signed Tag: Placed 'Date Signed' tag renders static epoch timestamp instead of local date | **P2** | Functional / Data Integrity | Signer Flow → Display |
| **BUG-035** | Dashboard Navigation: 'Expiring soon' dashboard tile links to broken query parameter | **P2** | UI / Navigation Link | Dashboard → Summary Cards |
| **BUG-036** | Email Subject: Custom email subject typed in prepare screen is overwritten on send | **P2** | Functional / Form Handling | Prepare → Message |
| **BUG-037** | Canvas Zoom Controls: Zooming scales document view without transforming field drop coordinates | **P2** | Functional / Canvas Interaction | Prepare → Canvas |
| **BUG-038** | Toast Notifications: Multiple error toasts stack and overlap primary 'Next' and 'Send' CTAs | **P2** | UI / Layout Obstruction | Prepare → Global Toasts |

---

## ⚡ QA Automation & Diagnostic Suite

Located in `qa_automation_scripts/`:
- **`test_envelope_creation_flow.py`**: Automated probe for `/api/v1/envelopes` verifying invariant failures (BUG-001 & BUG-016).
- **`audit_seeded_envelopes_api.py`**: Automated audit script checking timestamp consistency across seeded records (BUG-003 & BUG-024).
- **`inspect_ui_elements.py`**: Automated DOM crawler checking link targets and anchor attributes (BUG-012 & BUG-035).
- **`generate_sample_contract.py`**: Lightweight PDF generation script to produce standard test assets.

---

## 🛠️ Testing Methodology & Scope
- **In-Scope Audited:** Core envelope lifecycle, Drag-and-Drop canvas interactions, Recipient routing, Seeded data consistency, and DevTools computed styles.
- **Out-of-Scope (Deliberately Excluded):** PDF/CSV export downloads, third-party integrations (Drive, Slack), and security/penetration testing per assignment brief.
