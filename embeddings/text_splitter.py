import os
import sys
import logging
import json


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveJsonSplitter

from .file_loader import FileReader

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logging.basicConfig(encoding='utf-8', format='%(asctime)s %(levelname)s  %(message)s', level=logging.INFO)

class TextSplitter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_extension = os.path.splitext(file_path)[1].lower()
        self.loader = FileReader(file_path)

    def split(self):
        if self.file_extension == '.pdf':
            splitter = RecursiveCharacterTextSplitter(
                                                            chunk_size=1000,
                                                            chunk_overlap=200,
                                                            length_function=len,
                                                            is_separator_regex=False,
                                                    )
            for chunk in self.loader.read():
                split = splitter.split_documents([chunk])
                yield split            
        elif self.file_extension == ".json" or self.file_extension == ".jsonl":
            splitter = RecursiveJsonSplitter(max_chunk_size=300)
            for chunk in self.loader.read():
                # TODO find better way to split json
                is_json_lines = self.file_extension == ".jsonl"
                if not is_json_lines:
                    parsed_chunk = json.loads(chunk.page_content.replace("\'", "\""))
                else:
                    parsed_chunk = [chunk.page_content]
                split = splitter.split_text(parsed_chunk, convert_lists=True)
                yield split
                
        else: 
            raise ValueError(f"Unknown extension {self.file_extension} for text splitting")        

if __name__ == "__main__":
    splitter = TextSplitter("logs_lines.jsonl")
    print([l for l in splitter.split()])
    
    splitter = TextSplitter("logs_json.json")
    print([l for l in splitter.split()])    
    
    splitter = TextSplitter("./data/documents/Deloitte-SOC2.pdf")
    print([l for l in splitter.split()])
        