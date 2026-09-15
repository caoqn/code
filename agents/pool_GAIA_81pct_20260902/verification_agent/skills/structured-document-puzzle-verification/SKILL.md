---
name: structured-document-puzzle-verification
description: Extract and verify structured data embedded in office documents before solving entity-matching puzzles.
trigger: When a task asks for deductions from an attached DOCX or similar structured document.
---
1. Identify the attached file and inspect its container contents without modifying it.
2. Extract text and tables using a structure-preserving method (e.g., XML parsing), rather than relying only on flattened text.
3. Enumerate all entities, rows, and columns explicitly; confirm headers and directionality.
4. Build a mapping from clues/profiles to items, checking that each item is used once and noting unmatched entities.
5. Independently verify the inferred answer by reversing the mapping or checking all rows for consistency.
6. Report concise evidence to the lead, including any ambiguity in labels or assumptions and the exact requested output format.