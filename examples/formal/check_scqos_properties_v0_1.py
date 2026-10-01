"""Finite exhaustive checks for selected SCQOS formal-model properties."""
from itertools import product

from scqos_kernel_v0_1 import (
    HOLD,
    PERMIT,
    InvariantVector,
    boundary_pass,
    causality_pass,
    decide,
    reference_pass,
)


def check_fail_closed() -> None:
    names = (
        "time",
        "continuity",
        "alignment",
        "genesis",
        "boundary",
        "reference",
        "causality",
        "consciousness",
    )
    permit_count = 0
    for bits in product((False, True), repeat=8):
        vector = InvariantVector(**dict(zip(names, bits)))
        decision = decide(vector)
        if all(bits):
            assert decision == PERMIT
            assert vector.first_failed() is None
            permit_count += 1
        else:
            assert decision == HOLD
            expected = names[next(i for i, value in enumerate(bits) if not value)]
            assert vector.first_failed() == expected
    assert permit_count == 1


def check_release_block_is_not_ninth_invariant() -> None:
    vector = InvariantVector(*(True for _ in range(8)))
    assert vector.pass_all()
    assert decide(vector, release_admitted=False) == HOLD
def check_reference_exactness() -> None:
    requested = {"memory:1"}
    resolved = {"memory:1"}
    assert reference_pass(
        requested,
        resolved,
        {"memory:1": "aaa"},
        {"memory:1": "aaa"},
    )
    assert not reference_pass(
        requested,
        resolved,
        {"memory:1": "aaa"},
        {"memory:1": "bbb"},
    )
    assert not reference_pass(
        requested,
        {"memory:2"},
        {"memory:1": "aaa"},
        {"memory:2": "aaa"},
    )


def check_boundary_substitution_resistance() -> None:
    valid = dict(
        actual_operation="write",
        expected_operation="write",
        actual_destination="ledger",
        expected_destination="ledger",
        actual_consequence_digest="abc",
        proposed_consequence_digest="abc",
    )
    assert boundary_pass(**valid)
    for field, replacement in (
        ("actual_operation", "delete"),
        ("actual_destination", "other-ledger"),
        ("actual_consequence_digest", "xyz"),
    ):
        candidate = dict(valid)
        candidate[field] = replacement
        assert not boundary_pass(**candidate)


def check_causality_exactness() -> None:
    valid = dict(
        success=True,
        actual_transition_id="t1",
        proposed_transition_id="t1",
        produced_consequence_digest="abc",
        proposed_consequence_digest="abc",
        observation_consistent=True,
    )
    assert causality_pass(**valid)
    for field, replacement in (
        ("success", False),
        ("actual_transition_id", "t2"),
        ("produced_consequence_digest", "xyz"),
        ("observation_consistent", False),
    ):
        candidate = dict(valid)
        candidate[field] = replacement
        assert not causality_pass(**candidate)
def main() -> None:
    checks = (
        check_fail_closed,
        check_release_block_is_not_ninth_invariant,
        check_reference_exactness,
        check_boundary_substitution_resistance,
        check_causality_exactness,
    )
    for check in checks:
        check()
        print(f"PASS {check.__name__}")
    print("PASS all selected SCQOS formal-model properties")


if __name__ == "__main__":
    main()
