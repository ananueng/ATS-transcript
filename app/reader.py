# reader.py
import fitz  # PyMuPDF
import pandas as pd
import os

class PDF_Parser:
    def __init__(self, file_path, filter_path):
        self.transcript_data = []
        self.transcript_path = file_path
        # self.course_filter = self.config_df.index.tolist()
        self.filtered_data = {'transcript_file': os.path.basename(file_path), 'name': '', 'uniqname': ''}
        df = pd.read_csv(filter_path)
        self.courses = df.iloc[:, 0]
        self.filtered_data.update({key: '' for key in self.courses})
        
    def read_transcript(self):
        # read the pdf as a list of strings, separated by newlines
        with fitz.open(self.transcript_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                self.transcript_data += [word.strip() for word in text.split('\n')]
                
        for chunk_index, chunk in enumerate(self.transcript_data):
            # for each course of interest
            for course in self.courses:
                course_department = course.split()[0]
                course_number = course.split()[1]
                # check if this part of the transcript matches one of the courses of interest
                if (chunk == course_department and chunk_index + 3 < len(self.transcript_data)):
                    if (self.transcript_data[chunk_index + 1] == course_number):
                        # record the grade
                        grade = self.transcript_data[chunk_index + 3]
                        self.filtered_data[course] = grade
                        
            # check if this part of the transcript has their name
            if chunk == "Page 1" and chunk_index - 1 > 0:
                self.filtered_data['name'] = self.transcript_data[chunk_index - 1].split('Pref:')[-1].strip()
            
            # check if this part of the transcript has their uniqname
            if chunk.split() and chunk.split()[0] == "Uniqname:":
                self.filtered_data['uniqname'] = chunk.split()[1]
            
        return self.filtered_data

    def read_page(self, text=str):
        return 
            
