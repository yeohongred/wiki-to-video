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
def generate_audio(voice: int = 0, text_list: list[str] = ["The quick brown fox jumps over the lazy dog", "Lorem Ipsum is simply dummy text of the printing and typesetting industry."], output_directory: str = "generate_audio_output") -> None:
    """
    Initialise TTS engine and set desired voice
    """

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


def process_audio(input_directory: str = "generate_audio_output", output_directory: str = "process_audio_output") -> None:
    """
    Add sound effects like reverb
    """

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


def generate_text(text_list: list[str] = ["The quick brown fox jumps over the lazy dog", "Lorem Ipsum is simply dummy text of the printing and typesetting industry."], output_directory: str = "generate_text_output") -> None:
    """
    Generate .png files of text
    """

    # Ensure directory exists and clear existing .png files
    os.makedirs(f"media/{output_directory}", exist_ok=True)
    for file in os.listdir(f"media/{output_directory}"):
        if file.endswith(".png"):
            os.remove(os.path.join(f"media/{output_directory}", file))

    # Save each text to its own .png file
    for i, text in enumerate(text_list):
        # Set up image
        text_image = Image.new("RGBA", (WIDTH, HEIGHT), color=(0, 0, 0, 0))
        text_image_draw = ImageDraw.Draw(text_image)

        # Wrap text
        lines = ['']
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            if FONT.getlength(line) <= 700:
                lines[-1] = line
            else:
                lines.append(word)
        text = '\n'.join(lines)

        # Draw text in the centre of the screen
        text_image_draw.text(xy=(WIDTH/2, HEIGHT/2), text=text, fill=(255, 255, 255), font=FONT, anchor="mm", align="center", stroke_width=10, stroke_fill=(0, 0, 0))

        # Save to .png file
        text_image.save(f"media/{output_directory}/{output_directory}_{i}.png")


def generate_video(gameplay_video_file: str | None = None, text_image_directory: str = "generate_text_output", background_audio_file: str | None = None, voice_audio_directory: str = "process_audio_output", output_file: str = "generate_video_output") -> None:
    """
    Combine all audio and video to final output
    """
    
    # Randomly choose gameplay footage if not provided
    if gameplay_video_file is None:
        for _, _, files in os.walk("assets"):
            gameplay_video_files = [file for file in files if file.endswith(".mp4")]
        gameplay_video_file = random.choice(gameplay_video_files)
    
    # Randomly choose background music if not provided
    if background_audio_file is None:
        for _, _, files in os.walk("assets"):
            background_audio_files = [file for file in files if file.endswith(".wav")]
        background_audio_file = random.choice(background_audio_files)

    # Set up clips
    gameplay_video = VideoFileClip(f"assets/{gameplay_video_file}")
    text_images = [ImageClip(f"media/{text_image_directory}/{text_image_directory}_{i}.png") for i in range(sum((len(files) for _, _, files in os.walk(f"media/{text_image_directory}"))))]
    background_audio = AudioFileClip(f"assets/{background_audio_file}")
    voice_audios = [AudioFileClip(f"media/{voice_audio_directory}/{voice_audio_directory}_{i}.wav") for i in range(sum((len(files) for _, _, files in os.walk(f"media/{voice_audio_directory}"))))]

    # Sequence text with voice audio
    for i in range(len(text_images)):
        text_images[i] = text_images[i].set_duration(voice_audios[i].duration).set_audio(voice_audios[i])
    text_with_voice = concatenate_videoclips(text_images)

    # Trim gameplay video to correct length
    video_length = math.ceil(sum(voice_audio.duration for voice_audio in voice_audios))
    start_time = random.randint(0, math.floor(gameplay_video.duration) - video_length)
    gameplay_video = gameplay_video.subclip(start_time, start_time + video_length)

    # Reduce volume of background audio
    background_audio = background_audio.subclip(0, video_length)
    background_audio = background_audio.volumex(0.05)

    # Organise and combine video and audio, save to .mp4 file
    final_video = CompositeVideoClip([gameplay_video, text_with_voice])
    final_audio = CompositeAudioClip([background_audio, text_with_voice.audio])
    final_output = final_video.set_audio(final_audio)
    final_output.write_videofile(f"media/{output_file}.mp4", fps=24)


if __name__ == "__main__":
    generate_text()
    generate_video()