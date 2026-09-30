#!/usr/bin/env python3
"""Local validator for external-authority provider onboarding manifests."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
SCHEMA_VERSION="external_authority_provider_onboarding_v1"
REQUIRED_MAPPING=("subject_id","transition_id","action_intent_digest","target_ref","scope_refs","issued_at","expires_at","nonce","evidence_ref","proof_format","proof_digest")
REQUIRED_NEGATIVE_PROBES={"changed_subject","changed_transition","changed_action_intent","wrong_target","insufficient_scope","expired_authority","wrong_envelope_digest","invalid_provider_proof"}
def _require(condition, reason):
    if not condition: raise ValueError(reason)
def validate_manifest(manifest):
    _require(type(manifest) is dict,"manifest_object_required")
    _require(manifest.get("schema_version")==SCHEMA_VERSION,"schema_version_invalid")
    pid=manifest.get("provider_id")
    _require(type(pid) is str and re.fullmatch(r"[A-Za-z0-9._:-]+",pid or "") is not None,"provider_id_invalid")
    _require(type(manifest.get("display_name")) is str and bool(manifest["display_name"].strip()),"display_name_invalid")
    _require(type(manifest.get("provider_contract_version")) is str and bool(manifest["provider_contract_version"].strip()),"provider_contract_version_invalid")
    mapping=manifest.get("envelope_mapping")
    _require(type(mapping) is dict and set(mapping)==set(REQUIRED_MAPPING),"envelope_mapping_fields_invalid")
    _require(all(type(mapping[k]) is str and bool(mapping[k].strip()) for k in REQUIRED_MAPPING),"envelope_mapping_value_invalid")
    verifier=manifest.get("verifier")
    _require(type(verifier) is dict,"verifier_invalid")
    _require(verifier.get("input_contract")=="ExternalAuthorityEnvelopeV1","verifier_input_contract_invalid")
    _require(verifier.get("output_contract")=="ExternalAuthorityVerificationV1","verifier_output_contract_invalid")
    _require(type(verifier.get("entrypoint")) is str and bool(verifier["entrypoint"].strip()),"verifier_entrypoint_invalid")
    _require(type(verifier.get("verifier_id")) is str and bool(verifier["verifier_id"].strip()),"verifier_id_invalid")
    proof=manifest.get("proof"); _require(type(proof) is dict and proof.get("verification_owner")=="provider","proof_verification_owner_invalid")
    _require(type(proof.get("proof_format")) is str and bool(proof["proof_format"].strip()),"proof_format_invalid")
    evidence=manifest.get("evidence"); _require(type(evidence) is dict,"evidence_invalid")
    for key in ("evidence_reference_semantics","verifier_receipt_reference_semantics"):
        _require(type(evidence.get(key)) is str and bool(evidence[key].strip()),f"{key}_invalid")
    failures=manifest.get("failure_semantics"); _require(type(failures) is dict,"failure_semantics_invalid")
    for key in ("adapter_exception","malformed_verification","proof_invalid"): _require(failures.get(key)=="fail_closed",f"{key}_must_fail_closed")
    probes=manifest.get("negative_probes")
    _require(type(probes) is list and set(probes)==REQUIRED_NEGATIVE_PROBES and len(probes)==len(REQUIRED_NEGATIVE_PROBES),"negative_probes_incomplete")
    safety=manifest.get("safety_boundary"); _require(type(safety) is dict,"safety_boundary_invalid")
    _require(safety.get("network_access_owned_by_provider") is True,"provider_network_ownership_required")
    _require(safety.get("scqos_writer_access") is False,"scqos_writer_access_must_be_false")
    _require(safety.get("scqos_authority_consumption") is False,"scqos_authority_consumption_must_be_false")
    _require(safety.get("live_execution_enabled") is False,"live_execution_enabled_must_be_false")
    canonical=json.dumps(manifest,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return hashlib.sha256(canonical).hexdigest()
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("manifest",type=Path); args=parser.parse_args()
    try: manifest=json.loads(args.manifest.read_text()); digest=validate_manifest(manifest)
    except (OSError,json.JSONDecodeError,ValueError) as error:
        print(f"external_authority_provider_onboarding_invalid reason={error}"); return 2
    print(f"external_authority_provider_onboarding_valid provider_id={manifest['provider_id']} manifest_digest={digest}"); return 0
if __name__=="__main__": raise SystemExit(main())
