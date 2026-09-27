# QA Automation & Diagnostic Scripts

This directory contains automated Python scripts used during the QA audit of the DocuSign clone (`http://13.207.185.159`).

### 1. `test_envelope_creation_flow.py`
* **Purpose:** Programmatically tests the envelope creation API (`POST /api/v1/envelopes`).
* **Bug Verified:** Confirms **BUG-001** (backend accepts empty payload `{}` and creates an envelope without enforcing recipient validation).
* **Usage:** `python test_envelope_creation_flow.py`

### 2. `audit_seeded_envelopes_api.py`
* **Purpose:** Queries the inbox agreements list (`GET /api/v1/envelopes?view=inbox`) to inspect seeded mock data.
* **Bug Verified:** Confirms **BUG-003** (detects hardcoded static dates and contradictory status counts).
* **Usage:** `python audit_seeded_envelopes_api.py`

### 3. `generate_sample_contract.py`
* **Purpose:** Generates a lightweight, valid single-page PDF agreement (`sample_nda.pdf`) for consistent, reproducible drag-and-drop canvas testing.
* **Usage:** `python generate_sample_contract.py`

### 4. `inspect_ui_elements.py`
* **Purpose:** Scrapes the rendered HTML to audit navigation links and button actions.
* **Bug Verified:** Catches **BUG-012** (identifies empty href `#` placeholder anchors across legal footer links).
* **Usage:** `python inspect_ui_elements.py`
