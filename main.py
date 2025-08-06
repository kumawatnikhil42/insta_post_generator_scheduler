import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from typing import TypedDict
from caption_generator import generate_caption
from image_generator import generate_image
from post_to_instagram import post_image
from reflection_agent import refine_prompt, refine_caption_for_post, generate_daily_prompt

load_dotenv()

class InstaState(TypedDict):
    base_caption: str
    caption: str
    base_prompt: str
    prompt: str
    image_path: str

# Node 1: Base Image Prompt Generator
def base_prompt_node(state: InstaState):
    print("📂 Reading subject from subject.txt...")
    with open("subject.txt", "r") as f:
        subject = f.read().strip()
    print(f"🎯 Current subject: {subject}")

    fresh_prompt = generate_daily_prompt(subject)
    print(f"✅ Today's unique prompt: {fresh_prompt}")
    return {"base_prompt": fresh_prompt}

# Node 2: Prompt Reflection
def prompt_reflection_node(state: InstaState):
    print("🔍 Refining image prompt...")
    refined_prompt = refine_prompt(state["base_prompt"])
    print("✅ Refined prompt:", refined_prompt)
    return {"prompt": refined_prompt}

# Node 3: Base Caption Generator
def base_caption_node(state: InstaState):
    print("📝 Generating base Instagram caption...")
    base_caption = generate_caption(state["prompt"])
    print("✅ Base caption generated:", base_caption)
    return {"base_caption": base_caption}

# Node 4: Caption Reflection
def caption_reflection_node(state: InstaState):
    print("🔍 Refining caption...")
    refined_caption = refine_caption_for_post(state["base_caption"])
    print("✅ Refined caption:", refined_caption)
    return {"caption": refined_caption}

# Node 5: Image Generator
def image_node(state: InstaState):
    print("🎨 Generating AI image with refined prompt...")
    image_path = generate_image(state["prompt"])
    print("✅ Image generated:", image_path)
    return {"image_path": image_path}

# Node 6: Instagram Post
def post_node(state: InstaState):
    print("📤 Uploading image to Instagram...")
    post_image(state["image_path"], state["caption"])
    print("✅ Post successfully uploaded!")
    return {}

# Build workflow
graph = StateGraph(InstaState)
graph.add_node("base_prompt_generator", base_prompt_node)
graph.add_node("prompt_reflection", prompt_reflection_node)
graph.add_node("base_caption_generator", base_caption_node)
graph.add_node("caption_reflection", caption_reflection_node)
graph.add_node("image_generator", image_node)
graph.add_node("post_instagram", post_node)

# Correct order
graph.add_edge("base_prompt_generator", "prompt_reflection")
graph.add_edge("prompt_reflection", "base_caption_generator")
graph.add_edge("base_caption_generator", "caption_reflection")
graph.add_edge("caption_reflection", "image_generator")
graph.add_edge("image_generator", "post_instagram")

# ✅ Only one entry point
graph.set_entry_point("base_prompt_generator")

if __name__ == "__main__":
    print("🚀 Starting Instagram AI Post Workflow with Reflection Agent...")
    workflow = graph.compile()
    workflow.invoke({})
    print("🏁 Workflow complete.")
