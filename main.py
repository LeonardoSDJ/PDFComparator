from src.gui import PDFComparisonGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = PDFComparisonGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()