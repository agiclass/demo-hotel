import json
import os

import openai
import requests

# from dotenv import find_dotenv, load_dotenv

# load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")


# 去除LLM返回JSON中为空的字段
def remove_empty(d):
    if type(d) is dict:
        return dict(
            (k, remove_empty(v)) for k, v in d.items() if v and remove_empty(v)
        )
    elif type(d) is list:
        return [remove_empty(v) for v in d if v and remove_empty(v)]
    else:
        return d


# 将LLM返回文本解析为JSON
def deserialize(text):
    try:
        return remove_empty(json.loads(text))
    except Exception:
        print(text)
        return {}


# 对比查询条件是否一致
def compare_dict(dict1, dict2):
    if len(dict1) != len(dict2):
        return False
    for key in dict1:
        if key not in dict2:
            return False
        if isinstance(dict1[key], (int, float)) and isinstance(
            dict2[key], (int, float)
        ):
            if abs(dict1[key] - dict2[key]) > 1e-9:
                return False
        elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
            list1 = sorted([s.replace("服务", "") for s in dict1[key]])
            list2 = sorted([s.replace("服务", "") for s in dict2[key]])
            if list1 != list2:
                return False
        elif dict1[key] != dict2[key]:
            return False
    return True


# minimax LLM 接口
def complete_minimax(prompt, model="abab5.5-chat"):
    group_id = os.getenv("MINIMAX_GROUP_ID")
    api_key = os.getenv("MINIMAX_API_KEY")
    url = (
        "https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId="
        + group_id
    )
    payload = {
        "bot_setting": [
            {
                "bot_name": "智能助理",
                "content": "你是根据用户需求来输出JSON格式文本的机器人",
            }
        ],
        "messages": [
            {"sender_type": "USER", "sender_name": "小明", "text": prompt}
        ],
        "reply_constraints": {"sender_type": "BOT", "sender_name": "智能助理"},
        "model": model,
        "tokens_to_generate": 1000,
        "temperature": 0.01,
        "top_p": 0.95,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    response = json.loads(response.text)
    reply = response["reply"]
    return reply


def complete_openai(prompt, model="gpt-3.5-turbo-instruct"):
    if model == "gpt-3.5-turbo-instruct":
        response = openai.Completion.create(
            model=model, prompt=prompt, max_tokens=500, temperature=0
        )
        return response.choices[0].text
    else:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]


def embedding_openai(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(model=model, input=text)
    return response["data"][0]["embedding"]
