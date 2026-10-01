# Examples

## Formal model

- [`formal/scqos_kernel_v0_1.py`](formal/scqos_kernel_v0_1.py) — executable public abstraction of selected SCQOS v0.2 predicates and decision rules.
- [`formal/check_scqos_properties_v0_1.py`](formal/check_scqos_properties_v0_1.py) — finite exhaustive checks for fail-closed behavior, release-block separation, exact Reference binding, Boundary substitution resistance, and Causality binding.

This directory will contain synthetic examples illustrating interoperable SCQOS events.

valid/ is for packages expected to satisfy the documented contract.

invalid/ is for intentionally malformed, expired, out-of-scope, stale-reference, or otherwise inadmissible examples used to demonstrate validation and HOLD behavior.

No production data belongs here.
