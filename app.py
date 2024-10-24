import logging
import sys
import json

from flask import Flask, request, make_response
from werkzeug.utils import secure_filename

from config import DEFAULT_DOCUMENTS_PATH,DEFAULT_QUESTIONS_PATH
from bot import Bot

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
        2. files: [relevant_documents]: pdf files, json files
    """
    logger.info(f"request files are {request.files}")
    if request.method == 'POST': 
        logger.info(f"saving question file")
        questions_file = request.files['questions_file'] 
        questions_file_path = f"{DEFAULT_QUESTIONS_PATH}/{secure_filename(questions_file.filename)}"
        questions_file.save(questions_file_path)
        logger.info(f"saved question file")

        uploaded_files = request.files.getlist("relevant_documents")
        print(f"uploaded files {uploaded_files}")
        all_relevant_document_file_paths = []
        for relevant_document_files in uploaded_files:
            try:
                logger.info(f"saving relevant doc {relevant_document_files.filename}")
                relevant_document_file_path = f"{DEFAULT_DOCUMENTS_PATH}/{secure_filename(relevant_document_files.filename)}"
                relevant_document_files.save(relevant_document_file_path)
                all_relevant_document_file_paths.append(relevant_document_file_path)
                logger.info(f"saved relevant doc {relevant_document_files.filename}")
            except Exception as ex:
                logger.error(f"error saving document {relevant_document_files.filename} due to {ex}")
        query_responses = {}
        response = make_response(query_responses)
        try:
            bot = Bot()
            bot.add_files_to_store(all_relevant_document_file_paths)
            
            questions = []
            with open(questions_file_path) as fp:
                questions = json.load(fp)

            for query in questions:
                try:
                    logger.info(f"asking query f{query}")
                    llm_answer = bot.ask_question(query)
                    query_responses[query] = llm_answer
                    logger.info(f"got query response f{query}")
                except Exception as q_ex:
                    logger.info(f"query {query} failed with {q_ex}")
                
            response = make_response(query_responses)
            response.status_code = 201                
        except Exception as ex:
            logger.error(f"Exception {ex} while querying the bot")
            response.status_code = 500

        return response

if __name__ == '__main__': 
    logger.info("started app default port 5000")
    app.run(debug = True) 
