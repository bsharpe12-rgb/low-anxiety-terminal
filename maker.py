import os
import json
import random
import asyncio
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, ImageClip

# ==========================================
# 1. DYNAMIC BACKGROUND ASSET PICKER
# ==========================================
def get_random_background_clip(folder_path="backgrounds"):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        raise FileNotFoundError(f"⚠️ '{folder_path}' folder was missing. Created it! Please add assets to it.")
    
    # Accept both video and image formats
    valid_extensions = ('.mp4', '.mov', '.avi', '.png', '.jpg', '.jpeg')
    clips = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
    
    if not clips:
        raise FileNotFoundError(f"⚠️ No usable assets found in '{folder_path}'. Place video or image files there!")
        
    chosen_clip = random.choice(clips)
    print(f"🎲 Randomly selected background asset: {chosen_clip}")
    return chosen_clip

# ==========================================
# 2. DYNAMIC SCRIPT DATA BRIDGE
# ==========================================
def get_dynamic_script_text(json_path="business_bundle.json"):
    print(f"📖 Reading dynamic content from {json_path}...")
    if not os.path.exists(json_path):
        return (
            "The market is moving, but our strategy stays the same. "
            "Building wealth is supposed to be boring. Head to the link in my bio "
            "to grab my free Low-Anxiety Investing Blueprint and let's get started."
        )

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            
        script_text = data.get("daily_voiceover_script", "")
        if script_text:
            return script_text
            
    except Exception as e:
        print(f"⚠️ Error reading JSON payload: {e}")
        
    return "The market is moving, but our strategy stays the same. Grab my free blueprint in my bio."

# ==========================================
# 3. TTS VOICEOVER GENERATOR (ASYNC)
# ==========================================
async def generate_voiceover(text, output_path="voiceover_audio.mp3"):
    print("🎙️ Generating AI voiceover narration...")
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, "en-US-AndrewNeural")
        await communicate.save(output_path)
        print("✅ AI voiceover file saved successfully!")
    except Exception as e:
        print(f"⚠️ edge-tts failed or not installed ({e}). Attempting gTTS fallback...")
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', tld='com')
        tts.save(output_path)
        print("✅ AI voiceover file saved successfully (via gTTS fallback)!")

# ==========================================
# 4. HIGH-RETENTION COMPILER ENGINE (MoviePy v2.x Version)
# ==========================================
def create_viral_video(asset_source, voiceover_source, music_source, output_filename="final_viral_video.mp4"):
    print("🎬 Initializing High-Retention Video Engine...")
    
    bg_clip = None
    voice_clip = None
    music_clip = None
    final_video = None
    
    try:
        # 1. Load Audio Narrator
        voice_clip = AudioFileClip(voiceover_source)
        duration = voice_clip.duration
        
        # 2. Load and Prepare Background (Detect if Image or Video)
        is_image = asset_source.lower().endswith(('.png', '.jpg', '.jpeg'))
        
        if is_image:
            print("🖼️ Detected static image background. Converting to video clip...")
            # Use MoviePy v2.x `.with_duration`
            bg_clip = ImageClip(asset_source).with_duration(duration)
        else:
            print("📹 Detected video background clip...")
            bg_clip = VideoFileClip(asset_source)
            # Match duration using MoviePy v2.x `.with_duration` and `.subclipped`
            if bg_clip.duration < duration:
                bg_clip = bg_clip.loop(duration=duration)
            else:
                max_start = max(0, bg_clip.duration - duration)
                start_time = random.uniform(0, max_start)
                bg_clip = bg_clip.subclipped(start_time, start_time + duration)
            bg_clip = bg_clip.with_duration(duration)
            
        # 3. Load and Blend Background Music (Low Volume)
        if os.path.exists(music_source):
            music_clip = AudioFileClip(music_source)
            if music_clip.duration < duration:
                music_clip = music_clip.loop(duration=duration)
            else:
                music_clip = music_clip.subclipped(0, duration)
            
            # Use MoviePy v2.x `.with_volume_scaled`
            music_clip = music_clip.with_volume_scaled(0.08)
            final_audio = CompositeAudioClip([voice_clip, music_clip])
        else:
            print("🎵 No background music file found. Compiling with voice only.")
            final_audio = voice_clip
            
        # 4. Export Final Composite Video using MoviePy v2.x `.with_audio`
        final_video = bg_clip.with_audio(final_audio)
        
        print(f"🚀 Rendering final edit to: {output_filename}...")
        final_video.write_videofile(
            output_filename,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        print("🎉 Video successfully rendered and saved!")
        
    except Exception as e:
        print(f"❌ Rendering Error: {e}")
    finally:
        # Cleanly release files
        if bg_clip: bg_clip.close()
        if voice_clip: voice_clip.close()
        if music_clip: music_clip.close()
        if final_video: final_video.close()

# ==========================================
# 5. RUNTIME EXECUTION
# ==========================================
if __name__ == "__main__":
    try:
        BASE_ASSET = get_random_background_clip("backgrounds")
    except FileNotFoundError as e:
        print(e)
        exit(1)
        
    BACKGROUND_MUSIC = "background_music.mp3"
    VOICEOVER_OUTPUT = "voiceover_audio.mp3"
    
    # Run the JSON parser
    SCRIPT_TEXT = get_dynamic_script_text("business_bundle.json")
    print(f"📣 Generated Script text: \"{SCRIPT_TEXT}\"")
    
    # Run Async TTS Generator
    asyncio.run(generate_voiceover(SCRIPT_TEXT, VOICEOVER_OUTPUT))
    
    # Compile Video
    create_viral_video(
        asset_source=BASE_ASSET,
        voiceover_source=VOICEOVER_OUTPUT,
        music_source=BACKGROUND_MUSIC,
        output_filename="final_viral_video.mp4"
    )
