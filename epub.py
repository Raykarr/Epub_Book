import streamlit as st
import ebooklib
from ebooklib import epub
from PIL import Image
import io
import markdown
import uuid
from datetime import datetime
from collections import OrderedDict

# Initialize session state variables
if 'chapters' not in st.session_state:
    st.session_state.chapters = OrderedDict({"Chapter 1": ""})

if 'metadata' not in st.session_state:
    st.session_state.metadata = {
        "description": "",
        "publisher": "Self Published",
        "publication_date": datetime.now().strftime("%Y-%m-%d"),
        "rights": "All rights reserved"
    }

# Helper functions
def get_chapter_num(chapter_title):
    try:
        return int(chapter_title.split()[1])
    except:
        return float('inf')

def add_chapter():
    chapter_numbers = [get_chapter_num(title) for title in st.session_state.chapters.keys()]
    next_number = max(chapter_numbers) + 1 if chapter_numbers else 1

    new_chapters = OrderedDict()
    existing_chapters = sorted(st.session_state.chapters.items(), key=lambda x: get_chapter_num(x[0]))

    for title, content in existing_chapters:
        new_chapters[title] = content

    new_chapters[f"Chapter {next_number}"] = ""
    st.session_state.chapters = new_chapters

def remove_chapter(chapter_title):
    if chapter_title in st.session_state.chapters:
        new_chapters = OrderedDict()
        for title, content in st.session_state.chapters.items():
            if title != chapter_title:
                new_chapters[title] = content
        st.session_state.chapters = new_chapters

def update_chapter_content(chapter_title, new_content):
    if chapter_title in st.session_state.chapters:
        st.session_state.chapters[chapter_title] = new_content

def update_chapter_title(old_title, new_title):
    if old_title in st.session_state.chapters and old_title != new_title:
        content = st.session_state.chapters[old_title]
        new_chapters = OrderedDict()
        for title, chapter_content in st.session_state.chapters.items():
            if title == old_title:
                new_chapters[new_title] = content
            else:
                new_chapters[title] = chapter_content
        st.session_state.chapters = new_chapters

def convert_markdown_to_html(markdown_text):
    return markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'footnotes'])

def create_epub(title, author, cover_image, chapters_content, metadata):
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)
    book.add_metadata('DC', 'description', metadata['description'])
    book.add_metadata('DC', 'publisher', metadata['publisher'])
    book.add_metadata('DC', 'date', metadata['publication_date'])
    book.add_metadata('DC', 'rights', metadata['rights'])

    # Handle cover image
    cover_page = None
    if cover_image is not None:
        cover_image_bytes = io.BytesIO()
        cover_image.save(cover_image_bytes, format='PNG')
        cover_image_bytes = cover_image_bytes.getvalue()

        cover_item = epub.EpubItem(
            uid='cover_image',
            file_name='images/cover.png',
            media_type='image/png',
            content=cover_image_bytes
        )
        book.add_item(cover_item)

        # Create cover page
        cover_page = epub.EpubHtml(title='Cover', file_name='cover.xhtml')
        cover_page.content = f'''<html><body><div style="text-align: center; padding: 0; margin: 0;">
            <img src="images/cover.png" alt="cover"/></div></body></html>'''
        book.add_item(cover_page)
        
        # Set the cover page as the book's cover
        book.set_cover("images/cover.png", cover_image_bytes)

    # Create table of contents page
    toc_page = epub.EpubHtml(title='Table of Contents', file_name='toc.xhtml')
    toc_content = ['<h1>Table of Contents</h1>', '<nav>', '<ol>']
    
    for chapter_title in chapters_content.keys():
        toc_content.append(f'<li><a href="#{chapter_title}">{chapter_title}</a></li>')
    
    toc_content.extend(['</ol>', '</nav>'])
    toc_page.content = '\n'.join(toc_content)
    book.add_item(toc_page)

    # Create chapters
    chapter_objects = []
    for idx, (chapter_title, chapter_content) in enumerate(chapters_content.items(), 1):
        html_content = convert_markdown_to_html(chapter_content)
        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=f'chapter_{idx}.xhtml',
            content=f'<h1 id="{chapter_title}">{chapter_title}</h1>\n{html_content}'
        )
        book.add_item(chapter)
        chapter_objects.append(chapter)

    # Add navigation
    book.toc = chapter_objects
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Add CSS
    style = '''
        body { font-family: "Crimson Text", Georgia, serif; line-height: 1.6; margin: 2em; }
        h1, h2, h3 { color: #2c3e50; margin-top: 1.5em; }
        p { text-align: justify; margin-bottom: 1em; }
        img { max-width: 100%; display: block; margin: 1em auto; }
        nav { margin: 2em 0; }
        nav ol { list-style-type: none; padding-left: 0; }
        nav ol li { margin-bottom: 0.5em; }
        nav ol li a { color: #2c3e50; text-decoration: none; }
        nav ol li a:hover { text-decoration: underline; }
    '''
    nav_css = epub.EpubItem(
        uid="style",
        file_name="style/main.css",
        media_type="text/css",
        content=style
    )
    book.add_item(nav_css)

    # Set spine with correct order: cover -> toc -> chapters
    spine = []
    if cover_page:
        spine.append(cover_page)
    spine.append(toc_page)
    spine.extend(chapter_objects)
    book.spine = spine

    return book

def main():
    st.set_page_config(page_title="📚 EPUB Creator", layout="wide")
    st.title("📚 EPUB Creator")

    with st.expander("📋 Book Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title", "My Book")
            author = st.text_input("Author Name")
        with col2:
            st.session_state.metadata["publisher"] = st.text_input("Publisher", value=st.session_state.metadata["publisher"])
            st.session_state.metadata["description"] = st.text_area("Book Description", value=st.session_state.metadata["description"])

    with st.expander("🖼️ Cover Image", expanded=True):
        cover_image = st.file_uploader("Upload cover image (PNG/JPG)", type=['png', 'jpg', 'jpeg'])
        if cover_image:
            st.image(cover_image, width=300)

    with st.expander("📝 Chapters", expanded=True):
        st.button("➕ Add New Chapter", on_click=add_chapter)
        for chapter_title in st.session_state.chapters.keys():
            st.subheader(chapter_title)
            new_title = st.text_input("Title", value=chapter_title, key=f"title_{chapter_title}")
            if new_title != chapter_title:
                update_chapter_title(chapter_title, new_title)
                st.rerun()

            content = st.text_area(
         "Content (Markdown supported)",
            value=st.session_state.chapters[chapter_title],
          height=200,
          key=f"content_{chapter_title}"
            )

        # Update content if changed
        if content != st.session_state.chapters[chapter_title]:
         update_chapter_content(chapter_title, content)

        if len(st.session_state.chapters) > 1:
         st.button("🗑️ Remove Chapter", key=f"remove_{chapter_title}", on_click=remove_chapter, args=(chapter_title,))
        st.markdown("---")

    with st.expander("👁️ Preview", expanded=True):
        if st.session_state.chapters:
            chapter_select = st.selectbox("Select chapter to preview", options=list(st.session_state.chapters.keys()))
            st.markdown("### Preview")
            st.markdown(st.session_state.chapters[chapter_select])

    if st.button("📚 Generate EPUB", type="primary"):
        if not title or not author:
            st.error("Please provide both title and author name!")
            return

        if not any(st.session_state.chapters.values()):
            st.error("Please add some content to at least one chapter!")
            return

        try:
            cover_img = Image.open(cover_image) if cover_image else None
            book = create_epub(title, author, cover_img, st.session_state.chapters, st.session_state.metadata)

            epub_bytes = io.BytesIO()
            epub.write_epub(epub_bytes, book)

            st.download_button("📥 Download EPUB", data=epub_bytes.getvalue(), file_name=f"{title.lower().replace(' ', '_')}.epub", mime="application/epub+zip")
            st.success("✅ EPUB generated successfully!")

        except Exception as e:
            st.error(f"Error generating EPUB: {str(e)}")

if __name__ == "__main__":
    main()
