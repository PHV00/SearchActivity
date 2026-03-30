import time
from strategies.search_strategy import SearchStrategy, SearchResult


class NaiveSearch(SearchStrategy):
    def name(self):
        return "Naive"

    def complexity(self):
        return "O(n * m)"

    def search(self, text, pattern, step_by_step=False):
        n = len(text)
        m = len(pattern)
        matches = []
        comparisons = 0
        logs = []

        start = time.perf_counter_ns()

        if m == 0:
            end = time.perf_counter_ns()
            return SearchResult([], 0, end - start, ["Padrão vazio."], n, m, self.complexity())

        for i in range(n - m + 1):
            if step_by_step:
                logs.append(f"Alinhando padrão na posição {i}")

            found = True
            for j in range(m):
                comparisons += 1

                if step_by_step:
                    logs.append(
                        f"Comparando text[{i + j}]='{text[i + j]}' com pattern[{j}]='{pattern[j]}'"
                    )

                if text[i + j] != pattern[j]:
                    found = False
                    if step_by_step:
                        logs.append(f"Falha na comparação. Deslocando padrão para {i + 1}")
                    break

            if found:
                matches.append(i)
                if step_by_step:
                    logs.append(f"Ocorrência encontrada na posição {i}")

        end = time.perf_counter_ns()
        return SearchResult(matches, comparisons, end - start, logs, n, m, self.complexity())