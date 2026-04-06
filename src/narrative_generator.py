import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def story_generator(user_prompt):
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")

    system_prompt = """
    You are a professional visual storyteller. Your task is to take a user's high-level idea and break it down into exactly 5 distinct, visually descriptive scenes for an AI image generator. Each scene should be a concise paragraph (under 50 words) that captures a key moment in the story. Ensure the scenes have a consistent style (e.g., fantasy, sci-fi) and flow logically to form a mini-narrative. The final output must be a JSON object with keys "scene_1", "scene_2", "scene_3", "scene_4", and "scene_5".
    """
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        scene_text = response.choices[0].message.content
        scenes = json.loads(scene_text)
        return scenes
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred with Groq: {e}")
        return {}

if __name__ == '__main__':
    test_prompt = "A curious wizard discovers an ancient, glowing artifact in a forgotten library."
    scenes_dict = story_generator(test_prompt)
    if scenes_dict:
        print("Generated Scenes:")
        for key, value in scenes_dict.items():
            print(f"- {key}: {value}")
