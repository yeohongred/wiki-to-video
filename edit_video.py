import math
import os
import random

import pyttsx3
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile
from moviepy.editor import *


# 0 is male voice, 1 is female voice (for my computer)
def generate_audio(voice=0, text="The quick brown fox jumps over the lazy dog.", output_file="generate_audio_output.wav"):
    engine = pyttsx3.init()

    # Setting desired voice
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voice].id)

    # Creating file
    os.makedirs("media", exist_ok=True)
    engine.save_to_file(text, f"media/{output_file}")
    engine.runAndWait()


# might need to add normalisation
def process_audio(input_file="generate_audio_output.wav", output_file="process_audio_output.wav"):
    board = Pedalboard([Reverb(room_size=0.4, damping=1, wet_level=0.2, dry_level=0.3)])

    with AudioFile(f"media/{input_file}") as input_audio:
        with AudioFile(f"media/{output_file}", 'w', input_audio.samplerate, input_audio.num_channels) as output_audio:
            while input_audio.tell() < input_audio.frames:
                chunk = input_audio.read(input_audio.samplerate)
                effected = board(chunk, input_audio.samplerate, reset=False)
                output_audio.write(effected)


def generate_video(gameplay_video_file="minecraft.mp4", background_audio_file="the_begin.wav", voice_audio_file="process_audio_output.wav", output_file="generate_video_output.mp4"):
    gameplay_video = VideoFileClip(f"assets/{gameplay_video_file}")
    background_audio = AudioFileClip(f"assets/{background_audio_file}")
    voice_audio = AudioFileClip(f"media/{voice_audio_file}")

    video_length = math.ceil(voice_audio.duration)
    start_time = random.randint(0, math.floor(gameplay_video.duration) - video_length)
    gameplay_video = gameplay_video.subclip(start_time, start_time + video_length)

    background_audio = background_audio.subclip(0, video_length)

    final_video = gameplay_video
    final_audio = CompositeAudioClip([background_audio, voice_audio])

    final_output = final_video.set_audio(final_audio)
    os.makedirs("media", exist_ok=True)
    final_output.write_videofile(f"media/{output_file}", fps=60)


if __name__ == "__main__":
    generate_audio()
    process_audio()
    generate_video()