"""Canonical, family-scoped persistence for inter-agent handoff rules.

中文说明：注册表保存 family 级交接规则，并维护 team family 到 handoff family
的绑定；退休规则仍保留，供审计历史使用。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.evolution_models import HandoffDecision, HandoffRule, now_iso


class HandoffRegistry:
    # 中文：这里是规则唯一性、方向 pair 和生命周期的持久化边界。
    SCHEMA_VERSION = 3

    def __init__(
        self,
        *,
        bindings: dict[str, str] | None = None,
        rules: list[HandoffRule] | None = None,
    ) -> None:
        self._bindings = dict(bindings or {})
        self._rules = list(rules or [])
        self.validate()

    def validate(self, known_agent_ids: set[str] | None = None) -> None:
        seen: set[str] = set()
        for team_family_id, handoff_family_id in self._bindings.items():
            if not str(team_family_id).strip() or not str(handoff_family_id).strip():
                raise ValueError("handoff family bindings cannot be empty")
        for rule in self._rules:
            rule.validate(known_agent_ids)
            if rule.rule_id in seen:
                raise ValueError(f"duplicate handoff rule_id: {rule.rule_id}")
            seen.add(rule.rule_id)

    def bind_team_family(self, team_family_id: str, handoff_family_id: str) -> None:
        if not team_family_id.strip() or not handoff_family_id.strip():
            raise ValueError("handoff family binding requires both ids")
        existing = self._bindings.get(team_family_id)
        if existing is not None and existing != handoff_family_id:
            raise ValueError("team family is already bound to another handoff family")
        self._bindings[team_family_id] = handoff_family_id

    def handoff_family_for(self, team_family_id: str) -> str | None:
        return self._bindings.get(team_family_id)

    def rules_for_team_family(self, team_family_id: str) -> list[HandoffRule]:
        # 中文：只返回当前绑定 family 中 active 的规则，避免把其他 family 的
        # 规则泄漏到本次团队，也避免把已退休规则展示给执行 Agent。
        # team family 通过绑定关系找到 handoff family；已退役规则保留在
        # 注册表中供审计，但不会作为当前可用规则返回。
        handoff_family_id = self.handoff_family_for(team_family_id)
        if not handoff_family_id:
            return []
        return [
            rule for rule in self._rules
            if rule.handoff_family_id == handoff_family_id and rule.status == "active"
        ]

    def list_rules(self) -> list[HandoffRule]:
        return sorted(
            self._rules,
            key=lambda rule: (rule.handoff_family_id, rule.rule_id),
        )

    def _find_target(self, decision: HandoffDecision) -> HandoffRule | None:
        # 有 ID 时精确查找；无 ID 时仅在同 family、同方向 pair 恰好只有
        # 一条有效规则时回退匹配，避免多条规则之间发生歧义更新。
        if decision.rule_id:
            return next(
                (rule for rule in self._rules if rule.rule_id == decision.rule_id),
                None,
            )
        matching = [
            rule for rule in self._rules
            if rule.handoff_family_id == decision.handoff_family_id
            and rule.from_agent == decision.from_agent
            and rule.to_agent == decision.to_agent
            and rule.status == "active"
        ]
        if len(matching) == 1:
            return matching[0]
        return None

    @staticmethod
    def _append_failure_evidence(
        rule: HandoffRule,
        evidence: dict[str, Any] | None,
    ) -> None:
        """Attach one normal-task failure observation without duplicating it."""
        if not evidence:
            return
        payload = dict(evidence)
        payload.setdefault("recorded_at", now_iso())
        # 同一任务、同一消息的失败证据只追加一次，避免重试重复累计。
        identity = (
            str(payload.get("task_id") or ""),
            str(payload.get("message_id") or ""),
        )
        if any(
            (
                str(item.get("task_id") or ""),
                str(item.get("message_id") or ""),
            ) == identity
            for item in rule.failure_evidence
        ):
            return
        rule.failure_evidence.append(payload)

    def apply_decision(
        self,
        decision: HandoffDecision,
        *,
        task_id: str,
        known_agent_ids: set[str],
        team_family_id: str | None = None,
    ) -> HandoffRule | None:
        # 先验证决策和现有注册表，再检查目标规则的 family/pair 归属。
        # 这是持久化层边界，不能因模型返回了一个已存在 ID 就直接覆盖。
        decision.validate()
        self.validate(known_agent_ids)
        if team_family_id:
            self.bind_team_family(team_family_id, decision.handoff_family_id)
        current = self._find_target(decision)
        if current is not None and (
            current.handoff_family_id != decision.handoff_family_id
            or current.from_agent != decision.from_agent
            or current.to_agent != decision.to_agent
        ):
            raise ValueError(
                "handoff_rule_id does not match the decision family or agent pair"
            )
        failure_evidence = decision.evidence.get("failure_evidence")
        if failure_evidence is not None and not isinstance(failure_evidence, dict):
            raise ValueError("handoff failure_evidence must be an object")
        if decision.action == "no_update":
            return current
        if decision.action == "retain":
            if current is None:
                raise ValueError("handoff retain requires an existing rule")
            self._append_failure_evidence(current, failure_evidence)
            if task_id and task_id not in current.evidence_task_ids:
                current.evidence_task_ids.append(task_id)
            return current
        if decision.action == "create":
            rule_id = decision.rule_id
            if any(rule.rule_id == rule_id for rule in self._rules):
                raise ValueError(f"handoff rule_id already exists: {rule_id}")
            rule = HandoffRule(
                handoff_family_id=decision.handoff_family_id,
                from_agent=decision.from_agent,
                to_agent=decision.to_agent,
                version=1,
                instruction=decision.instruction,
                trigger_description=decision.trigger_description,
                payload_schema=dict(decision.payload_schema),
                required_evidence=list(decision.required_evidence),
                verification=decision.verification,
                fallback=decision.fallback,
                context_notes=decision.context_notes,
                evidence_task_ids=[task_id] if task_id else [],
                failure_evidence=[
                    {**dict(failure_evidence), "recorded_at": now_iso()}
                ] if failure_evidence else [],
                rule_id=rule_id,
            )
            rule.validate(known_agent_ids)
            self._rules.append(rule)
            self.validate(known_agent_ids)
            return rule
        if decision.action == "retire":
            if current is None:
                raise ValueError("handoff retire requires an existing rule")
            current.version_history.append({
                "version": current.version,
                "instruction": current.instruction,
                "trigger_description": current.trigger_description,
                "payload_schema": current.payload_schema,
                "required_evidence": current.required_evidence,
                "verification": current.verification,
                "fallback": current.fallback,
                "context_notes": current.context_notes,
                "failure_evidence": list(current.failure_evidence),
                "reason": decision.reason,
                "task_id": task_id,
                "changed_at": now_iso(),
                "status": "retired",
            })
            self._append_failure_evidence(current, failure_evidence)
            current.status = "retired"
            if task_id and task_id not in current.evidence_task_ids:
                current.evidence_task_ids.append(task_id)
            current.validate(known_agent_ids)
            return current
        if current is None:
            raise ValueError("handoff refine requires an existing rule")
        current.version_history.append({
            "version": current.version,
            "instruction": current.instruction,
            "trigger_description": current.trigger_description,
            "payload_schema": current.payload_schema,
            "required_evidence": current.required_evidence,
            "verification": current.verification,
            "fallback": current.fallback,
            "context_notes": current.context_notes,
            "failure_evidence": list(current.failure_evidence),
            "reason": decision.reason,
            "task_id": task_id,
            "changed_at": now_iso(),
            "status": current.status,
        })
        self._append_failure_evidence(current, failure_evidence)
        current.version += 1
        current.instruction = decision.instruction
        current.trigger_description = decision.trigger_description
        current.payload_schema = dict(decision.payload_schema)
        current.required_evidence = list(decision.required_evidence)
        current.verification = decision.verification
        current.context_notes = decision.context_notes
        current.fallback = decision.fallback
        if task_id and task_id not in current.evidence_task_ids:
            current.evidence_task_ids.append(task_id)
        current.validate(known_agent_ids)
        return current

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema_version": self.SCHEMA_VERSION,
            "bindings": dict(sorted(self._bindings.items())),
            "rules": [rule.to_dict() for rule in self.list_rules()],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "HandoffRegistry":
        if not isinstance(payload, dict):
            raise ValueError("handoff registry must be an object")
        version = int(payload.get("schema_version") or 0)
        if version not in {1, 2, cls.SCHEMA_VERSION}:
            raise ValueError(f"unsupported handoff registry schema_version: {version}")
        bindings = payload.get("bindings", {})
        rows = payload.get("rules", [])
        if not isinstance(bindings, dict) or not isinstance(rows, list):
            raise ValueError("handoff registry bindings/rules have invalid types")
        normalized_rows = []
        for index, row in enumerate(rows):
            item = dict(row)
            item.setdefault(
                "trigger_description",
                f"Use when this handoff is needed: {str(item.get('instruction') or '').strip()}",
            )
            # Schema v1 had no rule id and could contain only one rule per pair.
            # Preserve those rules with deterministic ids during migration.
            item.setdefault(
                "rule_id",
                f"hr_legacy_{index + 1}_{str(item.get('from_agent') or 'agent')[:24]}",
            )
            normalized_rows.append(item)
        return cls(
            bindings={str(k): str(v) for k, v in bindings.items()},
            rules=[HandoffRule(**row) for row in normalized_rows],
        )

    @classmethod
    def load(cls, path: str | Path) -> "HandoffRegistry":
        target = Path(path)
        if not target.exists():
            return cls()
        return cls.from_dict(json.loads(target.read_text(encoding="utf-8")))

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_suffix(target.suffix + ".tmp")
        temp.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        temp.replace(target)
