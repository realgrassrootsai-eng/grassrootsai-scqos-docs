# External Authority Onboarding

This document defines the public onboarding boundary for systems that provide authority evidence to SCQOS.

## Goal

An external authority system should be able to provide evidence that SCQOS can evaluate without requiring either system to absorb the responsibilities of the other.

## Minimum onboarding questions

An integration should establish:

- Who or what issued the authority?
- What exact action or consequence is authorized?
- What resource or state is in scope?
- What constraints limit the authority?
- When does the authority become valid or expire?
- What proposal or reference state is the authority bound to?
- How is the authority authenticated or verified?
- How is replay, mutation, or reuse handled?
- What evidence will be retained for the resulting receipt?

## Boundary rule

Providing authority evidence does not itself cause a consequence. SCQOS consumes the evidence as part of an admissibility evaluation. The consequential writer remains separately gated.

## Public integration sequence

1. Produce a proposed state transition.
2. Produce or resolve authority evidence.
3. Bind both to a common reference.
4. Submit the evidence package for SCQOS evaluation.
5. Receive PERMIT or HOLD.
6. Invoke the consequential writer only after PERMIT.
7. Record the observed result and receipt.

Versioned schemas and concrete example payloads will live under /schemas and /examples.
