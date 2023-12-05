import base64
import requests
import os

with open('key1.txt', 'r') as file:
    api_key = file.readline()

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_name(folder_path, limit=10, extensions=['.jpg', '.jpeg', '.png', '.JPG', '.PNG', '.JPEG', '.webp']):
  image_names = [f for f in os.listdir(folder_path) if f.endswith(tuple(extensions))]
  return image_names[:min(len(image_names), limit)]

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


folder_path = 'images'
# WARNING: Unless we're sure, don't increase too much, too much $$$$ 
LIMIT = 1
image_names = get_image_name(folder_path, LIMIT)

prompt = "What’s dangerous about this image in one sentence?"
for image in image_names:
  image_path = f"images/{image}"
  print(image_path)
  base64_image = encode_image(image_path)

  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": prompt},
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    # NOTE: this is the max amount of output words
    "max_tokens": 30
  }

  # Make the API request 
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  print(response.json())