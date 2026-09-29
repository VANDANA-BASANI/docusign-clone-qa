# Recommended Code Fixes for Developers (QA Technical Insights)

**Author:** Vandana Basani (QA Intern Candidate)  
**Target:** Scaler AI Labs Engineering Team  
**Scope:** Technical root-cause suggestions for high-priority and critical bugs reported in `bug_tracker_Vandana_Basani.xlsx`.

---

### Fix 1: BUG-016 (P0) — Enforce Envelope State Machine Invariants on Status Mutation
**Module:** Backend API (`controllers/envelopes.py` / `models/envelope.py`)  
**Issue:** `PUT /api/v1/envelopes/{id}` allows transitioning empty envelopes (0 documents, 0 recipients) to `sent`.  
**Proposed Fix:** Add an invariant validation guard prior to state transition:

```python
@router.put("/envelopes/{envelope_id}")
async def update_envelope(envelope_id: int, payload: EnvelopeUpdateSchema, db: Session = Depends(get_db)):
    envelope = db.query(Envelope).filter(Envelope.id == envelope_id).first()
    if not envelope:
        raise HTTPException(status_code=404, detail="Envelope not found")

    if payload.status == EnvelopeStatus.SENT:
        # 1. Enforce at least one document
        if not envelope.documents or len(envelope.documents) == 0:
            raise HTTPException(
                status_code=422, 
                detail="Envelope must contain at least one document before being sent."
            )
        # 2. Enforce at least one recipient
        if not envelope.recipients or len(envelope.recipients) == 0:
            raise HTTPException(
                status_code=422, 
                detail="Envelope must contain at least one recipient with valid credentials."
            )
        # 3. Enforce field assignment for signers
        signers = [r for r in envelope.recipients if r.recipient_type == RecipientType.SIGNER]
        for s in signers:
            assigned_fields = [f for f in envelope.fields if f.recipient_id == s.id]
            if len(assigned_fields) == 0:
                raise HTTPException(
                    status_code=422, 
                    detail=f"Signer '{s.name}' ({s.email}) must have at least one field assigned."
                )

    envelope.status = payload.status
    envelope.sent_at = datetime.utcnow()
    db.commit()
    return envelope
```

---

### Fix 2: BUG-017 (P0) — Fieldless Signing Session Fallback to Prevent White-Screen Crash
**Module:** Frontend Signing View (`app/sign/[envelopeId]/page.tsx`)  
**Issue:** Undefined fields array crashes the React component during filter execution.  
**Proposed Fix:** Provide default array fallbacks and render an empty-state informative banner:

```tsx
export default function SigningPage({ envelope }: { envelope: EnvelopeDetails }) {
  // Safe fallback for fields array
  const fields = envelope?.fields ?? [];
  const documents = envelope?.documents ?? [];

  if (fields.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-50">
        <div className="max-w-md p-6 bg-white rounded-lg shadow-md border text-center">
          <InfoIcon className="w-12 h-12 text-blue-600 mx-auto mb-3" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Review Document</h2>
          <p className="text-sm text-gray-600 mb-4">
            There are no signature fields assigned to you on this agreement. Please review the contents and click Complete.
          </p>
          <button 
            onClick={handleCompleteReview} 
            className="w-full bg-[#005cb9] hover:bg-[#004c99] text-white font-semibold py-2 px-4 rounded"
          >
            Finish Review
          </button>
        </div>
      </div>
    );
  }

  return <SigningCeremonyCanvas envelope={envelope} fields={fields} documents={documents} />;
}
```

---

### Fix 3: BUG-024 (P1) — Backend Query Filtering by Status Param
**Module:** Backend Agreements Controller (`controllers/envelopes.py`)  
**Issue:** `?status=voided` or `?status=declined` query params are ignored in SQL builder.  
**Proposed Fix:**

```python
@router.get("/envelopes")
async def list_envelopes(
    status: Optional[str] = Query(None),
    view: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Envelope).filter(Envelope.is_deleted == False)

    # Apply strict status filtering
    if status:
        query = query.filter(Envelope.status == status.lower())
    elif view == "sent":
        query = query.filter(Envelope.status.in_([EnvelopeStatus.SENT, EnvelopeStatus.DELIVERED]))
    elif view == "completed":
        query = query.filter(Envelope.status == EnvelopeStatus.COMPLETED)
    elif view == "action-required":
        query = query.filter(Envelope.status == EnvelopeStatus.DELIVERED)

    if search:
        query = query.filter(Envelope.subject.ilike(f"%{search}%"))

    return {"envelopes": query.order_by(Envelope.created_at.desc()).all()}
```

---

### Fix 4: BUG-002 & BUG-037 — Canvas Field Auto-Save and Zoom Coordinate Matrix Scaling
**Module:** `components/canvas/FieldPlacementCanvas.tsx`  
**Issue:** Unsaved canvas tags on refresh and coordinate drift when zoomed.  
**Proposed Fix:**

```tsx
const handleDropField = (e: React.DragEvent, pageIndex: number) => {
  const canvasRect = canvasRef.current.getBoundingClientRect();
  
  // Divide by current zoom scale factor to normalize coordinates
  const normalizedX = (e.clientX - canvasRect.left) / zoomScale;
  const normalizedY = (e.clientY - canvasRect.top) / zoomScale;

  const newField: CanvasField = {
    id: crypto.randomUUID(),
    field_type: draggedFieldType,
    page_number: pageIndex + 1,
    x_position: Math.round(normalizedX),
    y_position: Math.round(normalizedY),
    recipient_id: activeRecipientId
  };

  setFields((prev) => [...prev, newField]);
  
  // Persist immediately to draft API
  syncDraftFields(envelopeId, [...fields, newField]);
};
```
