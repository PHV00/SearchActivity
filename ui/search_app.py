import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from strategies.naive_search import NaiveSearch
from strategies.rabin_karp_search import RabinKarpSearch
from strategies.kmp_search import KMPSearch
from strategies.boyer_moore_search import BoyerMooreSearch
from context.search_context import SearchContext


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
        self.algorithm_combo = ttk.Combobox(
            top_frame,
            values=list(self.strategies.keys()),
            state="readonly",
            width=20
        )
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