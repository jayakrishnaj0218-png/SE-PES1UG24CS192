"""Branch-focused tests for blood_donation_screening."""
import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


@pytest.mark.parametrize("cohorts,volume", [("bad", 450), ([], 0), ([], -1)])
def test_invalid_inputs(cohorts, volume):
    with pytest.raises(ValueError):
        process_donor_cohort(cohorts, volume)


def test_registered_and_unregistered_cohorts():
    result = process_donor_cohort([{"clinic_registered": False, "donors": [{"age": 30, "weight_kg": 70, "hb": 15}]}, {"clinic_registered": True, "donors": [{"age": 30, "weight_kg": 70, "hb": 15}]}], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


@pytest.mark.parametrize("donor", [{"age": 16, "weight_kg": 60, "hb": 14}, {"age": 17, "weight_kg": 49, "hb": 14}, {"age": 17, "weight_kg": 50, "hb": 12.4}, {"age": 17, "weight_kg": 50, "hb": 18.1}, {"age": 17, "weight_kg": 50, "hb": 12.5}, {"age": 17, "weight_kg": 50, "hb": 18.0}])
def test_each_donor_decision_branch(donor):
    result = process_donor_cohort([{"clinic_registered": True, "donors": [donor]}], 450)
    assert result["status"] in {"ACCEPTED", "ZERO_YIELD"}


def test_high_altitude_low_hb_branch():
    result = process_donor_cohort([{"clinic_registered": True, "type": "high_altitude", "donors": [{"age": 30, "weight_kg": 70, "hb": 14}, {"age": 30, "weight_kg": 70, "hb": 12}]}], 450)
    assert result["status"] == "ZERO_YIELD"


def test_standard_low_hb_branch_does_not_break():
    result = process_donor_cohort([{"clinic_registered": True, "type": "standard", "donors": [{"age": 30, "weight_kg": 70, "hb": 12}, {"age": 30, "weight_kg": 70, "hb": 14}]}], 450)
    assert result["collected_ml"] == 450


def test_fast_track_true_and_false():
    result = process_donor_cohort([{"clinic_registered": True, "fast_track": True, "donors": []}, {"clinic_registered": True, "fast_track": False, "donors": []}], 450)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_high_deferral_precedes_zero_yield():
    donors = [{"age": 16, "weight_kg": 70, "hb": 14} for _ in range(5)]
    result = process_donor_cohort([{"clinic_registered": True, "donors": donors}], 450)
    assert result["status"] == "HIGH_DEFERRAL"


def test_zero_yield_and_accepted_final_statuses():
    assert process_donor_cohort([], 450)["status"] == "ZERO_YIELD"
    assert process_donor_cohort([{"clinic_registered": True, "donors": [{"age": 30, "weight_kg": 70, "hb": 14}]}], 450)["status"] == "ACCEPTED"


def test_centrifuge_empty_and_nonempty():
    assert verify_storage_centrifuge([]) == "NO_DATA"
    assert verify_storage_centrifuge([[3200]]) == "STABLE"


def test_centrifuge_low_rpm_then_recovery_resets_streak():
    assert verify_storage_centrifuge([[2800, 3100, 2700, 3200]]) == "STABLE"


def test_centrifuge_second_consecutive_low_rpm_aborts():
    assert verify_storage_centrifuge([[2800, 2900]]) == "ABORT_SPIN"
