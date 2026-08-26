"""
main.py

Main execution module for the Cardiovascular Disease (CVD) Risk Calculator.
Call user input validation, risk scoring, and session history management.
"""

__author__ = "MINERVA VALENTINE"

from data_types import User, Sex, Smoker, Vital, Risk
from calculator import calculate_risk, classify_risk, get_risk_advice
from input_handler import input_int, input_float, input_bool, input_menu

# Global Session Collections
users: list[User] = []
scores: list[float] = []


def input_name() -> str:
    """
    Prompts and validates the user's full name.

    Returns:
        str: Validated alphabetical name string.
    """
    while True:
        name = input("Enter full name: ")
        if name.replace(" ", "").isalpha() and len(name.strip()) > 0:
            return name.strip()
        print("Invalid name. Use letters only.")


def input_age() -> int:
    """
    Prompts and validates the user's age within the required boundaries.

    Returns:
        int: Validated age between 30 and 79 inclusive.
    """
    return input_int("Enter age", 30, 79)


def input_sex() -> Sex:
    """
    Prompts and maps user selection to the Sex enum.

    Returns:
        Sex: Selected Sex enum value.
    """
    options = ["Male", "Female"]
    choice = input_menu("Select sex at birth", options)
    if choice == 1:
        return Sex.MALE
    return Sex.FEMALE


def input_smoker() -> Smoker:
    """
    Prompts and maps user selection to the Smoker enum.

    Returns:
        Smoker: Selected Smoker enum value.
    """
    options = ["Current", "Former", "Never"]
    choice = input_menu("Select smoking status", options)
    if choice == 1:
        return Smoker.CURRENT
    elif choice == 2:
        return Smoker.FORMER
    return Smoker.NEVER


def input_vital() -> Vital:
    """
    Collects medical vitals from user inputs using input_handler tools.

    Returns:
        Vital: Structured dataclass containing clinical metrics.
    """
    print("\n--- Enter Clinical Measurements ---")
    sbp = input_int("Enter Systolic Blood Pressure (mmHg) ", 75, 220)
    total_chol = input_float("Enter Total Cholesterol (mmol/L) ", 0.0, 30.0)
    hdl_chol = input_float("Enter HDL Cholesterol (mmol/L) ", 0.0, 10.0)
    diabetes = input_bool("Does the individual have diabetes? ")
    bp_med = input_bool("Is the individual taking blood pressure lowering medication? ")
    lipid_med = input_bool("Is the individual taking lipid modifying medication? ")
    anti_med = input_bool("Is the individual taking antithrombotic medication? ")

    return Vital(
        systolic_blood_pressure=sbp,
        total_cholesterol=total_chol,
        hdl_cholesterol=hdl_chol,
        diabetes_status=diabetes,
        blood_pressure_lowering_med=bp_med,
        lipid_modifying_med=lipid_med,
        antithrombotic_med=anti_med,
    )


def add_user() -> User:
    """
    Gathers comprehensive demographic and vital data to construct a User instance.

    Returns:
        User: Fully populated User dataclass instance.
    """
    print("\n====================================")
    print("      REGISTER NEW INDIVIDUAL       ")
    print("====================================")
    name = input_name()
    age = input_age()
    sex = input_sex()
    smoker = input_smoker()
    vital = input_vital()

    return User(
        name=name, age=age, sex_at_birth=sex, smoking_status=smoker, vital=vital
    )


def run_assessment(user: User) -> tuple[float, Risk]:
    """
    Pass user records to calculator functions to evaluate risk.

    Args:
        user (User): The user profile to process.

    Returns:
        tuple[float, Risk]: Estimated risk percentage score and Risk category enum.
    """
    score = calculate_risk(user)
    risk_cat = classify_risk(score)
    return score, risk_cat


def display_result(user: User, score: float, risk: Risk) -> None:
    """
    Prints individual assessment results along with specific clinical advice.

    Args:
        user (User): The assessed individual.
        score (float): Calculated risk percentage.
        risk (Risk): Risk category enum.
    """
    print("\n====================================")
    print("      CVD RISK ASSESSMENT REPORT     ")
    print("====================================")
    print(f"Name:               {user.name}")
    print(f"Age / Sex:          {user.age} / {user.sex_at_birth.value}")
    print(f"Smoking Status:     {user.smoking_status.value}")
    print(f"Systolic BP:        {user.vital.systolic_blood_pressure} mmHg")
    print(f"Total Cholesterol:  {user.vital.total_cholesterol} mmol/L")
    print(f"HDL Cholesterol:    {user.vital.hdl_cholesterol} mmol/L")
    print("------------------------------------")
    print(f"Estimated 5-Year Risk: {score:.1f}%")
    print(f"Risk Classification:   {risk.value.upper()}")
    print("------------------------------------")
    print("Clinical Advice:")
    print(get_risk_advice(risk))
    print("====================================\n")


def display_history(users_list: list[User], scores_list: list[float]) -> None:
    """
    Loops over historical records to display a structural summary table.

    Args:
        users_list (list[User]): List of historical users.
        scores_list (list[float]): List of associated historical risk scores.
    """
    print("\n==================================================================")
    print(f"{'Name':<20} | {'Age':<5} | {'Sex':<8} | {'Risk Score':<10} | {'Category':<10}")
    print("==================================================================")

    if not users_list:
        print(f"{'No historical records found.':^66}")
    else:
        for i in range(len(users_list)):
            user = users_list[i]
            score = scores_list[i]
            risk_cat = classify_risk(score)
            
            print(
                f"{user.name:<20} | {user.age:<5} | {user.sex_at_birth.value:<8} | "
                f"{score:<9.1f}% | {risk_cat.value:<10}"
            )

    print("==================================================================\n")


def display_menu() -> int:
    """
    Displays choices.

    Returns:
        int: Selected operation index.
    """
    options = [
        "Add User & Run Risk Assessment",
        "View Current Assessment Result",
        "View Historical Summary Table",
        "Quit Program",
    ]
    return input_menu("Main Navigation Menu", options)


def main() -> None:
    """
    Main loop.
    """
    current_user: User = None
    current_score: float = None
    current_risk: Risk = None

    while True:
        choice = display_menu()

        if choice == 1:
            current_user = add_user()
            current_score, current_risk = run_assessment(current_user)
            users.append(current_user)
            scores.append(current_score)
            display_result(current_user, current_score, current_risk)

        elif choice == 2:
            if current_user is not None and current_score is not None and current_risk is not None:
                display_result(current_user, current_score, current_risk)
            else:
                print("\nNo assessment has been conducted in this session yet.\n")

        elif choice == 3:
            display_history(users, scores)

        elif choice == 4:
            print("\nExiting Cardiovascular Disease Risk Calculator. Session closed.\n")
            break


if __name__ == "__main__":
    main()
