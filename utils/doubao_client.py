import base64
import json

from openai import OpenAI

import config


def get_client() -> OpenAI:
    """获取豆包/火山方舟 API客户端"""
    return OpenAI(
        api_key=config.ARK_API_KEY,
        base_url=config.ARK_BASE_URL,
    )


def _encode_image(image_bytes: bytes) -> str:
    """将图片bytes编码为base64 data URL"""
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def analyze_food(image_bytes: bytes) -> dict:
    """调用豆包视觉模型识别食物，返回菜品和热量"""
    client = get_client()
    image_url = _encode_image(image_bytes)

    prompt = (
        "请分析这张图片中的食物，列出所有菜品名称和预估热量（单位：千卡），"
        "以JSON格式返回。格式："
        '{"dishes": [{"name": "菜品名", "calories": 数字}], "total_calories": 数字}'
        "只返回JSON，不要有其他文字。"
    )

    response = client.responses.create(
        model=config.DOUBAO_ENDPOINT_ID,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_image", "image_url": image_url},
                    {"type": "input_text", "text": prompt},
                ],
            }
        ],
    )

    raw_text = response.output_text.strip()

    # 尝试从响应中提取JSON
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        lines = [l for l in lines if not l.startswith("```")]
        raw_text = "\n".join(lines).strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {"raw_response": raw_text, "parse_error": True}
