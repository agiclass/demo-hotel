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
        fn=chatbot_for_hotel, inputs="text", outputs=["text","dataframe"]
    )

    interface.launch(server_port=7800)


if __name__ == "__main__":  # pragma: no cover
    run_gradio_chatbot()
