# News Text Summarization


## Proof of Concept (Milestone 1)
I completed the proof of concept in a Kaggle notebook that can be found [here](https://www.kaggle.com/thomaslazarus/summarization-comparison). I ran a article summarization using the T5, BERT, GPT, DistilBERT, GPT2, and Pegasus. I should probably look at a concrete way to define correct summarizations to better choose the model to use.

## Web Scraper (Milestone 2)
The scraper can be found in `newssite/newssite/apps/news/web_scraper.py`. The scraper checks the rss feeds of The Verge, Huffpost, Independent, Wired, and Cnet. More site's can be implemented relativley simply. 

## Model Implementation
Before running the web server make sure you cd into `newssite/apps/summarizer/` and inside of a python shell run:
```python
from tranformers import AutoModelForSeq2SeqLM
model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-cnn_dailymail")
model.save_pretrained('model')
```
This will save the pretrained model to decrease downloading times. 
