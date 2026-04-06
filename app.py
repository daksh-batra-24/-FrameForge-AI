import streamlit as st
import os, hashlib, time
from src import narrative_generator, image_generator

# ----------------- Session -----------------
if 'video_path' not in st.session_state:
    st.session_state.video_path = None

st.set_page_config(page_title="Visual StoryTeller AI", page_icon='🌟', layout="wide")
st.title("Visual StoryTeller AI")
st.markdown("Enter a simple idea, and I'll generate a five-scene visual story")

# ----------------- Paths -------------------
DATA_DIR = "data"
RUNS_DIR = os.path.join(DATA_DIR, "runs")
os.makedirs(RUNS_DIR, exist_ok=True)

def _new_run_id(prompt: str) -> str:
    h = hashlib.sha256((prompt.strip() + str(time.time())).encode()).hexdigest()[:10]
    return f"run_{h}"

# user input the prompt
user_prompt = st.text_input("Enter your story idea here:")

# button to trigger the whole process
if st.button("Generate story", use_container_width=True):
    if user_prompt.strip():
        run_id = _new_run_id(user_prompt)
        run_dir_full = os.path.join(RUNS_DIR, run_id)
        os.makedirs(run_dir_full, exist_ok=True)

        with st.spinner("Creating your story......"):
            try:
                scene_dict = narrative_generator.story_generator(user_prompt)
                if scene_dict:
                    st.success("Narrative generated successfully!")
                    image_paths = []

                    def _sorted_items(d: dict):
                        try:
                            return sorted(d.items(), key=lambda kv: int(str(kv[0]).split("_")[-1]))
                        except Exception:
                            return list(d.items())

                    progress = st.progress(0.0, text="Generating images…")
                    ordered = _sorted_items(scene_dict)
                    total = len(ordered)

                    for i, (key, value) in enumerate(ordered, start=1):
                        filename = f"{key}.png"
                        rel_path_under_data = os.path.join("runs", run_id, filename)
                        full_path = os.path.join(DATA_DIR, rel_path_under_data)
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)

                        if not os.path.exists(full_path):
                            image_generator.generate_image(value, rel_path_under_data)

                        image_paths.append(full_path)
                        progress.progress(i / total, text=f"Generated {i}/{total} images")
                    progress.empty()
                    st.success("Images generated successfully!")

                    # video
                    try:
                        from moviepy.editor import ImageSequenceClip
                        video_path = os.path.join(run_dir_full, "story.mp4")
                        video_clip = ImageSequenceClip(image_paths, fps=1)
                        video_clip.write_videofile(video_path, codec='libx264', audio=False, verbose=False, logger=None)
                        st.success("Video created successfully!")
                        st.session_state.video_path = video_path
                    except OSError:
                        st.warning("Video export failed (FFmpeg may not be installed / on PATH). You can still download images below.")
                    except Exception as e:
                        st.error(f"Video creation failed: {e}")

                    # display
                    cols = st.columns(3)
                    for i, p in enumerate(image_paths):
                        with cols[i % 3]:
                            st.image(p, caption=scene_dict.get(f"scene_{i+1}", f"scene_{i+1}"), use_container_width=True)
                            with open(p, "rb") as f:
                                st.download_button("Download image", f.read(), file_name=os.path.basename(p), key=f"dl_img_{i}")
                else:
                    st.error("Failed to generate narrative. Please try again with a different prompt.")
            except Exception as e:
                st.error(f"Error Occurred: {e}")
    else:
        st.warning("Please enter a story idea to begin.")

# video playback
if st.session_state.video_path:
    st.video(st.session_state.video_path)
