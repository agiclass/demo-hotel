import json

from hotel_chatbot.utils import complete_openai


# 拼装用于NLU的prompt模版
def generate_prompt(user_input, hotel_list):
    prompt = f"""
    你是一个酒店查询的机器人，根据用户输入和查询到的酒店候选列表信息，为用户解释说明

    用户输入： {user_input}

    查询返回结果： {hotel_list}

    #注意不要用列表形式问答，使用纯文本段落#
    #尽量贴近酒店前台接线员的口吻且相对简短#
    """
    return prompt

def nlg(user_input, hotel_list):
    prompt = generate_prompt(user_input, hotel_list)
    return complete_openai(prompt)
