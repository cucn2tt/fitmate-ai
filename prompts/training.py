def build_training_prompt(profile: dict) -> str:
    """生成训练计划prompt"""
    workout_time = profile["workout_time"]
    return f"""你是专业健身教练。根据以下信息生成今日训练计划：

【用户信息】
- 性别：{profile["gender"]}
- 训练水平：{profile["level"]}
- 目标：{profile["goal"]}
- 可用时间：{workout_time}分钟
- 场地：{profile["location"]}

【输出要求】
严格按照以下Markdown格式输出：

## 今日训练计划

### 热身（5分钟）
- 动作1：xxx
- 动作2：xxx

### 正式训练（{workout_time - 10}分钟）
- 动作1：名称 × 组数 × 次数
- 动作2：名称 × 组数 × 次数
- 动作3：名称 × 组数 × 次数
- 动作4：名称 × 组数 × 次数

### 拉伸（5分钟）
- 动作1：xxx
- 动作2：xxx

### 注意事项
- 一句话提醒"""
