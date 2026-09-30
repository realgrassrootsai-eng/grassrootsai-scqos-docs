from __future__ import annotations
import copy, importlib.util, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXAMPLE=ROOT/"examples/external_authority_provider_onboarding_v1.example.json"
VALIDATOR=ROOT/"scripts/validate_external_authority_provider_onboarding.py"
def _load_validator():
    spec=importlib.util.spec_from_file_location("provider_onboarding_validator",VALIDATOR)
    module=importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(module); return module
def _example(): return json.loads(EXAMPLE.read_text())
def test_provider_onboarding_example_is_valid_and_deterministic():
    module=_load_validator(); manifest=_example()
    assert module.validate_manifest(manifest)==module.validate_manifest(copy.deepcopy(manifest))
    assert len(module.validate_manifest(manifest))==64
def test_provider_onboarding_cli_accepts_example():
    result=subprocess.run([sys.executable,str(VALIDATOR),str(EXAMPLE)],cwd=ROOT,text=True,capture_output=True,check=False)
    assert result.returncode==0
    assert result.stdout.startswith("external_authority_provider_onboarding_valid ")
def test_provider_onboarding_rejects_invalid_provider_id():
    module=_load_validator(); manifest=_example(); manifest["provider_id"]="bad provider id"
    try: module.validate_manifest(manifest)
    except ValueError as error: assert str(error)=="provider_id_invalid"
    else: raise AssertionError("expected provider_id_invalid")
def test_provider_onboarding_rejects_wrong_output_contract():
    module=_load_validator(); manifest=_example(); manifest["verifier"]["output_contract"]="AnythingElse"
    try: module.validate_manifest(manifest)
    except ValueError as error: assert str(error)=="verifier_output_contract_invalid"
    else: raise AssertionError("expected verifier_output_contract_invalid")
def test_provider_onboarding_rejects_unsafe_writer_or_live_execution():
    module=_load_validator()
    for key,reason in (("scqos_writer_access","scqos_writer_access_must_be_false"),("live_execution_enabled","live_execution_enabled_must_be_false")):
        manifest=_example(); manifest["safety_boundary"][key]=True
        try: module.validate_manifest(manifest)
        except ValueError as error: assert str(error)==reason
        else: raise AssertionError(reason)
def test_provider_onboarding_rejects_missing_negative_probe():
    module=_load_validator(); manifest=_example(); manifest["negative_probes"].remove("wrong_envelope_digest")
    try: module.validate_manifest(manifest)
    except ValueError as error: assert str(error)=="negative_probes_incomplete"
    else: raise AssertionError("expected negative_probes_incomplete")
