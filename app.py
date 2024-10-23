import logging
import sys

from flask import Flask, request, make_response
from werkzeug.utils import secure_filename

from config import DEFAULT_DOCUMENTS_PATH,DEFAULT_QUESTIONS_PATH

app = Flask(__name__) 
app.logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
app.logger.addHandler(handler)
logger = app.logger


@app.route('/v1/bot/question', methods = ['POST'])
def answer_question(): 
    """
    params: 
    request body:  
        1. file: questions_file: a json file
        2. files: [relevant_documents]: pdf files

    """
    logger.info(f"request files are {request.files}")
    if request.method == 'POST': 
        logger.info(f"saving question file")
        questions_file = request.files['questions_file'] 
        questions_file_path = f"{DEFAULT_QUESTIONS_PATH}/{secure_filename(questions_file.filename)}"
        questions_file.save(questions_file_path)
        logger.info(f"saved question file")

        uploaded_files = request.files.getlist("relevant_documents")
        for relevant_document_files in uploaded_files:
            try:
                logger.info(f"saving relevant doc {relevant_document_files.filename}")
                relevant_document_files_path = f"{DEFAULT_DOCUMENTS_PATH}/{secure_filename(relevant_document_files.filename)}"
                relevant_document_files.save(relevant_document_files_path)
                logger.info(f"saved relevant doc {relevant_document_files.filename}")
            except Exception as ex:
                logger.error(f"error saving document {relevant_document_files.filename}")
        # TODO add the llm machine
        chat_bot_response = [ "api WIP response"]
        response = make_response(chat_bot_response)
        response.status_code = 201
        return response

if __name__ == '__main__': 
    logger.info("started app default port 5000")
    app.run(debug = True) 
