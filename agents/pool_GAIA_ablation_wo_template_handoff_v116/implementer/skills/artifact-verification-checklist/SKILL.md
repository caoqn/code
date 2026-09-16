---
name: artifact-verification-checklist
description: Verify generated multi-file Python artifacts beyond syntax compilation
trigger: After copying or refactoring a Python package into a solution workspace
---
1. Enumerate all files under the output directory and confirm required package initializers exist.
2. Check source files for accidental Markdown fences or other transport-wrapper text.
3. Run syntax compilation on every generated Python file.
4. Run import smoke tests with the output directory explicitly first on PYTHONPATH, ensuring the intended source tree is imported.
5. Exercise registration, dataclass construction, and other module-level initialization paths, since these can fail at import time despite successful compilation.
6. Grep for changed function names and signatures, then inspect all callers for compatibility.
7. Report exact commands, paths, and any runtime fixes to the integrator.