# FitMate AI

智能健身规划与饮食管理助手，基于 DeepSeek + 豆包视觉模型。

## 功能

- **每日记录** — 记录体重、腰围，CSV 本地存储
- **训练计划** — DeepSeek 根据个人画像生成个性化训练方案
- **饮食计划** — 基于 Mifflin-St Jeor 公式计算热量目标，AI 生成三餐
- **拍照识食** — 上传食物照片，豆包视觉模型识别菜品并估算热量，AI 给出补救建议
- **体脂分析** — DeepSeek 分析近 7 天体重/腰围趋势
- **历史数据** — Plotly 可视化体重、腰围变化曲线

## 技术栈

| 组件 | 选型 |
|------|------|
| 框架 | Streamlit |
| LLM | DeepSeek Chat |
| 视觉模型 | 豆包（火山方舟） |
| 数据 | CSV + Pandas |
| 可视化 | Plotly |

## 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/cucn2tt/fitmate-ai.git
cd fitmate-ai

# 2. 安装依赖
pip install -r requirements.txt

# 3. 设置环境变量
# Windows (PowerShell)
$env:DEEPSEEK_API_KEY = "你的DeepSeek API Key"
$env:ARK_API_KEY = "你的火山方舟 API Key"

# macOS / Linux
export DEEPSEEK_API_KEY="你的DeepSeek API Key"
export ARK_API_KEY="你的火山方舟 API Key"

# 4. 启动
streamlit run app.py
```

## Streamlit Community Cloud 部署

1. 前往 [share.streamlit.io](https://share.streamlit.io)，用 GitHub 登录
2. 点击 **New app** → 选择仓库 `cucn2tt/fitmate-ai`，分支 `main`，主文件 `app.py`
3. 在 App Settings → Secrets 中添加：

```toml
DEEPSEEK_API_KEY = "你的DeepSeek API Key"
ARK_API_KEY = "你的火山方舟 API Key"
DOUBAO_ENDPOINT_ID = "你的豆包端点ID"
```

4. 点击 Deploy，等待 1-2 分钟即可

## 项目结构

```
fitmate-ai/
├── app.py                 # Streamlit 主程序
├── config.py              # 配置（API Key 从环境变量读取）
├── requirements.txt
├── prompts/
│   ├── training.py        # 训练计划 prompt
│   ├── diet.py            # 饮食计划 prompt
│   ├── body_analysis.py   # 体脂分析 prompt
│   └── current_meal.py    # 当餐补救 prompt
└── utils/
    ├── calories.py        # 热量计算 (BMR/TDEE)
    ├── file_ops.py        # CSV 读写
    ├── deepseek_client.py # DeepSeek API 封装
    └── doubao_client.py   # 豆包视觉模型封装
```

## License

MIT
