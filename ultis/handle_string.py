def get_file_name(url) -> str:
    return url.split("/")[-1]

def is_valid_question_url(url):
    return 'question/' in url and 'page=' not in url
    