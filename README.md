# SearchActivity
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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


class SearchContext:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_search(self, text, pattern, step_by_step=False):
        if not self.strategy:
            raise ValueError("Nenhuma estratégia foi definida.")
        return self.strategy.search(text, pattern, step_by_step)


class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparação de Algoritmos de Busca em Strings")
        self.root.geometry("1100x750")

        self.files_content = []
        self.strategies = {
            "Naive": NaiveSearch(),
            "Rabin-Karp": RabinKarpSearch(),
            "KMP": KMPSearch(),
            "Boyer-Moore": BoyerMooreSearch(),
        }
        self.context = SearchContext()

        self.build_interface()

    def build_interface(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(top_frame, text="Carregar .txt", command=self.load_files).grid(row=0, column=0, padx=5, pady=5)

        tk.Label(top_frame, text="Pattern:").grid(row=0, column=1, padx=5, pady=5)
        self.pattern_entry = tk.Entry(top_frame, width=30)
        self.pattern_entry.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(top_frame, text="Algoritmo:").grid(row=0, column=3, padx=5, pady=5)
        self.algorithm_combo = ttk.Combobox(top_frame, values=list(self.strategies.keys()), state="readonly", width=20)
        self.algorithm_combo.grid(row=0, column=4, padx=5, pady=5)
        self.algorithm_combo.current(0)

        tk.Button(top_frame, text="Executar", command=self.run_search).grid(row=0, column=5, padx=5, pady=5)
        tk.Button(top_frame, text="Passo a passo", command=self.run_step_by_step).grid(row=0, column=6, padx=5, pady=5)
        tk.Button(top_frame, text="Comparar todos", command=self.compare_all).grid(row=0, column=7, padx=5, pady=5)

        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.files_list = tk.Listbox(middle_frame, width=40)
        self.files_list.pack(side="left", fill="y", padx=5)

        self.output_text = tk.Text(middle_frame, wrap="word")
        self.output_text.pack(side="left", fill="both", expand=True, padx=5)

        scroll = tk.Scrollbar(middle_frame, command=self.output_text.yview)
        scroll.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=scroll.set)

    def load_files(self):
        paths = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        if not paths:
            return

        self.files_content.clear()
        self.files_list.delete(0, tk.END)

        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.files_content.append((path, content))
                    self.files_list.insert(tk.END, path)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível ler o arquivo {path}\n{e}")

    def get_selected_strategy(self):
        algorithm_name = self.algorithm_combo.get()
        strategy = self.strategies[algorithm_name]
        self.context.set_strategy(strategy)
        return strategy

    def validate_inputs(self):
        if not self.files_content:
            messagebox.showwarning("Aviso", "Carregue pelo menos um arquivo .txt")
            return False

        pattern = self.pattern_entry.get()
        if not pattern:
            messagebox.showwarning("Aviso", "Digite a string de busca")
            return False

        return True

    def print_result(self, filename, strategy, result, show_logs=False):
        self.output_text.insert(tk.END, f"\nArquivo: {filename}\n")
        self.output_text.insert(tk.END, f"Algoritmo: {strategy.name()}\n")
        self.output_text.insert(tk.END, f"Complexidade teórica: {result.complexity}\n")
        self.output_text.insert(tk.END, f"Tamanho do texto: {result.text_length}\n")
        self.output_text.insert(tk.END, f"Tamanho do padrão: {result.pattern_length}\n")
        self.output_text.insert(tk.END, f"Ocorrências encontradas: {result.matches}\n")
        self.output_text.insert(tk.END, f"Número de comparações: {result.comparisons}\n")
        self.output_text.insert(tk.END, f"Tempo de execução: {result.elapsed_ns} ns\n")

        if show_logs:
            self.output_text.insert(tk.END, "Log passo a passo:\n")
            for log in result.logs:
                self.output_text.insert(tk.END, f"- {log}\n")

        self.output_text.insert(tk.END, "-" * 80 + "\n")

    def run_search(self):
        if not self.validate_inputs():
            return

        self.output_text.delete("1.0", tk.END)
        pattern = self.pattern_entry.get()
        strategy = self.get_selected_strategy()

        for filename, text in self.files_content:
            result = self.context.execute_search(text, pattern, step_by_step=False)
            self.print_result(filename, strategy, result, show_logs=False)

    def run_step_by_step(self):
        if not self.validate_inputs():
            return

        self.output_text.delete("1.0", tk.END)
        pattern = self.pattern_entry.get()
        strategy = self.get_selected_strategy()

        for filename, text in self.files_content:
            result = self.context.execute_search(text, pattern, step_by_step=True)
            self.print_result(filename, strategy, result, show_logs=True)

    def compare_all(self):
        if not self.validate_inputs():
            return

        self.output_text.delete("1.0", tk.END)
        pattern = self.pattern_entry.get()

        for filename, text in self.files_content:
            self.output_text.insert(tk.END, f"\nComparação no arquivo: {filename}\n")
            self.output_text.insert(tk.END, "=" * 80 + "\n")
            for strategy in self.strategies.values():
                self.context.set_strategy(strategy)
                result = self.context.execute_search(text, pattern, step_by_step=False)
                self.print_result(filename, strategy, result, show_logs=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
