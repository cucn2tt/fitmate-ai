from openai import OpenAI

import config


def get_client() -> OpenAI:
    """获取DeepSeek API客户端"""
    return OpenAI(
        api_key=config.DEEPSEEK_API_KEY,
        base_url=config.DEEPSEEK_BASE_URL,
    )


def chat(prompt: str, system_prompt: str | None = None) -> str:
    """调用DeepSeek Chat，返回文本响应"""
    client = get_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=config.DEEPSEEK_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content.strip()
