import time
from datetime import datetime

import pyttsx3
from moviepy.editor import *

from edit_video import generate_audio, process_audio, generate_video
from scrape_wiki import open_wiki, get_wiki, close_wiki


def main():
    open_wiki("10", "August", "2023")
    title, article, link = get_wiki()
    close_wiki()
    generate_audio(voice=1, text=article, output_file="article.wav")
    process_audio(input_file="article.wav")


if __name__ == "__main__":
    main()