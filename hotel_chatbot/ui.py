import gradio as gr
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from nlu import nlu
from db import Database
from dm import DialogManager

db = Database()
dm = DialogManager()

def chatbot_for_hotel(input_text):
    state = nlu(input_text)
    dm.update_state(state)
    candidates = db.search(dm.get_state())
    data = {}
    for d in candidates:
        for key, value in d.items():
            if key not in data:
                data[key] = []
            data[key].append(value)
    if data == {}:
        data = {"hotel":[]}
    df = pd.DataFrame(data)
    return df

interface = gr.Interface(fn=chatbot_for_hotel, inputs="text", outputs="dataframe")

interface.launch()
