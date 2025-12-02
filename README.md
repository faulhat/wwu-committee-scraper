## To run the full program

In the project root directory, do:
```
./setup_all && ./run_all
```

This will start a local server on port 5000, run the web crawler in the background and run the frontend, it will say " * Running on http://---.0.0.1:5000" To check on the crawler's progress, do:
```
tail -f crawler.log
```
in a separate window.

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

The setup process is the same as with the server program; just run the same commands in the `wwucrawler` directory.

Then, you can do `python crawler -h` for instructions on how to use the program.

## Summarizer
Kyle Downing

To ensure the smooth operation of the summarizer program across a wide range of enviorments, the summarizer will use Google Gemini's GenAi API. This API offers a free tier, and will allow the program to make API requests with a strict limit. The limit will be enforced and implemented within the program, to avoid sending multiple requests that may result in an error.

- [Google GenAI Docs](https://ai.google.dev/gemini-api/docs)

If you need, read the documentation to understand how to use the API to generate responses. The document covers the differnet models offered, how to initialize them and query them, as well as all other useful information.

If you are using this program for the first time, you will need an API key. This may be proivded with the project in an enviorment variable, or you could generate your own. Note that with a shared API key, requests from differnet hosts at once may overload the rate limit. Thus, if you are running this project on a local machine you may want to generate your own API key anyways. The following link will direct you to the page where you can request to create an API key. You will need a google account to link this key to, but you will be able to proceeed with a free tier. This free tier will have a strict rate limit and token limit, which should not be exceeded. 

- [API Key](https://aistudio.google.com/api-keys)

Once you have an API key, you should be able to proceed with running the summarizer. Navigate to the **committee_scraper** directory and ensure you will run the program on an interperter with the relevant dependicies installed. The most important of which is the **google-genai** package. This will contian the functions needed to use the API:

Navigate to the committee_scraper directory and run the **setup** script. This should install all relevant depenencies as described above, but if not you can source the python interperter created by the setup script and install it manually using pip. Once all packages are installed you should be able to run the program. The program has a defined period to sleep after each API call, this is to ensure the rate limit is not exceeded. Note that this means the program will run slow, but it should only need to be ran once. The last thing to check before running the scraper is to ensure the crawler has created the database and updated it. This way, the summarizer will have content to preform operations on.

To run the program, navigate to the committee_scraper directory and use the **run** script. This will begin the program, and show a live print log of the progress as each entry is summarized.

```
cd committee_scraper
./setup
./run
```
