"""Executable public abstraction of the SCQOS formal model v0.2.

This is not production SCQOS code. It is a small machine-checkable model
of selected admissibility properties described in the public documentation.
"""
from dataclasses import dataclass

PERMIT = "PERMIT"
HOLD = "HOLD"

@dataclass(frozen=True)
class InvariantVector:
    time: bool
    continuity: bool
    alignment: bool
    genesis: bool
    boundary: bool
    reference: bool
    causality: bool
    consciousness: bool

    def pass_all(self) -> bool:
        return all((
            self.time,
            self.continuity,
            self.alignment,
            self.genesis,
            self.boundary,
            self.reference,
            self.causality,
            self.consciousness,
        ))

    def first_failed(self) -> str | None:
        ordered = (
            ("time", self.time),
            ("continuity", self.continuity),
            ("alignment", self.alignment),
            ("genesis", self.genesis),
            ("boundary", self.boundary),
            ("reference", self.reference),
            ("causality", self.causality),
            ("consciousness", self.consciousness),
        )
        return next((name for name, passed in ordered if not passed), None)
def decide(invariants: InvariantVector, *, release_admitted: bool = True) -> str:
    """All invariant failures are HOLD; release admission may independently HOLD."""
    if not invariants.pass_all():
        return HOLD
    return PERMIT if release_admitted else HOLD


def reference_pass(
    requested: set[str],
    resolved: set[str],
    consumed_digests: dict[str, str],
    resolved_digests: dict[str, str],
) -> bool:
    return (
        requested == resolved
        and set(consumed_digests) == requested
        and set(resolved_digests) == resolved
        and consumed_digests == resolved_digests
    )


def boundary_pass(
    *,
    actual_operation: str,
    expected_operation: str,
    actual_destination: str,
    expected_destination: str,
    actual_consequence_digest: str,
    proposed_consequence_digest: str,
) -> bool:
    return (
        actual_operation == expected_operation
        and actual_destination == expected_destination
        and actual_consequence_digest == proposed_consequence_digest
    )


def causality_pass(
    *,
    success: bool,
    actual_transition_id: str,
    proposed_transition_id: str,
    produced_consequence_digest: str,
    proposed_consequence_digest: str,
    observation_consistent: bool,
) -> bool:
    return (
        success
        and actual_transition_id == proposed_transition_id
        and produced_consequence_digest == proposed_consequence_digest
        and observation_consistent
    )
