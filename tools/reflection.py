"""Evolution reflection tools (L1 and optional legacy L2)."""

from pathlib import Path


# L1 — update_prompt_patch
# ---------------------------------------------------------------------------

def build_update_prompt_patch_schema() -> dict:
    return {
        "name": "update_prompt_patch",
        "description": (
            "View, add, or replace your behavioral patches (rules injected into "
            "your system prompt in future sessions).\n\n"
            "**Actions:**\n"
            "- `add` — Append one new patch to the existing list.\n"
            "- `replace_all` — Replace the entire patch list with a new set. "
            "Use this to merge duplicates, remove outdated patches, or reorganize.\n\n"
            "The tool always returns your FULL current patch list after the operation.\n\n"
            "**Quality guidelines (MANDATORY):**\n"
            "- Patches MUST be general principles that apply to ANY project.\n"
            "- A patch MUST NOT mention specific file names, class names, module names, "
            "CLI flags, or library names — if it does, it's too specific.\n"
            "- Test: 'Would this help on a completely different project?' If no, generalize.\n"
            "- Prefer creating a **skill** over a text patch for multi-step workflows.\n"
            "- Do NOT record teammate observations or handoff procedures as patches. "
            "Stable capability observations are Chairman-only L2 memory; reusable "
            "coordination procedures belong in family-scoped handoff rules.\n\n"
            "NOTE: Only available during L1 reflection phase."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["add", "replace_all"],
                    "description": (
                        "'add' = append one new patch. "
                        "'replace_all' = replace entire patch list (use to merge/deduplicate/remove)."
                    ),
                },
                "patch": {
                    "type": "string",
                    "description": (
                        "For action='add': the single new patch to append. "
                        "Should be a general, actionable rule, e.g., "
                        "'Always read the full function context before making changes'."
                    ),
                },
                "patches": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "For action='replace_all': the complete list of patches to keep. "
                        "Review the current patches shown below and provide the full "
                        "desired list (merged, deduplicated, updated)."
                    ),
                },
            },
            "required": ["action"],
        },
    }


def execute_update_prompt_patch(
    *,
    _agent_name: str,
    _agent_dir: str,
    action: str = "add",
    patch: str = "",
    patches: list[str] | None = None,
) -> str:
    evo_dir = Path(_agent_dir) / "evolution"
    evo_dir.mkdir(parents=True, exist_ok=True)
    patch_file = evo_dir / "prompt_patches.md"

    existing_patches: list[str] = []
    if patch_file.exists():
        raw = patch_file.read_text(encoding="utf-8")
        for line in raw.strip().splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                existing_patches.append(stripped[2:])
            elif stripped:
                existing_patches.append(stripped)

    if action == "add":
        if not patch or not patch.strip():
            return (
                "Error: 'patch' is required when action='add'.\n\n"
                + _format_patch_list(existing_patches, _agent_name)
            )
        existing_patches.append(patch.strip())
        _write_patches(patch_file, existing_patches)
        return (
            f"Patch added for {_agent_name}.\n\n"
            + _format_patch_list(existing_patches, _agent_name)
        )

    elif action == "replace_all":
        if patches is None or not isinstance(patches, list):
            return (
                "Error: 'patches' (array) is required when action='replace_all'.\n\n"
                + _format_patch_list(existing_patches, _agent_name)
            )
        cleaned = [p.strip() for p in patches if p and p.strip()]
        if not cleaned:
            if patch_file.exists():
                patch_file.unlink()
            return (
                f"All patches cleared for {_agent_name}.\n"
                "Patch list is now empty."
            )
        _write_patches(patch_file, cleaned)
        return (
            f"Patches replaced for {_agent_name} ({len(cleaned)} patches).\n\n"
            + _format_patch_list(cleaned, _agent_name)
        )

    else:
        return (
            f"Error: unknown action '{action}'. Use 'add' or 'replace_all'.\n\n"
            + _format_patch_list(existing_patches, _agent_name)
        )


def _format_patch_list(patches: list[str], agent_name: str) -> str:
    if not patches:
        return f"**Current patches for {agent_name}: (none)**"
    lines = [f"**Current patches for {agent_name} ({len(patches)} total):**"]
    for i, p in enumerate(patches, 1):
        lines.append(f"  {i}. {p}")
    return "\n".join(lines)


def _write_patches(patch_file: Path, patches: list[str]) -> None:
    content = "\n".join(f"- {p}" for p in patches) + "\n"
    patch_file.write_text(content, encoding="utf-8")


# L1 — update_skill
# ---------------------------------------------------------------------------

def build_update_skill_schema() -> dict:
    return {
        "name": "update_skill",
        "description": (
            "Create or update a reusable skill. **Skills are your PRIMARY "
            "self-improvement tool** — prefer creating skills over adding "
            "prompt patches whenever a multi-step workflow or checklist is involved.\n\n"
            "**When to create a skill:**\n"
            "- You followed a multi-step process that could be reused → encode it\n"
            "- You wish you had a checklist to follow → create one\n"
            "- You discovered a useful workflow pattern → capture it\n"
            "- A procedure is too complex for a one-line patch → make it a skill\n\n"
            "**Example skills:**\n"
            "- `systematic-debugging`: Step-by-step debugging workflow\n"
            "- `code-impl-checklist`: Quality checks before submitting code\n"
            "- `test-design`: How to design comprehensive test suites\n\n"
            "Each skill must have YAML frontmatter (name, description, trigger) "
            "and step-by-step instructions in the body. "
            "Skills should be GENERAL (applicable across many tasks), not specific "
            "to the current problem.\n\n"
            "NOTE: Only available during L1 reflection phase."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": (
                        "Name of the skill (lowercase, hyphenated). "
                        "E.g., 'systematic-debugging', 'test-design', 'code-impl-checklist'."
                    ),
                },
                "content": {
                    "type": "string",
                    "description": (
                        "Full content of the skill file (Markdown). Must include:\n"
                        "1. YAML frontmatter with 'name', 'description', and 'trigger' fields\n"
                        "2. Step-by-step instructions in the body\n\n"
                        "Example:\n"
                        "```\n"
                        "---\n"
                        "name: systematic-debugging\n"
                        "description: Step-by-step debugging workflow\n"
                        "trigger: When tests fail or code produces unexpected output\n"
                        "---\n"
                        "1. Read the complete error message and stack trace\n"
                        "2. Locate the exact failing line\n"
                        "3. Check input values at the failure point\n"
                        "4. Trace inputs back to their source\n"
                        "5. After fixing, check for similar patterns elsewhere\n"
                        "```"
                    ),
                },
            },
            "required": ["skill_name", "content"],
        },
    }


def execute_update_skill(
    skill_name: str,
    content: str,
    *,
    _agent_name: str,
    _agent_dir: str,
) -> str:
    if not skill_name.strip():
        return "Error: skill_name cannot be empty."
    if not content.strip():
        return "Error: content cannot be empty."

    clean_name = skill_name.strip()
    if ".." in clean_name or "/" in clean_name or "\\" in clean_name:
        return "Error: skill_name contains invalid characters (path traversal not allowed)."

    skill_dir = Path(_agent_dir) / "skills" / clean_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"

    is_update = skill_file.exists()
    try:
        skill_file.write_text(content, encoding="utf-8")
    except OSError as e:
        return f"Error: could not write skill file: {e}"

    action = "updated" if is_update else "created"
    return (
        f"Skill '{skill_name}' {action} for {_agent_name}.\n"
        f"Path: {skill_file}\n"
        f"This skill will be available via use_skill in future sessions."
    )


# L1 — skip_l1_reflection
# ---------------------------------------------------------------------------

def build_skip_l1_reflection_schema() -> dict:
    return {
        "name": "skip_l1_reflection",
        "description": (
            "Skip L1 reflection — your performance was satisfactory "
            "and no self-improvement patches or skills are needed. "
            "NOTE: Only available during L1 reflection phase."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Brief reason for skipping L1 reflection.",
                },
            },
            "required": ["reason"],
        },
    }


def execute_skip_l1_reflection(
    reason: str,
    *,
    _agent_name: str,
) -> str:
    if not reason.strip():
        return "Error: reason cannot be empty."
    return (
        f"L1 reflection skipped for {_agent_name}. Reason: {reason}\n"
        f"Moving on."
    )


# L2 — update_teammate_profile
# ---------------------------------------------------------------------------

def build_update_teammate_profile_schema(teammate_names: list[str]) -> dict:
    return {
        "name": "update_teammate_profile",
        "description": (
            "Update your observations about a teammate based on this task's "
            "interactions. The profile is stored in your evolution/teammate_profiles.yaml "
            "and will be injected into your system prompt in future sessions.\n\n"
            "**Quality guidelines:** Keep profiles organized, general, and limited to useful observations. "
            "Submit the complete curated current profile for this teammate: retain useful stable patterns, "
            "consolidate similar observations, and do not merely append new items. "
            "By default, do not delete an existing observation just because you are uncertain. "
            "To remove a clearly one-off, contradicted, or obsolete item, include an optional `remove` "
            "mapping listing the exact old item under its field. "
            "Do NOT reference specific files, modules, PRs, or task details. "
            "Do not record handoff rule IDs, triggers, from/to routing, payload schemas, "
            "verification requirements, or fallback procedures; those belong to handoff_rules.json.\n\n"
            "NOTE: Only available during L2 reflection phase."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "teammate_name": {
                    "type": "string",
                    "enum": teammate_names,
                    "description": "Name of the teammate to profile.",
                },
                "profile": {
                    "type": "string",
                    "description": (
                        "YAML-formatted observations about this teammate. "
                        "Include: reliability (high/medium/low), strengths, "
                        "weaknesses, communication_style, and notes. "
                        "Optionally include remove: {strengths: [...], weaknesses: [...], notes: [...]} "
                        "for explicit, justified deletions only."
                    ),
                },
            },
            "required": ["teammate_name", "profile"],
        },
    }


def execute_update_teammate_profile(
    teammate_name: str,
    profile: str,
    *,
    _agent_name: str,
    _agent_dir: str,
) -> str:
    import yaml as _yaml

    if not teammate_name.strip():
        return "Error: teammate_name cannot be empty."
    if not profile.strip():
        return "Error: profile cannot be empty."
    if teammate_name == _agent_name:
        return "Error: cannot profile yourself. Use update_prompt_patch for self-improvement."

    evo_dir = Path(_agent_dir) / "evolution"
    evo_dir.mkdir(parents=True, exist_ok=True)
    profile_file = evo_dir / "teammate_profiles.yaml"

    existing: dict = {}
    if profile_file.exists():
        raw = profile_file.read_text(encoding="utf-8")
        if raw.strip():
            try:
                existing = _yaml.safe_load(raw) or {}
            except Exception:
                existing = {}
    if not isinstance(existing, dict):
        existing = {}

    try:
        new_profile = _yaml.safe_load(profile)
    except Exception as e:
        return f"Error: profile must be valid YAML: {e}"
    if not isinstance(new_profile, dict):
        return "Error: profile must be a YAML mapping with teammate observations."

    removal_spec = new_profile.pop("remove", {})
    if removal_spec is None:
        removal_spec = {}
    if not isinstance(removal_spec, dict):
        return "Error: remove must be a YAML mapping keyed by profile field."

    list_fields = {"strengths", "weaknesses", "notes"}

    def _items(value) -> list[str]:
        if value in (None, ""):
            return []
        values = value if isinstance(value, list) else [value]
        return [str(item).strip() for item in values if str(item).strip()]

    def _key(value: str) -> str:
        import re
        return re.sub(r"[^\w]+", "", value.casefold())

    def _coalesce(values: list[str]) -> list[str]:
        # Collapse exact and very-high-confidence lexical duplicates. Broader
        # semantic consolidation is deliberately left to the reflecting model
        # so uncertain entries are not silently lost by a heuristic.
        from difflib import SequenceMatcher
        result: list[str] = []
        for value in values:
            key = _key(value)
            duplicate_at = None
            for index, previous in enumerate(result):
                previous_key = _key(previous)
                if key == previous_key or (
                    key and previous_key
                    and SequenceMatcher(None, key, previous_key).ratio() >= 0.92
                ):
                    duplicate_at = index
                    break
            if duplicate_at is None:
                result.append(value)
            elif len(value) > len(result[duplicate_at]):
                # Prefer the more informative wording when two entries are
                # effectively the same observation.
                result[duplicate_at] = value
        return result

    old_profile = existing.get(teammate_name, {})
    if not isinstance(old_profile, dict):
        old_profile = {}
    updated = dict(old_profile)

    # Existing observations are retained by default. The model must use the
    # explicit `remove` field to discard an item after establishing that it is
    # one-off, contradicted, or obsolete. Supplied scalar fields still update
    # normally; supplied list fields are curated and deduplicated.
    for key, new_value in new_profile.items():
        if key in list_fields:
            old_items = _items(old_profile.get(key))
            requested_removals = set(_key(item) for item in _items(removal_spec.get(key)))
            kept_old = [item for item in old_items if _key(item) not in requested_removals]
            updated[key] = _coalesce(kept_old + _items(new_value))
        else:
            updated[key] = new_value

    # Explicit removals for fields omitted from the submitted profile still
    # take effect, while unknown fields are ignored rather than deleting data.
    for key in list_fields:
        if key not in new_profile and key in removal_spec:
            requested_removals = set(_key(item) for item in _items(removal_spec.get(key)))
            updated[key] = [
                item for item in _items(old_profile.get(key))
                if _key(item) not in requested_removals
            ]

    existing[teammate_name] = updated

    try:
        profile_file.write_text(
            _yaml.dump(existing, default_flow_style=False, allow_unicode=True),
            encoding="utf-8",
        )
    except OSError as e:
        return f"Error: could not write profile file: {e}"

    return (
        f"Teammate profile for '{teammate_name}' updated by {_agent_name}.\n"
        f"This will be injected into your system prompt in future sessions."
    )


# L2 — skip_l2_reflection
# ---------------------------------------------------------------------------

def build_skip_l2_reflection_schema() -> dict:
    return {
        "name": "skip_l2_reflection",
        "description": (
            "Mark L2 reflection as complete. Call this after recording relevant "
            "teammate profiles, or immediately if no "
            "interactions occurred. "
            "NOTE: Only available during L2 reflection phase."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Brief reason or summary of L2 reflection.",
                },
            },
            "required": ["reason"],
        },
    }


def execute_skip_l2_reflection(
    reason: str,
    *,
    _agent_name: str,
) -> str:
    if not reason.strip():
        return "Error: reason cannot be empty."
    return (
        f"L2 reflection skipped for {_agent_name}. Reason: {reason}\n"
        f"Moving on."
    )
