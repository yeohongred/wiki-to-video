from edit_video import generate_audio, process_audio, generate_video
from scrape_wiki import open_wiki, get_wiki


def main():
    open_wiki("10", "August", "2023")
    title, article, link = get_wiki()
    generate_audio()
    process_audio()
    generate_video()


if __name__ == "__main__":
    main()