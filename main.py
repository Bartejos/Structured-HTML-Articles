from openai import OpenAI
from bs4 import BeautifulSoup

# Read API key value
keyFile = open("key.txt", "r")
api_key = keyFile.readline()
keyFile.close()

client = OpenAI(api_key=api_key)

file_r = open("Zadanie dla JJunior AI Developera - tresc artykulu.txt", "r")
file_w = open("artykul.html", "w")

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system", 
            "content": [
                {
                    "type": "text",
                    "text": "You will be provided with an article and your task is to structurize it with HTML tags, however use them only as if they are inside the body tag. Moreover you should propose where is it worth to insert images and also write prompts for generating these images in the alt attribute and image caption."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": file_r.read()
                }
            ]
        }
    ]
)

soup = BeautifulSoup(completion.choices[0].message.content, "html.parser")

for img in soup.find_all("img"):
    alt_text = img.get("alt")
    response = client.images.generate(
        prompt=alt_text,
        size="1024x1024"
    )
    new_src_value = response.data[0].url
    img["src"] = new_src_value

file_w.write(soup.prettify())

client.close()
file_r.close()
file_w.close()