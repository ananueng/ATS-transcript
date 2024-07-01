import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd
from tkinter import ttk
from app.reader import read_transcript

def run_gui():
    def select_directory():
        dir_path = filedialog.askdirectory(initialdir=input_dir.get())
        if dir_path:
            input_dir.set(dir_path)

    def process_files():
        input_path = input_dir.get()
        if not os.path.isdir(input_path):
            messagebox.showerror("Error", "Invalid input directory")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".tsv",
                                                   filetypes=[("TSV files", "*.tsv"), ("All files", "*.*")])
        if output_file:
            try:
                compile_transcripts()
                transcript_paths = []
                progress_bar["value"] = 0
                progress_label.config(text="Processing...")
                
                for filename in os.listdir(input_dir):
                    if filename.endswith(".pdf"):
                        transcript_paths += os.path.join(input_dir, filename)

                pdf_count = transcript_paths.count()
                num_processed_pdfs = 0
                
                # Read PDFs and update progress bar
                for transcript in transcript_paths:
                    update_progress(num_processed_pdfs, pdf_count)
                    read_transcript(output_file)
                    num_processed_pdfs += 1
                    df = pd.DataFrame(output_data)
                    
                
                
                progress_label.config(text=f"Finished processing {pdf_count} PDFs")
                progress_bar["value"] = 100

                # Show success message
                messagebox.showinfo("Success", "PDFs processed successfully")

                # Close the GUI window
                root.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_progress(current, total):
        progress_bar["value"] = int((current / total) * 100)
        root.update_idletasks()

    root = tk.Tk()
    root.title("ATS Tool")

    default_input_path = os.path.join(os.getcwd(), "data", "input")
    input_dir = tk.StringVar(value=default_input_path)

    tk.Label(root, text="Input Directory:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=input_dir, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_directory).grid(row=0, column=2, padx=10, pady=10)

    tk.Button(root, text="Process PDFs", command=process_files).grid(row=1, columnspan=3, pady=10)

    progress_label = tk.Label(root, text="")
    progress_label.grid(row=2, columnspan=3, pady=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.grid(row=3, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
