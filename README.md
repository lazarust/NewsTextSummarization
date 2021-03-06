# News Text Summarization

## The Project

### The Idea
The basic premise for this project was for my Capstone to get my B.S. in Computer Science. I wanted to create a site that would show summarized news articles since
it there is so much and lot of people don't have to the time to read them all. The proof of concept Jupyter Notebook can be found [here](https://github.com/lazarust/JupyterNotebooks/tree/main/NewsSummarization).

#### Current News Sites
These are the current sites that are scraped and summarized:
* The Verge
* NY Times
* Wired
* CNET
* The Onion

### The Future
Even though this project was originally just for my capstone project I plan to continue to work on it to practice my programming skills. 
Some future things I plan to work on and am currently working on:
* Adding VueX as the front end framework
* Create an API to show previous articles
* Add more sites
* Fix the linter
* Deploy the sites to AWS or GCP

## Local Environment
Since this application is using containers via Docker you'll need to start by downloading and installing [Docker](https://www.docker.com/get-started). From there you have wo options. 
> Docker settings: 6 CPUs, >=6GB RAM

1. Using just docker
    * Navigate to the cloned repository
    * Run `docker build`
    * Run `docker run python manage.py runserver 0.0.0.0:8000`
2. Using [docker-compsoe](https://docs.docker.com/compose/install/)
    * Navigate to the cloned repository
    * Run `docker-compose run`
    
**NOTE: The server takes on average 25-30 minutes to start. This is due to it scraping and summarizing all articles on start.**
