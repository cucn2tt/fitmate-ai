def build_analysis_prompt(weight_list: list, waist_list: list) -> str:
    """生成体脂趋势分析prompt"""
    return f"""你是健身数据分析师。用户最近7天的数据如下：

体重(kg)：{weight_list}
腰围(cm)：{waist_list}

请分析：
1. 体脂变化趋势（下降/平台/上升）
2. 变化速度是否合理（每周减重0.5-1kg为健康）
3. 一句鼓励或提醒

输出格式：3行短文本，每行一个要点，简洁有力。"""
