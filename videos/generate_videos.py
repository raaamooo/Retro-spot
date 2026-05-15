import os
import re
import time
import argparse
from pathlib import Path
from google import genai
from google.genai import types

def parse_markdown_prompts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Global Style
    global_style_match = re.search(r'## GLOBAL STYLE REFERENCE.*?```\n?(.*?)\n?```', content, re.DOTALL)
    global_style = global_style_match.group(1).strip() if global_style_match else ""

    # Extract Character Sheets
    characters = {}
    char_blocks = re.finditer(r'### CHARACTER ([A-Z]) — (.*?)\n.*?```\n?(.*?)\n?```', content, re.DOTALL)
    for match in char_blocks:
        char_letter = match.group(1).strip()
        char_name = match.group(2).strip()
        char_desc = match.group(3).strip()
        # We will match placeholders like [CHARACTER A — THE OLD MAN]
        placeholder = f"CHARACTER {char_letter} — {char_name}".upper()
        characters[placeholder] = char_desc

    # Extract Reels and Shots
    shots = []
    
    # Split by REEL to keep track of reel info
    reel_splits = re.split(r'## REEL (\d+\.\d+) — "(.*?)"', content)
    
    # First part is intro (before any reels), so we iterate from index 1 in steps of 3
    # reel_splits[1] = "1.1"
    # reel_splits[2] = "A Street in Color"
    # reel_splits[3] = "... content of reel 1.1 ..."
    
    for i in range(1, len(reel_splits), 3):
        reel_number = reel_splits[i]
        reel_title = reel_splits[i+1]
        reel_content = reel_splits[i+2]
        
        # Now split shots within this reel
        shot_matches = re.finditer(r'### SHOT (\d+) — (.*?)\n.*?```\n?(.*?)\n?```', reel_content, re.DOTALL)
        for shot_match in shot_matches:
            shot_num = shot_match.group(1).strip()
            shot_title = shot_match.group(2).strip()
            shot_body = shot_match.group(3).strip()
            
            # Replace [GLOBAL STYLE applied]
            if "[GLOBAL STYLE applied]" in shot_body or "[GLOBAL STYLE applied — warm interior color active]" in shot_body:
                # To be safe, just inject it at the top
                shot_body = shot_body.replace("[GLOBAL STYLE applied]", f"GLOBAL STYLE:\n{global_style}\n")
                shot_body = shot_body.replace("[GLOBAL STYLE applied — warm interior color active]", f"GLOBAL STYLE:\n{global_style}\n\nNOTE: Warm interior color active.\n")
            
            # Replace Character placeholders
            for placeholder, desc in characters.items():
                if f"[{placeholder}]" in shot_body:
                    shot_body = shot_body.replace(f"[{placeholder}]", f"CHARACTER REFERENCE:\n{desc}\n")
            
            shots.append({
                "reel_num": reel_number,
                "reel_title": reel_title,
                "shot_num": shot_num,
                "shot_title": shot_title,
                "prompt": shot_body
            })
            
    return shots

def generate_video(client, shot, output_dir, reference_images=None):
    filename = f"Reel_{shot['reel_num'].replace('.', '_')}_Shot_{shot['shot_num']}.mp4"
    filepath = output_dir / filename
    
    if filepath.exists():
        print(f"Skipping {filename} - already exists.")
        return
        
    print(f"\n--- Generating Video: {filename} ---")
    print(f"Reel: {shot['reel_title']} | Shot: {shot['shot_title']}")
    print(f"Prompt length: {len(shot['prompt'])} characters")
    
    try:
        config = types.GenerateVideosConfig(aspect_ratio="9:16")
        if reference_images:
            config.reference_images = reference_images
            print(f"Using {len(reference_images)} reference images.")

        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=shot['prompt'],
            config=config,
        )

        # Poll the operation status until the video is ready.
        while not operation.done:
            print("Waiting for video generation to complete... (sleeping 15s)")
            time.sleep(15)
            operation = client.operations.get(operation)

        # Download the generated video.
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        
        generated_video.video.save(str(filepath))
        print(f"SUCCESS: Saved to {filepath}")
    except Exception as e:
        print(f"FAILED to generate {filename}: {str(e)}")

def load_reference_image(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    return types.VideoGenerationReferenceImage(
        image=types.Image(image_bytes=img_bytes, mime_type="image/jpeg"),
        reference_type="asset"
    )

def main():
    parser = argparse.ArgumentParser(description="Generate Videos with Google Veo 3.1")
    parser.add_argument("--test-parse", action="store_true", help="Only parse and print the shots, do not generate videos.")
    parser.add_argument("--single", action="store_true", help="Only generate the first shot (for testing).")
    args = parser.parse_args()

    md_path = Path(__file__).parent / "RetroSpot_GoogleFlow_Prompts.md"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    print(f"Parsing {md_path.name}...")
    shots = parse_markdown_prompts(md_path)
    print(f"Found {len(shots)} shots total.")
    
    if args.test_parse:
        for s in shots:
            print(f"\n[REEL {s['reel_num']} SHOT {s['shot_num']}] {s['shot_title']}")
            print("-" * 40)
            print(s['prompt'])
            print("=" * 40)
        return

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please export it before running this script: export GEMINI_API_KEY='your_key'")
        return
        
    client = genai.Client()
    
    ref_images = None
    if args.single:
        print("Running in SINGLE mode. Will only generate the first shot.")
        shots = shots[:1]
        
        # Load the extracted video frames as reference images
        base_dir = Path(__file__).parent
        img1 = base_dir / "painting_ref.jpg"
        img2 = base_dir / "retro_outside_ref.jpg"
        if img1.exists() and img2.exists():
            ref_images = [
                load_reference_image(img1),
                load_reference_image(img2)
            ]
        
    for shot in shots:
        generate_video(client, shot, output_dir, reference_images=ref_images)
        
    print("\nAll requested videos have been processed!")

if __name__ == "__main__":
    main()
