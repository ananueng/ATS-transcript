import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd
from tkinter import ttk
from app.reader import PDF_Parser
from datetime import datetime

class ATSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATS Tool")
        
        self.transcript_paths = []
        self.default_input_path = os.path.join(os.getcwd(), "data", "input", "transcript")
        self.default_output_path = os.path.join(os.getcwd(), "data", "output")
        self.default_config_file = os.path.join(os.getcwd(), "data", "input", "config.csv")
        
        self.input_dir = tk.StringVar(value=self.default_input_path)
        self.output_dir = tk.StringVar(value=self.default_output_path)
        self.config_file = tk.StringVar(value=self.default_config_file)
        self.output_file = None
        self.output_folder = None

        ttk.Label(root, text="Input Directory:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(root, textvariable=self.input_dir, width=50).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(root, text="Browse", command=self.select_directory).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=10)
        ttk.Entry(root, textvariable=self.output_dir, width=50).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(root, text="Browse", command=self.select_output_directory).grid(row=1, column=2, padx=10, pady=10)

        ttk.Label(root, text="Config File:").grid(row=2, column=0, padx=10, pady=10)
        ttk.Entry(root, textvariable=self.config_file, width=50).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(root, text="Browse", command=self.select_config_file).grid(row=2, column=2, padx=10, pady=10)

        ttk.Button(root, text="Process PDFs", command=self.process_files).grid(row=3, columnspan=3, pady=10)

        self.num_processed_pdfs = 0
        self.progress_label = ttk.Label(root, text="")
        self.progress_label.grid(row=4, columnspan=3, pady=10)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=5, columnspan=3, pady=10)

    def select_directory(self):
        dir_path = filedialog.askdirectory(initialdir=self.input_dir.get())
        if dir_path:
            self.input_dir.set(dir_path)

    def select_output_directory(self):
        dir_path = filedialog.askdirectory(initialdir=self.output_dir.get())
        if dir_path:
            self.output_dir.set(dir_path)

    def select_config_file(self):
        file_path = filedialog.askopenfilename(initialdir=self.config_file.get(), filetypes=[("TSV files", "*.tsv"), ("All files", "*.*")])
        if file_path:
            self.config_file.set(file_path)

    def process_files(self):
        input_path = self.input_dir.get()
        output_path = self.output_dir.get()
        config_path = self.config_file.get()
        
        if not os.path.isdir(input_path):
            messagebox.showerror("Error", "Invalid input directory")
            return

        if not os.path.isdir(output_path):
            messagebox.showerror("Error", "Invalid output directory")
            return

        if not os.path.isfile(config_path):
            messagebox.showerror("Error", "Invalid config file")
            return

        # Set output file path
        self.output_folder = output_path
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_file = os.path.join(self.output_folder, f"ATS_output_{timestamp}.tsv")

        try:
            self.compile_transcripts()
                            
            self.progress_label.config(text=f"Finished processing {self.pdf_count} PDFs")
            self.progress_bar["value"] = 100

            # Show success message
            messagebox.showinfo("Success", "PDFs processed successfully")

            # Close GUI
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def compile_transcripts(self):
        self.progress_bar["value"] = 0
        self.progress_label.config(text="Processing...")

        for filename in os.listdir(self.input_dir.get()):
            if filename.endswith(".pdf"):
                self.transcript_paths.append(os.path.join(self.input_dir.get(), filename))

        self.pdf_count = len(self.transcript_paths)
        output_data = []

        # Read PDFs and update progress bar
        for transcript in self.transcript_paths:
            self.update_progress(self.num_processed_pdfs, self.pdf_count)
            parser = PDF_Parser(transcript, self.config_file.get())
            output_data.append(parser.read_transcript())
        
        # Save to TSV file
        df = pd.DataFrame(output_data)
        os.makedirs(self.output_folder, exist_ok=True)
        df.to_csv(self.output_file, sep='\t', index=False)

    def update_progress(self, current, total):
        self.progress_bar["value"] = int((current / total) * 100)
        self.root.update_idletasks()
        self.num_processed_pdfs += 1

def run_gui():
    root = tk.Tk()
    app = ATSApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
