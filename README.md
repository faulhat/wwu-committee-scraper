## Viewing the webpage templates
Dylan Pugh

```
cd frontend/
npm install
npm run dev
```

## Setting up the Virtual Environment for backend App
Ethan Griffith

When cloning the repo, do this:
```
cd flaskapp/
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```

## Crawler
Tom Faulhaber

The setup process is the same as with the server program; just run the same commands in the `crawler` directory.

Then, you can do `./wwucrawler.py -h` for instructions on how to use the program.

## Summarizer
Kyle Downing

The summarization process requires the use of the Ollama application to support
running LLMs locally. The application is not required to run the program, but the summarization
and data extraction features of the summarizer is only supported with the use of Ollama.

- [Install Ollama](https://ollama.com/download)

After installation, open the Ollama Application and keep the process running as it will serve
as the backend server for requests from the summarizer. 

Next you need to pull a model from Ollama to use for the summarizer. Choose a model to use for the 
summarizer from this list. In terms of performance, you should have 8GB of RAM to run
7B models, 16GB to run the 13B models, and 32GB to run the 33B models. I would recommend the **llama3.2** model, and I am using a system with 8GB of RAM.

- [Model Library](https://github.com/ollama/ollama?tab=readme-ov-file#model-library)

Pull a model with **pull**, and check that it is present with **list**:
```
ollama pull [model_name]
ollama list
```

Navigate to the committee_scraper directory and run the **setup** script. Once all packages are installed
run the program with the **run** script. The script takes two arguments: The name of the model you want to use
for this invocation of the summarizer, and the minimum ___score___ of the pages you want to summarize. Pass in the 
model name as it appears when you called the **list** command. 

```
cd committee_scraper
./setup
./run [model_name] [min_score]
```
