import PyPDF2
from ebooklib import epub
from ebooklib.utils import debug

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        # Initialize an empty list to store the text for each page
        pages_text = []

        # Loop through each page
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()

            # Append the text to the list
            pages_text.append(text)

    return pages_text

def create_epub(pages_text, output_path):
    # Create a new EPUB book
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('id123456')
    book.set_title('Extracted Text from PDF')
    book.set_language('en')

    # Add chapters
    chapters = []
    for i, text in enumerate(pages_text):
        text = text.replace('\n', '</p><p>')
        chapter = epub.EpubHtml(title=f'Page {i + 1}', file_name=f'page_{i + 1}.xhtml', lang='en')
        chapter.set_content(f'<h1>Page {i + 1}</h1><p>{text}</p>')
        book.add_item(chapter)
        chapters.append(chapter)

    # Define Table Of Contents
    book.toc = chapters

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = 'BODY { color: white; }'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # Basic spine
    book.spine = ['nav'] + chapters

    # Write the EPUB file
    epub.write_epub(output_path, book, {})

# Example usage
pdf_path = 'C:/Users/rajes/OneDrive/Documents/RPG/DnD5e/Rules/Sword Coast Adventurer Guide.pdf'
output_path = 'c:/temp/dnd-rulebooks/sword-coast-text.epub'

pages_text = extract_text_from_pdf(pdf_path)
create_epub(pages_text, output_path)
