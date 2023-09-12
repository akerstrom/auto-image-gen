import base64
import io
import sys
import uuid
from diffusers import DiffusionPipeline
import torch
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
import argparse
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient, ContentSettings
from PIL import Image

load_dotenv()

def log(msg):
    _now = now_string()
    print(f'{_now} - {msg}', flush=True)

def now_string():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def now_file_string():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_prompt(key):
    openai.api_key = key
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "user",
        "content": "Generate a random prompt description for creating an image around 200 characters long."
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )   
    return response.choices[0].message.content

def generate_image(prompt):
    log (f"Prompt: {prompt}")
    # torch.backends.cuda.max_split_size_mb = 128
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
    # pipe.to("cuda")
    pipe.enable_model_cpu_offload() # My 8Gb GPU is not enough. Offload the model to the CPU to save GPU memory

    image: Image = pipe(prompt=prompt).images[0]
    
    id = uuid.uuid4().hex
    s = image.save(f"../data/{id}.png")
    # convert the image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes = image_bytes.getvalue()
    url = save_to_blob_storage(id, image_bytes)
    save_to_cosmos(prompt, id, url)

def get_cosmos_client():
    host = os.getenv("COSMOS_HOST")
    key = os.getenv("COSMOS_KEY")
    client = CosmosClient(host, key)
    return client

def save_to_cosmos(prompt, id, image_url):
    client = get_cosmos_client()
    database_name = os.getenv("COSMOS_DATABASE")
    database = client.get_database_client(database_name)
    container_name = os.getenv("COSMOS_CONTAINER")
    container = database.get_container_client(container_name)
    item = {
        "id": id,
        "prompt": prompt,
        "image_url": image_url,
        "timestamp": now_string()
    }
    container.create_item(item)

def save_to_blob_storage(id, image:bytes):
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")
    container_client = blob_service_client.get_container_client(container_name)
    blob_name = f"{id}.png"
    blob_client = container_client.get_blob_client(blob_name)
    content_settings = ContentSettings(content_type="image/png")
    blob_client.upload_blob(image, blob_type="BlockBlob", content_settings=content_settings)
    url = f"https://semodo.blob.core.windows.net/auto-image-gen/{blob_name}"
    return url

def run(args):
    log("Auto Image Generator")
    # parser = argparse.ArgumentParser(description='Auto Image Generator')
    # parser.add_argument('-a','--action', help='Action', required=False, default="generate")
    # args = vars(parser.parse_args())

    # log(f"#### Enviroment ####")
    # log(f"####################")
    # log(f"####### Args #######")
    # log(f"####################")
    key = os.getenv("OPENAI_API_KEY")
    prompt = get_prompt(key)
    generate_image(prompt)
    
if __name__ == "__main__":
    run(sys.argv[1:])

