import os

# ========== DeepSeek API ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# ========== 豆包/火山方舟 ==========
ARK_API_KEY = os.getenv("ARK_API_KEY")
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DOUBAO_ENDPOINT_ID = os.getenv("DOUBAO_ENDPOINT_ID", "ep-20260520040238-bvzw")

# ========== 用户画像 ==========
USER_PROFILE = {
    "gender": "男",
    "age": 28,
    "height": 175,
    "weight": 70,
    "goal": "减脂",
    "target_weight": 65,
    "level": "中级",
    "workout_time": 30,
    "location": "居家",
    "restrictions": "",
}
