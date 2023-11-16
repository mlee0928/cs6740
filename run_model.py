import base64
import requests

with open('key.txt', 'r') as file:
    api_key = file.readline()

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Replace 'path_to_your_image.jpg' with the path to your actual image file
image_path = "images/baby_woodwork.png"
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "What’s dangerous about this image?"},
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
}

# Make the API request and print out the response
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
print(response.json())