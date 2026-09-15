from types import SimpleNamespace

from benchmarks.adapter import _handoff_participant_ids


def test_handoff_endpoints_include_chairman_but_not_global_service_agents() -> None:
    pool = SimpleNamespace(chairman_name="plan_agent")
    result = SimpleNamespace(metadata={
        "recruited_agent_ids": [
            "web_agent",
            "verification_agent",
            "answer_agent",
        ],
        "global_service_agent_ids": ["answer_agent"],
    })

    assert _handoff_participant_ids(pool, result) == [
        "plan_agent",
        "web_agent",
        "verification_agent",
    ]


def test_handoff_endpoints_do_not_duplicate_recruited_chairman() -> None:
    pool = SimpleNamespace(chairman_name="plan_agent")
    result = SimpleNamespace(metadata={
        "recruited_agent_ids": ["plan_agent", "file_agent"],
        "global_service_agent_ids": [],
    })

    assert _handoff_participant_ids(pool, result) == [
        "plan_agent",
        "file_agent",
    ]
