# News Text Summarization

## Proof of Concept (Milestone 1)
I completed the proof of concept in a Kaggle notebook that can be found [here](https://www.kaggle.com/thomaslazarus/summarization-comparison). I ran a article summarization using the T5, BERT, GPT, DistilBERT, GPT2, and Pegasus. I should probably look at a concrete way to define correct summarizations to better choose the model to use.

## Web Scraper (Milestone 2)
The scraper can be found in `newssite/newssite/apps/news/web_scraper.py`. The scraper checks the rss feeds of The Verge, NY Times, Wired, CNET, and The Onion. More sites can be implemented relativley simply. 

## Model Implementation (Milestone 3)
The model will be automatically downloaded when the server starts. Decided to use [Google's Pegasus](https://ai.googleblog.com/2020/06/pegasus-state-of-art-model-for.html) model pretrianed on CNN Dailymail dataset. This dataset was ideal for this implementation of the model because the training data was very similar to the data that was being summarized. 

## Front-End Implementation (Milestone 4)
After spending some time trying to get a stable and reliable deployment working on google kubernetes engine (GKE), I have decided to just run it locally for now.
The costs associated with keeping the compute clusters running using GKE were starting to pile up and since I was not able to 
reliably use the service to create a live deployment of the app, I do not believe I will have the time to trouble shoot it before presenting.

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
