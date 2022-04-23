import os

from docx import Document
# from win32com import client as wc
from tqdm import tqdm
import abc
from abc import ABC


class FileConvertor(ABC):
    def __init__(self, path, target):
        self.path = path
        self.target = target

    @abc.abstractmethod
    def execute_file_convert(self):
        pass

    def __str__(self):
        pass


class Doc2docx(FileConvertor):
    def __init__(self, path, target):
        super().__init__(path, target)

    def execute_file_convert(self):
        docPath = self.path
        docxPath = self.target

        fileList = os.listdir(docPath)

        w = wc.Dispatch('Word.Application')
        for file in tqdm(iterable=fileList, desc="word => docx Converting"):
            try:
                docName = docPath + file
                docxName = docxPath + file + 'x'
                doc = w.Documents.Open(docName)
                doc.SaveAs(docxName, 16)
                doc.Close()
            except Exception:
                print(file, " ERROR!")
                continue
        w.Quit()
        print("Finished!")


class Docx2txt(FileConvertor):
    def __init__(self, path, target):
        super().__init__(path, target)

    def execute_file_convert(self):
        filePath = self.path
        txtPath = self.target

        fileList = os.listdir(filePath)

        for file in tqdm(iterable=fileList, desc="docx => txt Converting"):
            try:
                document = Document(os.path.join(filePath, file))
                txtFileName = file.split('.docx')[0] + '.txt'

                txt = open(os.path.join(txtPath, txtFileName), 'w', encoding='UTF-8')
                for i in document.paragraphs:
                    _ = txt.write(i.text)
                txt.close()
            except Exception:
                print(file, " ERROR!")
                continue
        print("Finished")
