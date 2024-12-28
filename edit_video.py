import math
import os
import random

import soundfile as sf
import stable_whisper
import stable_whisper.alignment
import stable_whisper.audio
import torch
from moviepy import *
from moviepy.video.tools.subtitles import SubtitlesClip
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer


WIDTH = 1080
HEIGHT = 1920
device = "cuda:0" if torch.cuda.is_available() else "cpu"


def generate_voice(prompt: str = "The quick brown fox jumps over the lazy dog. Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
                   description: str = "A female speaker delivers a very expressive and animated speech with a very quick pace and high pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up.",
                   model_checkpoint: str = "parler-tts-mini-v1",
                   output_file: str = "generate_voice_output") -> None:
    """
    Convert string of text to audio through TTS and save to a .wav file
    model_checkpoint: https://huggingface.co/collections/parler-tts/parler-tts-fully-open-source-high-quality-tts-66164ad285ba03e8ffde214c
    """

    model = ParlerTTSForConditionalGeneration.from_pretrained(f"parler-tts/{model_checkpoint}").to(device)
    tokenizer = AutoTokenizer.from_pretrained(f"parler-tts/{model_checkpoint}")

    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    sf.write(f"media/{output_file}.wav", audio_arr, model.config.sampling_rate)


def generate_subtitles(prompt: str = "The quick brown fox jumps over the lazy dog. Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
                       voice_audio_file: str = "generate_voice_output",
                       model_name: str = "base",
                       output_file: str = "generate_subtitles_output") -> None:
    """
    name : {'tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large-v1',
    'large-v2', 'large-v3', or 'large'}
    """

    # Transcribe
    model = stable_whisper.load_model(model_name)
    result = stable_whisper.alignment.align(model=model,
                                            audio=f"media/{voice_audio_file}.wav",
                                            text=prompt,
                                            language="en",
                                            suppress_silence=False)
    result.to_srt_vtt(f"media/{output_file}.srt", False, True)

    # Append two empty lines as otherwise moviepy cannot read last line
    with open(f"media/{output_file}.srt", 'a') as file:
        file.write("\n\n")


def generate_video(gameplay_video_file: str | None = None,
                   background_audio_file: str | None = None,
                   font_file: str | None = None,
                   voice_audio_file: str = "generate_voice_output",
                   subtitles_file: str = "generate_subtitles_output",
                   output_file: str = "generate_video_output") -> None:
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

    # Randomly choose OpenType font if not provided
    if font_file is None:
        for _, _, files in os.walk("assets"):
            font_files = [file for file in files if file.endswith(".otf") or file.endswith(".ttf")]
        font_file = random.choice(font_files)

    # Set up clips
    gameplay_video = VideoFileClip(f"assets/{gameplay_video_file}")
    background_audio = AudioFileClip(f"assets/{background_audio_file}")
    voice_audio = AudioFileClip(f"media/{voice_audio_file}.wav")
    subtitles = SubtitlesClip(subtitles=f"media/{subtitles_file}.srt", make_textclip=lambda txt: TextClip(font=f"assets/{font_file}",
                                                                                                          text=txt,
                                                                                                          font_size=150,
                                                                                                          size=(None, 190),
                                                                                                          color='white',
                                                                                                          bg_color="black",
                                                                                                          text_align="center"))

    # Trim gameplay video to correct length
    video_length = math.ceil(voice_audio.duration)
    start_time = random.randint(0, math.floor(gameplay_video.duration) - video_length)
    gameplay_video = gameplay_video.subclipped(start_time, start_time + video_length)

    # Reduce volume of background audio
    background_audio = background_audio.subclipped(0, video_length)
    background_audio = background_audio.with_volume_scaled(0.2)

    # Organise and combine video and audio, save to .mp4 file
    final_video = CompositeVideoClip([gameplay_video, subtitles.with_position(("center", "center"))])
    final_audio = CompositeAudioClip([background_audio, voice_audio])
    final_output = final_video.with_audio(final_audio)
    final_output.write_videofile(f"media/{output_file}.mp4", fps=24)


if __name__ == "__main__":
    generate_voice()
    generate_subtitles()
    generate_video()