import math
import os
import random

import pyttsx3
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *


WIDTH = 1080
HEIGHT = 1920
FONT = ImageFont.truetype(font="assets/montserrat_semibold.ttf", size=100)

# Take a list of strings and save each string to a .wav file
def generate_audio(voice=0, text_list=["The quick brown fox jumps over the lazy dog", "Lorem Ipsum is simply dummy text of the printing and typesetting industry."], output_directory="generate_audio_output"):
    # Initialise TTS engine and set desired voice
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voice].id)

    # Ensure directory exists and also clear existing .wav files
    os.makedirs(f"media/{output_directory}", exist_ok=True)
    for file in os.listdir(f"media/{output_directory}"):
        if file.endswith(".wav"):
            os.remove(os.path.join(f"media/{output_directory}", file))

    # Save each text to its own file
    for i, text in enumerate(text_list):
        engine.save_to_file(text, f"media/{output_directory}/{output_directory}_{i}.wav")
    engine.runAndWait()


def process_audio(input_directory="generate_audio_output", output_directory="process_audio_output"):
    # Add reverb to sound more spacious
    board = Pedalboard([Reverb(room_size=0.4, damping=1, wet_level=0.2, dry_level=0.3)])

    # Ensure directory exists and also clear existing .wav files
    os.makedirs(f"media/{output_directory}", exist_ok=True)
    for file in os.listdir(f"media/{output_directory}"):
        if file.endswith(".wav"):
            os.remove(os.path.join(f"media/{output_directory}", file))

    # Iterate through input directory and save processed .wav files into output directory
    for i in range(sum((len(files) for _, _, files in os.walk(f"media/{input_directory}")))):
        with AudioFile(f"media/{input_directory}/{input_directory}_{i}.wav") as input_audio:
            with AudioFile(f"media/{output_directory}/{output_directory}_{i}.wav", 'w', input_audio.samplerate, input_audio.num_channels) as output_audio:
                while input_audio.tell() < input_audio.frames:
                    chunk = input_audio.read(input_audio.samplerate)
                    effected = board(chunk, input_audio.samplerate, reset=False)
                    output_audio.write(effected)


def generate_text(text_list=["The quick brown fox jumps over the lazy dog", "Lorem Ipsum is simply dummy text of the printing and typesetting industry."], output_directory="generate_text_output"):
    # Ensure directory exists and also clear existing .png files
    os.makedirs(f"media/{output_directory}", exist_ok=True)
    for file in os.listdir(f"media/{output_directory}"):
        if file.endswith(".png"):
            os.remove(os.path.join(f"media/{output_directory}", file))

    # Save each text to its own file
    for i, text in enumerate(text_list):
        text_image = Image.new("RGBA", (WIDTH, HEIGHT), color=(0, 0, 0, 0))
        text_image_draw = ImageDraw.Draw(text_image)

        _, _, text_width, text_height = text_image_draw.textbbox((0, 0), text, font=FONT)
        text_image_draw.text(((WIDTH-text_width)/2, (HEIGHT-text_height)/2), text, font=FONT, fill=(255, 255, 255))

        text_image.save(f"media/{output_directory}/{output_directory}_{i}.png")


def generate_video(gameplay_video_file="minecraft.mp4", background_audio_file="the_begin.wav", voice_audio_file="process_audio_output.wav", output_file="generate_video_output.mp4"):
    gameplay_video = VideoFileClip(f"assets/{gameplay_video_file}")
    background_audio = AudioFileClip(f"assets/{background_audio_file}")
    voice_audio = AudioFileClip(f"media/{voice_audio_file}")

    video_length = math.ceil(voice_audio.duration)
    start_time = random.randint(0, math.floor(gameplay_video.duration) - video_length)
    gameplay_video = gameplay_video.subclip(start_time, start_time + video_length)

    background_audio = background_audio.subclip(0, video_length)
    background_audio = background_audio.volumex(0.05)

    final_video = gameplay_video
    final_audio = CompositeAudioClip([background_audio, voice_audio])

    final_output = final_video.set_audio(final_audio)
    os.makedirs("media", exist_ok=True)
    final_output.write_videofile(f"media/{output_file}", fps=60)


if __name__ == "__main__":
    generate_text()