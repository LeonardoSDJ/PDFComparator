import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import threading
import logging
import os
import textwrap
from .pdf_tool import PDFComparisonTool
from .utils import resize_image

class PDFComparisonGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Ferramenta de Comparação de PDFs")
        self.master.geometry("1280x720")
        self.master.minsize(800, 600) 
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', padding=6, relief='flat', background='#4CAF50', wraplength=150)
        self.style.configure('TLabel', padding=6, background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')

        self.pdf_tool = PDFComparisonTool()
        self.current_page = 0
        self.pdf1_path = ""
        self.pdf2_path = ""

        self.create_widgets()
    
    def create_widgets(self):
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        self.file_frame = ttk.Frame(self.master)
        self.file_frame.grid(row=0, column=0, pady=10, sticky='ew')
        self.file_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.pdf1_button = ttk.Button(self.file_frame, text="Selecionar PDF 1", command=self.select_pdf1)
        self.pdf1_button.grid(row=0, column=0, padx=5, sticky='ew')
        
        self.pdf2_button = ttk.Button(self.file_frame, text="Selecionar PDF 2", command=self.select_pdf2)
        self.pdf2_button.grid(row=0, column=1, padx=5, sticky='ew')
        
        ttk.Button(self.file_frame, text="Comparar PDFs", command=self.start_comparison).grid(row=0, column=2, padx=5, sticky='ew')

        self.image_frame = ttk.Frame(self.master)
        self.image_frame.grid(row=1, column=0, pady=10, sticky='nsew')
        self.image_frame.grid_columnconfigure((0, 1), weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)

        self.image_label1 = ttk.Label(self.image_frame)
        self.image_label1.grid(row=0, column=0, sticky='nsew')

        self.image_label2 = ttk.Label(self.image_frame)
        self.image_label2.grid(row=0, column=1, sticky='nsew')

        self.nav_frame = ttk.Frame(self.master)
        self.nav_frame.grid(row=2, column=0, pady=10, sticky='ew')
        self.nav_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Button(self.nav_frame, text="Anterior", command=self.prev_page).grid(row=0, column=0, padx=5, sticky='e')
        self.page_label = ttk.Label(self.nav_frame, text="Página: 0 / 0")
        self.page_label.grid(row=0, column=1, padx=5)
        ttk.Button(self.nav_frame, text="Próxima", command=self.next_page).grid(row=0, column=2, padx=5, sticky='w')

        self.adjust_frame = ttk.Frame(self.master)
        self.adjust_frame.grid(row=3, column=0, pady=10, sticky='ew')

        self.contrast_slider = ttk.Scale(self.adjust_frame, from_=0, to=2, length=200, command=self.update_image)
        self.contrast_slider.set(1)
        self.contrast_slider.pack(side=tk.LEFT, padx=10)
        ttk.Label(self.adjust_frame, text="Contraste").pack(side=tk.LEFT)

        self.brightness_slider = ttk.Scale(self.adjust_frame, from_=-50, to=50, length=200, command=self.update_image)
        self.brightness_slider.set(0)
        self.brightness_slider.pack(side=tk.LEFT, padx=10)
        ttk.Label(self.adjust_frame, text="Brilho").pack(side=tk.LEFT)

        self.color_intensity = ttk.Scale(self.adjust_frame, from_=0, to=1, length=200, command=self.update_comparison)
        self.color_intensity.set(0.3)
        self.color_intensity.pack(side=tk.LEFT, padx=10)
        ttk.Label(self.adjust_frame, text="Intensidade da Cor").pack(side=tk.LEFT)

        self.threshold = ttk.Scale(self.adjust_frame, from_=0, to=255, length=200, command=self.update_comparison)
        self.threshold.set(30)
        self.threshold.pack(side=tk.LEFT, padx=10)
        ttk.Label(self.adjust_frame, text="Limiar de Diferença").pack(side=tk.LEFT)

        ttk.Button(self.master, text="Salvar Diferenças", command=self.save_differences).grid(row=4, column=0, pady=10)
        ttk.Button(self.master, text="Gerar Relatório", command=self.generate_report_callback).grid(row=5, column=0, pady=10)

        self.progress_bar = ttk.Progressbar(self.master, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.grid(row=6, column=0, pady=10)

        self.feedback_label = ttk.Label(self.master, text="", foreground="red")
        self.feedback_label.grid(row=7, column=0, pady=10)

        self.master.bind('<Configure>', self.on_window_resize)

    def format_button_text(self, prefix, filename):
        wrapped_filename = textwrap.fill(filename, width=20)
        return f"{prefix}:\n{wrapped_filename}"

    def on_window_resize(self, event):
        self.update_image()


    def select_pdf1(self):
        self.pdf1_path = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if self.pdf1_path:
            filename = os.path.basename(self.pdf1_path)
            button_text = self.format_button_text("PDF 1", filename)
            self.pdf1_button.config(text=button_text)

    def select_pdf2(self):
        self.pdf2_path = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if self.pdf2_path:
            filename = os.path.basename(self.pdf2_path)
            button_text = self.format_button_text("PDF 2", filename)
            self.pdf2_button.config(text=button_text)

    def start_comparison(self):
        if self.pdf1_path and self.pdf2_path:
            self.feedback_label.config(text="Comparando PDFs, aguarde...")
            self.progress_bar['value'] = 0
            self.master.update_idletasks()
            comparison_thread = threading.Thread(target=self.compare_pdfs)
            comparison_thread.start()
        else:
            messagebox.showerror("Erro", "Por favor, selecione ambos os PDFs primeiro.")

    def compare_pdfs(self):
        try:
            self.pdf_tool.process_pdfs(self.pdf1_path, self.pdf2_path, self.update_progress)
            self.current_page = 0
            self.update_image()
            self.feedback_label.config(text="Comparação Completa!")
            self.progress_bar['value'] = 100
        except Exception as e:
            self.feedback_label.config(text=f"Erro: {str(e)}")
            logging.error(f"Erro durante a comparação de PDFs: {str(e)}", exc_info=True)

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.master.update_idletasks()

    def update_comparison(self, _=None):
        if hasattr(self, 'pdf1_path') and hasattr(self, 'pdf2_path'):
            self.pdf_tool.update_comparison_params(
                threshold=int(self.threshold.get()),
                color_intensity=self.color_intensity.get()
            )
            self.update_image()

    def update_image(self, _=None):
        if self.pdf_tool.diff_images:
            try:
                img1 = self.pdf_tool.pdf1_images[self.current_page]
                img2 = self.pdf_tool.get_diff_image(self.current_page)['image']

                if img1 is not None and img2 is not None:
                    img1 = Image.fromarray(img1.astype('uint8'))
                    img2 = Image.fromarray(img2.astype('uint8'))

                    img1 = img1.filter(ImageFilter.SHARPEN)
                    img2 = img2.filter(ImageFilter.SHARPEN)

                    enhancer = ImageEnhance.Contrast(img1)
                    img1 = enhancer.enhance(self.contrast_slider.get())
                    enhancer = ImageEnhance.Contrast(img2)
                    img2 = enhancer.enhance(self.contrast_slider.get())

                    enhancer = ImageEnhance.Brightness(img1)
                    img1 = enhancer.enhance(1 + self.brightness_slider.get() / 100)
                    enhancer = ImageEnhance.Brightness(img2)
                    img2 = enhancer.enhance(1 + self.brightness_slider.get() / 100)

                    max_width = self.image_frame.winfo_width() // 2
                    max_height = self.image_frame.winfo_height()

                    img1 = resize_image(img1, max_width, max_height)
                    img2 = resize_image(img2, max_width, max_height)

                    img1 = ImageTk.PhotoImage(img1)
                    img2 = ImageTk.PhotoImage(img2)

                    self.image_label1.config(image=img1)
                    self.image_label1.image = img1
                    self.image_label2.config(image=img2)
                    self.image_label2.image = img2

                    self.page_label.config(text=f"Página: {self.current_page + 1} / {len(self.pdf_tool.diff_images)}")
            except Exception as e:
                self.feedback_label.config(text=f"Erro ao atualizar imagem: {str(e)}")
                logging.error(f"Erro ao atualizar imagem: {str(e)}", exc_info=True)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_image()

    def next_page(self):
        if self.current_page < len(self.pdf_tool.diff_images) - 1:
            self.current_page += 1
            self.update_image()

    def save_differences(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            try:
                self.pdf_tool.save_diff_images(output_dir)
                messagebox.showinfo("Sucesso", f"Imagens de diferença salvas em {output_dir}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar imagens: {str(e)}")
                logging.error(f"Erro ao salvar imagens de diferença: {str(e)}", exc_info=True)
    
    def generate_report_callback(self):
        if hasattr(self, 'pdf1_path') and hasattr(self, 'pdf2_path'):
            try:
                report = self.pdf_tool.generate_comparison_report(self.pdf1_path, self.pdf2_path)
                
                save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                if save_path:
                    with open(save_path, 'w', encoding='utf-8') as report_file:
                        report_file.write(report)
                    messagebox.showinfo("Relatório Gerado", f"Relatório salvo com sucesso em {save_path}")
                else:
                    messagebox.showwarning("Cancelado", "Operação de salvamento cancelada.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar o relatório: {str(e)}")
                logging.error(f"Erro ao gerar o relatório: {str(e)}", exc_info=True)
        else:
            messagebox.showerror("Erro", "Por favor, selecione ambos os PDFs antes de gerar o relatório.")