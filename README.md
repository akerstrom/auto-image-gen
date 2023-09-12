# Auto-Image-Gen: Automatic Image Generation and Storage Solution
## Overview
Auto-Image-Gen is a robust and dynamic system designed to automatically generate high-quality images based on text prompts. Leveraging the power of the ChatGPT API for textual prompts and Stable Diffusion for image generation, the program offers a seamless and automated solution. It not only generates images but also efficiently stores them in Azure Storage and Azure CosmosDB, offering a one-stop platform for all your image generation and storage needs.

## Features
### ChatGPT API Integration
Uses OpenAI's ChatGPT API to convert text into creative and specific prompts suitable for image generation.

### Stable Diffusion
Employs Stable Diffusion algorithms to generate images that closely match the given prompts, providing a high level of accuracy and quality.

### Azure Storage
Automatically stores the generated images in Azure Storage, offering a secure and reliable storage solution.

### Azure CosmosDB
Metadata and other details of the generated image are saved in Azure CosmosDB, providing fast and scalable access to image data.

### Auto-Scheduling
Automated task scheduler for image generation, allowing users to set the frequency and timing for automatic image generation and storage.

### User Dashboard
Provides a user-friendly dashboard to view, search, and manage generated images and their metadata.

### Technical Architecture
Prompt Generation: Auto-Image-Gen sends a text to the ChatGPT API, which returns a creative prompt suitable for image generation.
Image Creation: The prompt is fed into the Stable Diffusion algorithm, which generates an image based on the text.
Azure Storage: The generated image is then stored in Azure Storage for secure and long-term storage.
Azure CosmosDB: Metadata related to the image, such as the prompt used, timestamp, and image ID, are saved in Azure CosmosDB.
User Dashboard: Users can access and manage these images and their metadata through a web-based dashboard.

