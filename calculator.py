"""
calculator.py — CVD risk scoring and classification logic.

A simplified cardiovascular disease (CVD) risk calculator
inspired by the AustralianCVD risk guidelines
https://www.cvdcheck.org.au/?utm_source=website&utm_medium=referral&utm_content=guideline-page.

IMPORTANT
-----------------
This program is just a proof of concept.
Results are illustrative only and must NOT be used
for real clinical decision-making.

Key risk factors included:
  - Age and sex
  - Systolic blood pressure (and BP-lowering medication use)
  - Total-to-HDL cholesterol ratio (and lipid-modifying medication)
  - Smoking status
  - Diabetes status
  - Antithrombotic medication use

Risk thresholds (5-year absolute CVD risk):
  LOW          < 5 %
  INTERMEDIATE  5 % - 9.9 %
  HIGH         ≥ 10 %
"""

__author__ = "MINERVA VALENTINE"

from data_types import Risk, Sex, Smoker, User, Vital

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOW_THRESHOLD: float = 5.0
HIGH_THRESHOLD: float = 10.0

# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def calculate_risk(user: User) -> float:
    """Calculate the estimated 5-year absolute CVD risk score for a user.

    Uses a simplified point-scoring model based on known clinical risk
    factors from the Australian CVD risk guidelines.

    Parameters:
        user: User, the person being assessed (includes age, sex, vital signs).

    Returns:
        float, estimated percentage risk of a CVD event within 5 years (0–100).
    """

    score: float = 0.0

    score += _age_score(user.age, user.sex_at_birth)
    score += _blood_pressure_score(
        user.vital.systolic_blood_pressure,
        user.vital.blood_pressure_lowering_med,
    )
    score += _cholesterol_score(
        user.vital.total_cholesterol,
        user.vital.hdl_cholesterol,
        user.vital.lipid_modifying_med,
    )
    score += _smoking_score(user.smoking_status)
    score += _diabetes_score(user.vital.diabetes_status, user.sex_at_birth)
    score += _antithrombotic_score(user.vital.antithrombotic_med)

    # Clamp to a realistic 0–100 range
    return max(0.0, min(score, 100.0))


def classify_risk(score: float) -> Risk:
    """Classify a raw CVD risk score into a Risk level.

    Parameters:
        score: float, the estimated 5-year CVD risk percentage (0–100).

    Returns:
        Risk.LOW if score < 5 %,
        Risk.INTERMEDIATE if 5 % ≤ score < 10 %,
        Risk.HIGH if score ≥ 10 %.
    """

    if score < LOW_THRESHOLD:
        return Risk.LOW
    elif score < HIGH_THRESHOLD:
        return Risk.INTERMEDIATE
    else:
        return Risk.HIGH


def get_risk_advice(risk: Risk) -> str:
    """Return a plain-English recommendation for a given risk classification.

    Parameters:
        risk: Risk, the classified risk level.

    Returns:
        str, a clinical recommendation string appropriate for the risk level.
    """

    advice: dict[Risk, str] = {
        Risk.LOW: (
            "Your estimated CVD risk is LOW (< 5 % over 5 years).\n"
            "  • Maintain a healthy lifestyle: regular exercise, balanced diet.\n"
            "  • Have a follow-up risk assessment every 2 years.\n"
            "  • Discuss any concerns with your GP."
        ),
        Risk.INTERMEDIATE: (
            "Your estimated CVD risk is INTERMEDIATE (5–9.9 % over 5 years).\n"
            "  • Lifestyle modification is strongly recommended.\n"
            "  • Your GP may consider preventive medication.\n"
            "  • Annual review of risk factors is advised."
        ),
        Risk.HIGH: (
            "Your estimated CVD risk is HIGH (≥ 10 % over 5 years).\n"
            "  • Seek medical review promptly.\n"
            "  • Preventive medication (statins, antihypertensives) is\n"
            "    likely recommended by Australian guidelines.\n"
            "  • Significant lifestyle changes are essential."
        ),
    }

    return advice[risk]


# ---------------------------------------------------------------------------
# Private helper functions (not intended for direct use outside this module)
# ---------------------------------------------------------------------------


def _age_score(age: int, sex: Sex) -> float:
    """Compute a base risk score from age and sex.

    Men generally have higher CVD risk than women at the same age.
    Risk increases with age.

    Parameters:
        age: int, the person's age in years.
        sex: Sex, the person's biological sex at birth.

    Returns:
        float, the age/sex component of the risk score.
    """

    # Base score: 0.15 per year of age
    base: float = age * 0.15

    # Sex modifier: men carry roughly 1.5× the risk of women at the same age
    if sex == Sex.MALE:
        return base * 1.0
    else:
        return base * 0.65


def _blood_pressure_score(systolic_bp: int, on_bp_med: bool) -> float:
    """Calculate risk contribution from systolic blood pressure.

    Higher blood pressure increases CVD risk.  BP-lowering medication
    indicates the pressure is already managed but underlying risk exists.

    Parameters:
        systolic_bp: int, systolic blood pressure in mmHg.
        on_bp_med: bool, True if the person takes BP-lowering medication.

    Returns:
        float, the blood pressure component of the risk score.
    """

    score: float = 0.0

    # Score based on BP category
    if systolic_bp >= 180:
        score = 4.5
    elif systolic_bp >= 160:
        score = 3.0
    elif systolic_bp >= 140:
        score = 1.5
    elif systolic_bp >= 120:
        score = 0.5
    else:
        score = 0.0

    # Extra risk if BP medication is needed (indicates treated hypertension)
    if on_bp_med:
        score += 1.0

    return score


def _cholesterol_score(total_chol: float, hdl_chol: float, on_lipid_med: bool) -> float:
    """Compute risk contribution from cholesterol levels.

    Uses the total-cholesterol-to-HDL ratio.  A higher ratio indicates
    greater risk.  Lipid-modifying medication adds background risk.

    Parameters:
        total_chol: float, total cholesterol in mmol/L.
        hdl_chol: float, HDL cholesterol in mmol/L.
        on_lipid_med: bool, True if taking lipid-modifying medication.

    Returns:
        float, the cholesterol component of the risk score.
    """

    # Avoid division by zero
    if hdl_chol <= 0.0:
        ratio: float = total_chol
    else:
        ratio = total_chol / hdl_chol

    score: float = 0.0

    if ratio >= 7.0:
        score = 3.5
    elif ratio >= 5.0:
        score = 2.0
    elif ratio >= 4.0:
        score = 1.0
    elif ratio >= 3.0:
        score = 0.5
    else:
        score = 0.0

    if on_lipid_med:
        score += 0.5

    return score


def _smoking_score(smoking_status: Smoker) -> float:
    """Compute risk contribution from smoking status.

    Current smokers have the highest risk; former smokers retain some
    elevated risk; never-smokers have no additional contribution.

    Parameters:
        smoking_status: Smoker, the person's current/former/never status.

    Returns:
        float, the smoking component of the risk score.
    """

    if smoking_status == Smoker.CURRENT:
        return 2.5
    elif smoking_status == Smoker.FORMER:
        return 1.0
    else:
        return 0.0


def _diabetes_score(has_diabetes: bool, sex: Sex) -> float:
    """Compute risk contribution from diabetes status.

    Diabetes is a significant CVD risk factor, particularly in women.

    Parameters:
        has_diabetes: bool, True if diagnosed with diabetes.
        sex: Sex, the person's biological sex at birth.

    Returns:
        float, the diabetes component of the risk score.
    """

    if not has_diabetes:
        return 0.0

    # Diabetes raises risk more in females (stronger relative effect)
    if sex == Sex.FEMALE:
        return 2.5
    else:
        return 1.5


def _antithrombotic_score(on_antithrombotic: bool) -> float:
    """Compute risk contribution from antithrombotic medication use.

    Antithrombotic use (e.g., aspirin) typically indicates an existing
    cardiovascular condition or elevated clotting risk.

    Parameters:
        on_antithrombotic: bool, True if taking antithrombotic medication.

    Returns:
        float, the antithrombotic component of the risk score.
    """

    if on_antithrombotic:
        return 1.0
    else:
        return 0.0
