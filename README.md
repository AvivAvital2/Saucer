Saucer is a simple wrapper for spaCy NLP framework (v2.1.3) with S3 support for model storage. <br>
Created mainly to fit spaCy and its en_core_web_lg-2.1.0 model in AWS Lambda.<br>
Saucer was made to "live" within Lambda, heavily relying on S3 to load related files.<br>
Note that in case executed locally, a slow connection can greatly affect the performance<br>

Below example is quite similar to the native spaCy example.<br>
In addition the new __init_s3_connection()__, note __set_data_path()__ and __load()__ both use default locations.
```python
import spacy

#Initialize connection with S3, where prefix contains 'en_core_web_xx-2.1.0'
#Currently supporting sm, md and lg as models
spacy.init_s3_connection('s3_bucket', 's3_prefix', 'en_core_web_lg-2.1.0')
spacy.util.set_data_path()
nlp = spacy.load()

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

To use:
1. Download the desired en_core_web model (either [SM](https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-2.1.0), [MD](https://github.com/explosion/spacy-models/releases/tag/en_core_web_md-2.1.0) or [LG](https://github.com/explosion/spacy-models/releases/tag/en_core_web_lg-2.1.0))
1. Extract the model 
1. Upload the entire __en_core_web_xx-2.1.0/en_core_web_xx/en_core_web_xx-2.1.0__ directory to S3, where xx is the model you selected earlier
1. Specify the bucket, prefix and your model using spacy.init_s3_connection as in the example above.

__spaCy vs Saucer in Lambda - Benchmark__<br>
![spaCy vs Saucer in Lambda - Benchmark](https://github.com/AvivAvital2/Saucer/blob/master/image.png)
