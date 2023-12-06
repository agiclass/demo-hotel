import json
import gradio as gr
import pandas as pd

from hotel_chatbot.db import HotelDB
from hotel_chatbot.dm import DialogManager
from hotel_chatbot.nlu import nlu
from hotel_chatbot.nlg import nlg


def run_gradio_chatbot():
    db = HotelDB()
    dm = DialogManager()

    def chatbot_for_hotel(user_input):
        state = nlu(user_input)
        dm.update_state(state)
        output_fields = ["name", "rating", "price"]
        candidates = db.search(
            dm.get_state(), output_fields=output_fields
        )
        candidates = candidates[:3]
        data = {}
        for d in candidates:
            d.pop("hotel_id")  # hotel_id用于rrf排序，不做显示了
            for key, value in d.items():
                if key not in data:
                    data[key] = []
                data[key].append(value)
        if data == {}:
            data = {"hotel": []}
        df = pd.DataFrame(data)
        reply = nlg(user_input, json.dumps(candidates, ensure_ascii=False))
        return reply.strip(), df

    interface = gr.Interface(
        fn=chatbot_for_hotel,
        inputs=gr.Textbox(label="需求", placeholder="请输入您对酒店的需求"),
        outputs=[
            gr.Textbox(label="回复"),
            gr.Dataframe(label="酒店列表")
        ],
        examples=["推荐一下奢华的酒店", "机场附近的平价酒店", "我想带宠物住店"],
        title="酒店智能推荐助手 demo",
    )

    interface.launch(server_port=7800,root_path="/cs/")


if __name__ == "__main__":  # pragma: no cover
    run_gradio_chatbot()
