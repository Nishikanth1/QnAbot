# QnAbot
q and a bot for answering question from a given set of documents


# Setup

1. download and setup ollama
    * ollama pull ollama:tinyllama
    * ollama serve
2. cd into **docker** folder in repo
    * docker compose up -d
3. check python flask app is running
    * docker ps 
4. find ip/port for request using docker logs
    * find logs like `Running on http:`


# Usage
1. via curl command
```
curl --location --request POST 'http://192.168.68.108:5000/v1/bot/question' \
--form 'questions_file=@"/home/nishikanth/Projects/llm/localtesting/question.json"' \
--form 'relevant_documents=@"/home/nishikanth/Projects/llm/localtesting/deloitte-soc2-short.pdf"'
```
2. we are hitting the API /v1/bot/question
    * 2 file inputs
    * *    questions_file
    * *    relevant_documents


