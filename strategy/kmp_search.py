import time
from strategies.search_strategy import SearchStrategy, SearchResult


class KMPSearch(SearchStrategy):
    def name(self):
        return "KMP"

    def complexity(self):
        return "O(n + m)"

    def compute_lps(self, pattern, logs=None, step_by_step=False):
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1

        if step_by_step and logs is not None:
            logs.append(f"Construindo LPS para o padrão '{pattern}'")

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length

                if step_by_step and logs is not None:
                    logs.append(f"LPS[{i}] = {length}")

                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]

                    if step_by_step and logs is not None:
                        logs.append(f"Falha no LPS, recuando length para {length}")
                else:
                    lps[i] = 0

                    if step_by_step and logs is not None:
                        logs.append(f"LPS[{i}] = 0")

                    i += 1

        return lps

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

        lps = self.compute_lps(pattern, logs, step_by_step)

        if step_by_step:
            logs.append(f"Tabela LPS final: {lps}")

        i = 0
        j = 0

        while i < n:
            comparisons += 1

            if step_by_step:
                logs.append(f"Comparando text[{i}]='{text[i]}' com pattern[{j}]='{pattern[j]}'")

            if text[i] == pattern[j]:
                i += 1
                j += 1

            if j == m:
                matches.append(i - j)

                if step_by_step:
                    logs.append(f"Ocorrência encontrada na posição {i - j}")

                j = lps[j - 1]

                if step_by_step:
                    logs.append(f"Após match, j volta para {j} usando LPS")

            elif i < n and text[i] != pattern[j]:
                if j != 0:
                    if step_by_step:
                        logs.append(f"Falha. j vai de {j} para {lps[j - 1]} usando LPS")

                    j = lps[j - 1]
                else:
                    if step_by_step:
                        logs.append(f"Falha com j=0. Avançando i para {i + 1}")

                    i += 1

        end = time.perf_counter_ns()
        return SearchResult(matches, comparisons, end - start, logs, n, m, self.complexity())