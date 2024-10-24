import os
import sys
import logging

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import JSONLoader

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logging.basicConfig(encoding='utf-8', format='%(asctime)s %(levelname)s  %(message)s', level=logging.INFO)

class FileReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file_extension = os.path.splitext(filepath)[1].lower()

    def read(self):
        if self.file_extension == '.pdf':
            loader = PyPDFLoader(self.filepath)
            # lazy loader to handle large files
            lazy_pdf_loader = loader.lazy_load()
            logging.info(f"returning pdf lazy loader for {self.filepath}")
            return lazy_pdf_loader
        if self.file_extension == ".json":
            loader = JSONLoader(
                file_path=self.filepath,
                jq_schema=".",
                text_content=False,
                json_lines=True
            )
            json_lazy_loader = loader.lazy_load()
            return json_lazy_loader
        else:
            raise ValueError(f"Unsupported file type: {self.file_extension}")
        

if __name__ == "__main__":
    loader = FileReader("./data/documents/Deloitte-SOC2.pdf")
    print([l for l in loader.read()])
        