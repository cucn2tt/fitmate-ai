def build_diet_prompt(profile: dict, target_calories: float) -> str:
    """生成饮食计划prompt"""
    restrictions = profile.get("restrictions", "") or "无"
    water = round(profile["weight"] * 30)
    return f"""你是专业营养师。根据以下信息生成今日饮食计划：

【用户信息】
- 目标：{profile["goal"]}
- 热量目标：{target_calories} kcal
- 饮食限制：{restrictions}

【输出要求】
严格按照以下格式输出：

## 今日饮食计划（总热量：{target_calories} kcal）

### 早餐（约25%热量）
- 食物1：xxx
- 食物2：xxx
- 食物3：xxx

### 午餐（约35%热量）
- 食物1：xxx
- 食物2：xxx
- 食物3：xxx

### 晚餐（约30%热量）
- 食物1：xxx
- 食物2：xxx
- 食物3：xxx

### 加餐（可选，约10%热量）
- 建议：xxx

### 饮水提醒
- 建议饮水量：{water} ml"""
