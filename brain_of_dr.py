# step 1 setup api key 
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")



# step 2 comvert image to required formatee
import base64

image_path="acne.jpg"

def encode_image_to_base64(image_path):
    """
    Reads an image from the given path and returns its base64 encoded string.
    Args:
        image_path (str): Path to the image file
    Returns:
        str: Base64 encoded string of the image
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')


# step 3 steup multi modal llm
from groq import Groq
query="is something wrong with my face?"
model="meta-llama/llama-4-scout-17b-16e-instruct"
def analyize_image_with_query(query, image_base64, model):
    client = Groq(api_key=GROQ_API_KEY)
    
   

    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

