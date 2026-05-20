def build_current_meal_prompt(
    dishes: list, total_calories: float, remaining_calories: float
) -> str:
    """生成当餐补救建议prompt"""
    dishes_text = "\n".join(
        f"- {d['name']}：{d['calories']} kcal" for d in dishes
    )
    return f"""用户今日吃了以下食物：
{dishes_text}
合计热量：{total_calories} kcal

用户今日剩余热量预算：{remaining_calories} kcal

请输出（严格3行）：
1. 热量评估：xxx
2. 预算对比：超出/剩余 xxx kcal
3. 补救建议：一句话建议（如：晚餐减半主食、增加运动等）"""
