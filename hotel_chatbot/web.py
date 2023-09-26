import gradio as gr
import pandas as pd
from db import HotelDB
from dm import DialogManager
from nlu import nlu


def run_gradio_chatbot():
    db = HotelDB()
    dm = DialogManager()

    def chatbot_for_hotel(input_text):
        state = nlu(input_text)
        dm.update_state(state)
        candidates = db.search(
            dm.get_state(), output_fields=["address", "rating", "price"]
        )
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
        return df

    interface = gr.Interface(
        fn=chatbot_for_hotel, inputs="text", outputs="dataframe"
    )

    interface.launch()


if __name__ == "__main__":  # pragma: no cover
    run_gradio_chatbot()
