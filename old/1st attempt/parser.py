from ebooklib import epub
from bs4 import BeautifulSoup
import ebooklib

def extract_text(filepath):
    book = epub.read_epub(filepath)
    text_content = ""
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        text_content += soup.get_text() + " "
    return text_content