# reader.py
import fitz  # PyMuPDF
import pandas as pd
import os

class PDF_Parser:
    def __init__(self, filepath, config):
        self.transcript_data = []
        self.transcript_path = filepath
        self.config_df = config
        # self.course_filter = self.config_df.index.tolist()
        self.filtered_data = {key: '' for key in self.config_df.index.tolist()}

    def read_transcript(self):
        with fitz.open(self.transcript_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                self.transcript_data += self.read_page(text)
                
        for chunk_index, chunk in enumerate(self.transcript_data):
            for course in self.filtered_data.keys():
                course_department = course.split()[0]
                course_number = course.split()[1]
                if (chunk == course_department and chunk_index + 3 < len(self.transcript_data)):
                    if (self.transcript_data[chunk_index + 1] == course_number):
                        grade = self.transcript_data[chunk_index + 3]
                        self.filtered_data[course] = grade
                                
        return self.filtered_data

    def read_page(self, text=str):
        # TODO: edit
        return [word.strip() for word in text.split('\n')]