from edit_video import generate_audio, process_audio, generate_text, generate_video
from scrape_wiki import open_wiki, get_wiki
from upload_video import upload_instagram, upload_tiktok, upload_youtube


def main():
    while True:
        open_wiki("11", "August", "2023")
        title, article, link = get_wiki()
        article_list = article.split('. ')
        generate_audio(text_list=article_list)
        process_audio()
        generate_text(text_list=article_list)
        generate_video()
        break


if __name__ == "__main__":
    main()