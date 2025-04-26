import base64
import mimetypes
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


class ImageQA(BaseModel):
    model: str = "gpt-4.1-mini"

    def image_encode(self, image_source: str):
        """ This function automatically determines the MIME type and encodes the image to base64."""
        mime_type, _ = mimetypes.guess_type(image_source)
        if mime_type is None:
            raise ValueError(f"Mime type determination failed for {image_source}")

        with open(image_source, "rb") as image_content:
            encoded_image_string = base64.b64encode(image_content.read()).decode('utf-8')
            return f"data:{mime_type};base64,{encoded_image_string}"

    def ask_imagae(self, prompt, image_url):
        client = OpenAI()
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url,
                                          "detail": "high", }
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        return response


if __name__ == "__main__":
    img = ImageQA()
    prompt = "I am providing you an image of a sequence diagram in UML. " \
               "Please generate the PLANTUML code for this diagram"

    image_source = "/Users/joyeed/openai_examples/openai_examples/output_3.png"
    image_url = img.image_encode(image_source)
    response = img.ask_imagae(prompt, image_url)
    print(response.choices[0].message.content)
