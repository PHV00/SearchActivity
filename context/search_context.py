class SearchContext:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_search(self, text, pattern, step_by_step=False):
        if not self.strategy:
            raise ValueError("Nenhuma estratégia foi definida.")
        return self.strategy.search(text, pattern, step_by_step)
