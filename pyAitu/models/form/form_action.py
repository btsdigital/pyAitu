class FormAction:
    def __init__(
            self,
            action: str,
            data_template: str = None,
            hidden_metadata: str = None
    ):
        self.action = action
        self.data_template = data_template
        self.hidden_metadata = hidden_metadata
