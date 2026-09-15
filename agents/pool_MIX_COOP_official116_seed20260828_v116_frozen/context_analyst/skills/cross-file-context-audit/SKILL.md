---
name: cross-file-context-audit
description: Systematically map a repository change across source files, imports, callers, and validation behavior before reporting findings.
trigger: When asked to inspect repository context or assess a cross-cutting code change
---
1. Enumerate every supplied context and solution file, distinguishing reference context from editable output.
2. Search globally for domain terms, function/class names, imports, and endpoint fields; record exact paths and line ranges.
3. Read complete surrounding definitions and all call sites, not only grep matches, to identify propagation and behavioral mismatches.
4. Compare existing and proposed interfaces, including generated values, schemas, path parameters, persistence constraints, and error semantics.
5. Check dependency availability and package import roots so newly added modules resolve from the intended source tree.
6. Report concrete snippets, locations, assumptions, and uncertainty to the lead; avoid modifying artifacts unless explicitly assigned.
7. After implementation, re-run global searches and a minimal import/behavior smoke check to catch stale callers, unused imports, and cross-file regressions.