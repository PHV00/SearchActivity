from abc import ABC, abstractmethod

class SearchResult:
    def __init__(self, matches, comparisons, elapsed_ns, logs, text_length, pattern_length, complexity):
        self.matches = matches
        self.comparisons = comparisons
        self.elapsed_ns = elapsed_ns
        self.logs = logs
        self.text_length = text_length
        self.pattern_length = pattern_length
        self.complexity = complexity

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, text, pattern, step_by_step=False):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def complexity(self):
        pass