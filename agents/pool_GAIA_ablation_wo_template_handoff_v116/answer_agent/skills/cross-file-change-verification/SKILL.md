---
name: cross-file-change-verification
description: Systematically verify repository-wide changes, imports, and edge cases before reporting completion
trigger: When a task modifies shared utilities, APIs, or behavior across multiple files
---
1. Map the requirement to every likely affected layer (utility, public exports, callers, API boundaries, tests, and packaging).
2. Search all references to changed symbols and signatures; inspect each caller for compatibility and import correctness.
3. Confirm the edited source is the one actually imported by the project (especially when duplicate source/install trees exist).
4. Run syntax/compile checks, focused behavioral tests for valid and invalid inputs, and import/registry smoke tests.
5. Review diffs and file lists to ensure all required artifacts are under the expected output directory and no accidental formatting or fence artifacts remain.
6. Report concrete evidence, including checks that could not run due to missing dependencies, before finalizing.