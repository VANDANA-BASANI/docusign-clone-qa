# Recommended Code Fixes for Developers (QA Technical Insights)

**Author:** Vandana Basani (QA Intern Candidate)  
**Target:** Scaler AI Labs Engineering Team  
**Scope:** Technical root-cause suggestions for high-priority bugs reported in `bug_tracker_Vandana_Basani.xlsx`.

---

### Fix 1: BUG-001 — Enforce Recipient Validation Prior to Submission
**Module:** `app/send/(prepare)/prepare/[envelopeId]/page.tsx`  
**Issue:** Submitting with 0 recipients is accepted.  
**Proposed Fix:** Add pre-flight validation on the Next / Send action handler:

```tsx
const handleProceedToFields = () => {
  // 1. Check document exists
  if (!documents || documents.length === 0) {
    setErrorBanner("Please upload at least one document before proceeding.");
    return;
  }

  // 2. Validate at least one valid recipient exists
  const validRecipients = recipients.filter(
    (r) => r.name.trim().length > 0 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(r.email.trim())
  );

  if (validRecipients.length === 0) {
    setErrorBanner("Please add at least one recipient with a valid name and email address.");
    return;
  }

  // Proceed to canvas
  router.push(`/send/prepare/${envelopeId}/canvas`);
};
```

---

### Fix 2: BUG-002 — Canvas Placed Fields Persistence via LocalStorage / API Draft Sync
**Module:** `components/canvas/FieldPlacementCanvas.tsx`  
**Issue:** Placed signature/date tags disappear on page refresh.  
**Proposed Fix:** Sync canvas field coordinates state to local draft cache or auto-save endpoint:

```tsx
// Auto-save placed fields to draft endpoint on tag change
useEffect(() => {
  if (!envelopeId || fields.length === 0) return;

  const debounceTimer = setTimeout(async () => {
    try {
      await fetch(`/api/v1/envelopes/${envelopeId}/fields`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fields }),
      });
    } catch (err) {
      console.error("Failed to auto-save field coordinates", err);
    }
  }, 500);

  return () => clearTimeout(debounceTimer);
}, [fields, envelopeId]);
```

---

### Fix 3: BUG-005 — Clamping Drag-and-Drop Tags Inside PDF Page Boundaries
**Module:** `components/canvas/DraggableTag.tsx`  
**Issue:** Tags can be dropped into the grey outer viewport outside page margins.  
**Proposed Fix:** Clamp `(x, y)` drop coordinates to document bounding box:

```tsx
const handleDrop = (e: React.DragEvent, pageRect: DOMRect) => {
  const TAG_WIDTH = 120;
  const TAG_HEIGHT = 40;

  // Calculate coordinates relative to the page
  const rawX = e.clientX - pageRect.left;
  const rawY = e.clientY - pageRect.top;

  // Clamp within page boundaries
  const clampedX = Math.max(0, Math.min(rawX, pageRect.width - TAG_WIDTH));
  const clampedY = Math.max(0, Math.min(rawY, pageRect.height - TAG_HEIGHT));

  addField({
    type: draggedFieldType,
    page: currentPageNumber,
    x: clampedX,
    y: clampedY,
  });
};
```

---

### Fix 4: BUG-008 & BUG-009 — Pixel Fidelity: Header CTA Color & Search Padding
**Module:** `components/Header.tsx` & `components/AgreementsTable.tsx`  
**Issue:** Search text overlaps search icon, CTA button color is `#1e3a8a` instead of DocuSign `#005cb9`.  
**Proposed Fix:**

```tsx
/* Fix Search input padding in Tailwind */
<div className="relative flex items-center">
  <SearchIcon className="absolute left-3 w-4 h-4 text-gray-500 pointer-events-none" />
  {/* Change pl-5 (20px) to pl-9 (36px) to avoid text overlap */}
  <input 
    type="text" 
    placeholder="Search agreements" 
    className="pl-9 pr-4 py-2 border rounded-md text-sm focus:outline-blue-600"
  />
</div>

/* Fix Primary Button Styling */
<button className="bg-[#005cb9] hover:bg-[#004c99] text-white font-semibold px-4 py-2 rounded text-sm transition-colors">
  Start
</button>
```
