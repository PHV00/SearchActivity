import time
from strategies.search_strategy import SearchStrategy, SearchResult


class RabinKarpSearch(SearchStrategy):
    def name(self):
        return "Rabin-Karp"

    def complexity(self):
        return "O(n + m) médio"

    def search(self, text, pattern, step_by_step=False):
        n = len(text)
        m = len(pattern)
        d = 256
        q = 101
        matches = []
        comparisons = 0
        logs = []

        start = time.perf_counter_ns()

        if m == 0 or m > n:
            end = time.perf_counter_ns()
            return SearchResult([], 0, end - start, ["Padrão vazio ou maior que o texto."], n, m, self.complexity())

        h = 1
        for _ in range(m - 1):
            h = (h * d) % q

        p = 0
        t = 0

        for i in range(m):
            p = (d * p + ord(pattern[i])) % q
            t = (d * t + ord(text[i])) % q

        if step_by_step:
            logs.append(f"Hash inicial do padrão: {p}")
            logs.append(f"Hash inicial da janela do texto: {t}")

        for i in range(n - m + 1):
            if step_by_step:
                logs.append(f"Janela iniciando em {i}: hash_texto={t}, hash_padrão={p}")

            if p == t:
                if step_by_step:
                    logs.append("Hashes iguais. Verificando caracteres...")

                match = True
                for j in range(m):
                    comparisons += 1

                    if step_by_step:
                        logs.append(
                            f"Comparando text[{i + j}]='{text[i + j]}' com pattern[{j}]='{pattern[j]}'"
                        )

                    if text[i + j] != pattern[j]:
                        match = False
                        if step_by_step:
                            logs.append("Colisão de hash detectada.")
                        break

                if match:
                    matches.append(i)
                    if step_by_step:
                        logs.append(f"Ocorrência encontrada na posição {i}")

            if i < n - m:
                t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
                if t < 0:
                    t += q

                if step_by_step:
                    logs.append(f"Recalculando hash para a próxima janela: {t}")

        end = time.perf_counter_ns()
        return SearchResult(matches, comparisons, end - start, logs, n, m, self.complexity())