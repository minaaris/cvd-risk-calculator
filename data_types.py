"""
data_types.py — Custom data types for the CVD Risk Calculator.

Defines all enumerated types and data classes used across the program:
  - Sex: biological sex at birth (Male / Female)
  - Smoker: current smoking status (Current / Former / Never)
  - Risk: CVD risk classification level (Low / Intermediate / High)
  - Vital: a collection of clinical measurements for one assessment
  - User: all information about a person being assessed
"""

__author__ = "MINERVA VALENTINE"

from dataclasses import dataclass
from enum import Enum


class Sex(Enum):
    """Biological sex at birth of the person being assessed."""

    MALE = "Male"
    FEMALE = "Female"


class Smoker(Enum):
    """Current or historical smoking status of the person being assessed."""

    CURRENT = "Current"
    FORMER = "Former"
    NEVER = "Never"


class Risk(Enum):
    """Cardiovascular disease risk classification level.

    Thresholds (absolute 5-year CVD risk):
        LOW          — less than 5 %
        INTERMEDIATE — 5 % to less than 10 %
        HIGH         — 10 % or greater
    """

    LOW = "Low"
    INTERMEDIATE = "Intermediate"
    HIGH = "High"


@dataclass
class Vital:
    """Clinical measurements collected during a CVD risk assessment.

    Attributes:
        systolic_blood_pressure: Systolic blood pressure in mmHg (75–220).
        total_cholesterol: Total cholesterol level in mmol/L (0.0–30.0).
        hdl_cholesterol: HDL (good) cholesterol level in mmol/L (0.0–10.0).
        diabetes_status: True if the person has been diagnosed with diabetes.
        blood_pressure_lowering_med: True if currently taking BP-lowering medication.
        lipid_modifying_med: True if currently taking lipid-modifying (statin) medication.
        antithrombotic_med: True if currently taking antithrombotic medication.
    """

    systolic_blood_pressure: int
    total_cholesterol: float
    hdl_cholesterol: float
    diabetes_status: bool
    blood_pressure_lowering_med: bool
    lipid_modifying_med: bool
    antithrombotic_med: bool


@dataclass
class User:
    """All personal and clinical information for a person being assessed.

    Attributes:
        name: Full name of the person.
        age: Age in years (30–79, the range supported by the risk model).
        sex_at_birth: Biological sex at birth (Sex enum).
        smoking_status: Current smoking habit (Smoker enum).
        vital: Clinical measurements (Vital dataclass).
    """

    name: str
    age: int
    sex_at_birth: Sex
    smoking_status: Smoker
    vital: Vital
