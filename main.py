import tkinter as tk
from ui.search_app import SearchApp


def main():
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()