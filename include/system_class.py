from include.window_class import App

class MainSystem(App):
    amount_paid = 0

    def __init__(self):
        super().__init__(self)
        self.add_amount_button_event = self.run_button_event
        self.paper_sizes = ["A4", "Long"]

    def run_button_event(self):
        self.amount_paid += 10
        self.amount_given_var.set(self.amount_paid) 
