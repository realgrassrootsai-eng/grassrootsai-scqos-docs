# External Authority Provider Onboarding v1

This package defines what an external authority provider must hand to SCQOS before interoperability work begins. It is provider-neutral and shadow-only.

## Required handoff

A provider supplies one manifest conforming to schemas/external_authority_provider_onboarding_v1.schema.json. The manifest identifies the provider, contract version, exact field mapping into ExternalAuthorityEnvelopeV1, verifier entrypoint, proof ownership, evidence references, fail-closed behavior, required negative probes, and safety boundary.

The provider remains responsible for its own proof semantics, cryptography, credentials, and any network access needed by its verifier. SCQOS receives only the normalized envelope plus ExternalAuthorityVerificationV1.

## Exact boundary

Every provider must map subject, transition, action-intent digest, target, scopes, issued time, expiry time, nonce, evidence reference, proof format, and proof digest.

The verifier boundary is:

ExternalAuthorityEnvelopeV1 -> ExternalAuthorityVerificationV1

The verification result must bind the exact envelope digest.

## Required negative probes

Before any discussion of live authority integration, the provider must pass one exact valid event and fail closed for changed subject, changed transition, changed action intent, wrong target, insufficient scope, expired authority, wrong envelope digest, and invalid provider proof.

## Safety boundary

Onboarding grants no consequence authority. Provider network access remains provider-owned. SCQOS writer access is false. SCQOS authority consumption is false. Live execution is disabled. The validator rejects any manifest that weakens those conditions.

## Validation

Run:

python scripts/validate_external_authority_provider_onboarding.py examples/external_authority_provider_onboarding_v1.example.json

Validation is local-only and prints one deterministic manifest digest on success.

## Integration sequence

1. Provider supplies the completed manifest and real verifier interface.
2. Map provider fields to ExternalAuthorityEnvelopeV1.
3. Verify provider proof using provider-owned logic.
4. Return ExternalAuthorityVerificationV1 bound to the exact envelope digest.
5. Run the existing external-authority shadow probe and all required negative probes.
6. Preserve and compare deterministic receipts.
7. Review the evidence before considering any separate live-authority design.

AFA has not supplied a concrete schema/verifier interface in this implementation. No AFA compatibility or integration is claimed.
