import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from dotenv import load_dotenv

load_dotenv()
stability_api_key = os.getenv("STABILITY_API_KEY")


if stability_api_key is None:
    raise ValueError("STABILITY_API_KEY environment variable is not set.")

# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

stability_api = client.StabilityInference(
    key=stability_api_key, 
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0",
)

def generate_image(prompt, filename):
    print(f"Generating image for: {prompt}")

    answers = stability_api.generate(
        prompt=prompt,
        steps=50,
        cfg_scale=8.0,
        width=512,
        height=512,
        samples=1,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again."
                )
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                image_path = os.path.join('data', filename)
                img.save(image_path)
                print(f"Image successfully saved to: {image_path}")

if __name__ == '__main__':
    test_prompt = "A curious wizard discovers an ancient, glowing artifact in a forgotten library."
    generate_image(test_prompt, "scene_1.png")