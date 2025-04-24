# This function reads a file of formats docx, txt

import textract
import os

def read_text_from_file(filepath):
    '''
    Читает текст из файла в зависимости от расширения.
    Поддерживаются: .txt, .docx
    '''
    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.docx':
        return textract.process(filepath).decode('utf-8')
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {ext}")
