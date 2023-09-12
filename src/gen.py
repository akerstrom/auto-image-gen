from diffusers import DiffusionPipeline
import torch
from PIL import Image

# function that returns date in string format
def get_date():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")


# torch.backends.cuda.max_split_size_mb = 128
pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
# pipe.to("cuda")
pipe.enable_model_cpu_offload() # My 8Gb GPU is not enough. Offload the model to the CPU to save GPU memory

prompt = "A steampunk village nested in the heart of a dense, enchanted forest, with a full moon shining brightly in the background."

image = pipe(prompt=prompt).images[0]
image.save(f"../data/image_{get_date()}.png")
