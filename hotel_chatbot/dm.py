class DialogManager:
    def __init__(self):
        self.state = {}

    def update_state(self, new_state):
        conflict_keys = []
        for key, value in new_state.items():
            if key in self.state and self.state[key] != value:
                conflict_keys.append(key)
        for key in conflict_keys:
            del self.state[key]
        self.state.update(new_state)
        if (
            "price.range.low" in self.state
            and "price.range.high" in self.state
        ):
            if self.state["price.range.low"] > self.state["price.range.high"]:
                del self.state["price.range.low"]
                del self.state["price.range.high"]
                if "price.range.low" in new_state:
                    self.state["price.range.low"] = new_state[
                        "price.range.low"
                    ]
                if "price.range.high" in new_state:
                    self.state["price.range.high"] = new_state[
                        "price.range.high"
                    ]
        if (
            "rating.range.low" in self.state
            and "rating.range.high" in self.state
        ):
            if (
                self.state["rating.range.low"]
                > self.state["rating.range.high"]
            ):
                del self.state["rating.range.low"]
                del self.state["rating.range.high"]
                if "rating.range.low" in new_state:
                    self.state["rating.range.low"] = new_state[
                        "rating.range.low"
                    ]
                if "rating.range.high" in new_state:
                    self.state["rating.range.high"] = new_state[
                        "rating.range.high"
                    ]

    def get_state(self):
        return self.state
