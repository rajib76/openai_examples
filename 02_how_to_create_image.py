import base64
import os

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI()

PROMPT="""
I am developing an application where a user will hit a chatbot URL.
the url will then call a LLM based chat application running in a Kubernetes pod
on AWS Kubernetes service. Any exception from the pod will be pushed to cloud watch. Aurora PGVECTOR
is the vector database. Please create me a UML sequence diagram which must use AWS icons.
"""

img = client.images.generate(
    model="gpt-image-1",
    prompt=PROMPT,
    n=3,
    size="1536x1024"
)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output_0.png", "wb") as f:
    f.write(image_bytes)

image_bytes = base64.b64decode(img.data[1].b64_json)
with open("output_1.png", "wb") as f:
    f.write(image_bytes)

image_bytes = base64.b64decode(img.data[2].b64_json)
with open("output_3.png", "wb") as f:
    f.write(image_bytes)