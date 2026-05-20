def calculate_bmr(gender: str, weight: float, height: float, age: int) -> float:
    """Mifflin-St Jeor 基础代谢率公式"""
    if gender == "男":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161


def calculate_tdee(bmr: float, activity_factor: float = 1.375) -> float:
    """每日总消耗（默认轻活动系数1.375）"""
    return bmr * activity_factor


def calculate_target_calories(tdee: float, goal: str) -> float:
    """根据目标计算每日热量摄入目标"""
    if goal == "减脂":
        return tdee - 300
    elif goal == "增肌":
        return tdee + 300
    else:
        return tdee


def get_calorie_info(profile: dict) -> dict:
    """根据用户画像计算完整热量信息"""
    bmr = calculate_bmr(
        profile["gender"],
        profile["weight"],
        profile["height"],
        profile["age"],
    )
    tdee = calculate_tdee(bmr)
    target = calculate_target_calories(tdee, profile["goal"])
    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "target_calories": round(target, 1),
        "goal": profile["goal"],
    }
