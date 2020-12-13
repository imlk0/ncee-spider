import pandas as pd

def read_student_excel(file_path):
    df = pd.read_excel(file_path)
    students = df.T.to_dict().values()
    return students