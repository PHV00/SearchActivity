import time
from strategy.search_strategy import SearchStrategy, SearchResult


class BoyerMooreSearch(SearchStrategy):
    def name(self):
        return "Boyer-Moore"

    def complexity(self):
        return "O(n / m) melhor caso"

    def build_bad_char_table(self, pattern):
        table = {}
        for i, char in enumerate(pattern):
            table[char] = i
        return table

    def search(self, text, pattern, step_by_step=False):
        n = len(text)
        m = len(pattern)
        matches = []
        comparisons = 0
        logs = []

        start = time.perf_counter_ns()

        if m == 0 or m > n:
            end = time.perf_counter_ns()
            return SearchResult([], 0, end - start, ["Padrão vazio ou maior que o texto."], n, m, self.complexity())

        bad_char = self.build_bad_char_table(pattern)

        if step_by_step:
            logs.append(f"Tabela de saltos (bad character): {bad_char}")

        s = 0

        while s <= n - m:
            j = m - 1

            if step_by_step:
                logs.append(f"Alinhando padrão na posição {s}")

            while j >= 0:
                comparisons += 1

                if step_by_step:
                    logs.append(
                        f"Comparando text[{s + j}]='{text[s + j]}' com pattern[{j}]='{pattern[j]}'"
                    )

                if pattern[j] != text[s + j]:
                    break

                j -= 1

            if j < 0:
                matches.append(s)

                if step_by_step:
                    logs.append(f"Ocorrência encontrada na posição {s}")

                s += (m - bad_char.get(text[s + m], -1)) if s + m < n else 1

                if step_by_step:
                    logs.append(f"Deslocando padrão para {s}")
            else:
                shift = max(1, j - bad_char.get(text[s + j], -1))

                if step_by_step:
                    logs.append(
                        f"Mismatch com '{text[s + j]}'. Última ocorrência no padrão: {bad_char.get(text[s + j], -1)}. Deslocamento = {shift}"
                    )

                s += shift

        end = time.perf_counter_ns()
        return SearchResult(matches, comparisons, end - start, logs, n, m, self.complexity())