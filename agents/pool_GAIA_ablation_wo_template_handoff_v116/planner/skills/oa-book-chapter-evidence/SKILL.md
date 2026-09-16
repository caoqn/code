---
name: oa-book-chapter-evidence
description: Efficiently answer questions requiring a precise passage from an open-access book identified by DOI.
trigger: When a question cites a book DOI and asks for a fact from a specific chapter.
---
1. Resolve the DOI through the publisher or scholarly landing page and confirm title, author, and chapter/page metadata.
2. Look for openly licensed full text via the publisher, institutional repository, OAPEN, or Internet Archive; prefer downloadable EPUB/PDF over search snippets.
3. Extract text locally with EPUB/XML parsing or PDF/OCR tools and search the exact distinctive phrase from the question.
4. Read sufficient surrounding context to identify the requested entity and distinguish the book author from the author mentioned in the passage.
5. Verify the passage independently using a second source (publisher chapter preview, repository OCR, or authoritative index), checking chapter numbering and wording.
6. Provide only the requested normalized answer, preserving required capitalization and strict prefix/output format.