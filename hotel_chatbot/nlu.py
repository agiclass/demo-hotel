import json

from hotel_chatbot.utils import complete_openai, deserialize


# 拼装用于NLU的prompt模版
def generate_prompt(input_text):
    instruction = """
      你的任务是识别用户对酒店的选择条件
      酒店包含8个属性，分别是：名称(name)、电话(phone)、地址(address)、地铁(subway)、
      酒店类型(type)、价格(price)、评分(rating)、酒店设施(facilities)。
      其中酒店类型的取值只有以下四种：豪华型, 经济型, 舒适型, 高档型
    """
    output_format = """
      以JSON格式输出，包含字段如下
        - name: string类型
        - type: string类型，取值范围：'豪华型', '经济型', '舒适型', '高档型'
        - address: string类型
        - subway: string类型
        - phone: string类型
        - facilities: list类型，其中元素string类型
        - price.range.low: float类型，取值范围大于0
        - price.range.high: float类型，取值范围大于0
        - rating.range.low: float类型，取值范围[0,5]
        - rating.range.high: float类型，取值范围[0,5]
        - sort.ordering: string类型，排序的顺序，取值范围：'ascend', 'descend'
        - sort.slot: string类型，用于排序的属性字段，取值范围：'price', 'rating'
      #不要编造此外的字段# #如用户输入与订酒店无关则输出空JSON: {}#
      #output JSON only# #no acknowledgement# #no comment#
    """
    examples = """
      最近情况不错啊，加油：{}
      想找一家评分4.5分以上的：{"rating.range.low":4.5}
      我想订一个400元以内的酒店：{"price.range.high":400}
      订一家200到400元的酒店吧：{"price.range.low":200,"price.range.high":400}
      有经济型酒店嘛，便宜点的：{"type":"经济型","sort.slot":"price","sort.ordering","ascend"}
    """
    prompt = f"""
      {instruction}

      {output_format}

      examples:
      {examples}

      user input：
      {input_text}
    """
    return prompt


def nlu(input_text):
    prompt = generate_prompt(input_text)
    reply = complete_openai(prompt)
    reply = deserialize(reply)
    print(f"\033[32mNLU DEBUG:\n{json.dumps(reply,ensure_ascii=False,indent=2)}\033[0m")
    return reply
