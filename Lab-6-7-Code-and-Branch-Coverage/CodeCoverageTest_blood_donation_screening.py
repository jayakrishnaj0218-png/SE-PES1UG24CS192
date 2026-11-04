"""Tests targeting high line coverage for blood_donation_screening."""
import pytest

from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def test_accepted_donor():
    result = process_donor_cohort([{"clinic_registered": True, "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]}], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_invalid_cohort_argument():
    with pytest.raises(ValueError):
        process_donor_cohort("not-a-list", 450)


def test_non_positive_volume():
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)


def test_unregistered_cohort_is_skipped():
    assert process_donor_cohort([{"clinic_registered": False}], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_missing_donor_fields_use_defaults_and_defer():
    result = process_donor_cohort([{"clinic_registered": True, "donors": [{}]}], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_age_and_weight_deferral():
    result = process_donor_cohort([{"clinic_registered": True, "donors": [{"age": 16, "weight_kg": 60, "hb": 14}, {"age": 25, "weight_kg": 49, "hb": 14}]}], 450)
    assert result["status"] == "ZERO_YIELD"


def test_low_hb_standard_cohort_defers_but_continues():
    result = process_donor_cohort([{"clinic_registered": True, "donors": [{"age": 25, "weight_kg": 65, "hb": 12.0}, {"age": 25, "weight_kg": 65, "hb": 14.0}]}], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hb_high_altitude_resets_yield_and_breaks():
    result = process_donor_cohort([{"clinic_registered": True, "type": "high_altitude", "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}, {"age": 25, "weight_kg": 65, "hb": 12.0}, {"age": 25, "weight_kg": 65, "hb": 14.0}]}], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_hb_deferral():
    result = process_donor_cohort([{"clinic_registered": True, "donors": [{"age": 25, "weight_kg": 65, "hb": 18.1}]}], 450)
    assert result["status"] == "ZERO_YIELD"


def test_hb_boundaries_are_accepted():
    result = process_donor_cohort([{"clinic_registered": True, "donors": [{"age": 17, "weight_kg": 50, "hb": 12.5}, {"age": 18, "weight_kg": 50, "hb": 18.0}]}], 450)
    assert result == {"collected_ml": 900, "status": "ACCEPTED"}


def test_fast_track_adds_fifty_even_without_donors():
    result = process_donor_cohort([{"clinic_registered": True, "fast_track": True, "donors": []}], 450)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_more_than_four_deferrals_returns_high_deferral():
    donors = [{"age": 16, "weight_kg": 60, "hb": 14} for _ in range(5)]
    result = process_donor_cohort([{"clinic_registered": True, "donors": donors}], 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


def test_empty_cohorts_return_zero_yield():
    assert process_donor_cohort([], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_centrifuge_no_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"
    assert verify_storage_centrifuge(None) == "NO_DATA"


def test_centrifuge_stable_and_streak_reset():
    assert verify_storage_centrifuge([[3000, 2999, 3200, 2999, 3100]]) == "STABLE"


def test_centrifuge_two_consecutive_drops_abort():
    assert verify_storage_centrifuge([[3200, 2999, 2800, 3300]]) == "ABORT_SPIN"


def test_centrifuge_abort_on_later_run():
    assert verify_storage_centrifuge([[3200], [2900, 2800]]) == "ABORT_SPIN"
