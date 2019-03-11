Saucer is a simple fork from spaCy NLP framework with S3 support for model storage. 
Created mainly to fit spaCy and its en_core_web_lg-2.0.0 model in AWS Lambda
Saucer was made to "live" within Lambda, heavily relying on S3 to load related files.
A slow connection can greatly affect the performance

Quite similar to the native spaCy example:
```python
import spacy
from os.path import dirname, join

spacy.util.set_data_path(dirname(spacy.__file__))
nlp = spacy.load(join(dirname(spacy.__file__), 'en_core_web_lg-2.0.0'))

# Process whole documents
text = (u"When Sebastian Thrun started working on self-driving cars at "
        u"Google in 2007, few people outside of the company took him "
        u"seriously. “I can tell you very senior CEOs of major American "
        u"car companies would shake my hand and turn away because I wasn’t "
        u"worth talking to,” said Thrun, now the co-founder and CEO of "
        u"online higher education startup Udacity, in an interview with "
        u"Recode earlier this week.")
doc = nlp(text)

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)

# Determine semantic similarities
doc1 = nlp(u"my fries were super gross")
doc2 = nlp(u"such disgusting fries")
similarity = doc1.similarity(doc2)
print(doc1.text, doc2.text, similarity)
```
