---
name: structured-clue-puzzle-extraction
description: Extract and solve relationship puzzles from documents while keeping role directions and evidence explicit.
trigger: When a document combines people, assignments, preference profiles, and incomplete or matching clues.
---
1. Extract every relevant document element, including paragraphs, tables, headings, and labels; preserve table column names and row direction.
2. Normalize the entities into separate lists: participants, directed assignments, profiles, and available clues/items.
3. Match each item to a profile using explicit preference evidence, recording both the matched recipient and the supporting preference.
4. Reconcile item-to-recipient matches with assignment direction: use the table headers and verify the role mapping across multiple rows before concluding who acted or failed to act.
5. Distinguish carefully between the person missing an item and the person responsible for giving them one; these are often different answers.
6. Send the coordinator a compact evidence table or mapping plus the final conclusion, clearly flagging any header ambiguity rather than issuing multiple speculative conclusions.
