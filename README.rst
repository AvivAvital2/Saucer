Saucer is a simple fork from spaCy NLP framework with S3 support for model storage. 
Created mainly to fit spaCy and its en_core_web_lg-2.0.0 model in AWS Lambda
Saucer was made to "live" within Lambda, heavily relying on S3 to load related files.
A slow connection can greatly affect the performance
