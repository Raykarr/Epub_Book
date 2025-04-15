# 📚 EPUB Creator

## Overview
EPUB Creator is a user-friendly Streamlit application that allows you to easily create professional EPUB ebooks with a clean, intuitive interface. Write your book chapter by chapter, add metadata, upload a cover image, and generate a polished EPUB file ready for distribution.

## 🌟 Features

### Book Creation
- Add and manage multiple chapters
- Write chapters using Markdown
- Dynamically rename and remove chapters
- Preview chapter content

### Metadata Management
- Set book title and author
- Add publisher information
- Include book description
- Specify publication date and rights

### Cover Image
- Upload a custom cover image (PNG/JPG)
- Automatic image integration into EPUB

### Styling
- Professional ebook formatting
- Responsive typography
- Clean, readable layout
- Table of contents generation

## 🛠 Requirements
- Python 3.7+
- Streamlit
- ebooklib
- Pillow (PIL)
- markdown
- uuid

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Epub_Book.git
cd epub-creator
```

2. Install required dependencies:
```bash
pip install streamlit ebooklib Pillow markdown
```

## 🚀 Usage

Run the Streamlit application:
```bash
streamlit run epub.py
```

### Step-by-Step Guide
1. Enter book details (title, author, etc.)
2. Upload a cover image (optional)
3. Add chapters and write content in Markdown
4. Preview chapters
5. Click "Generate EPUB" to create your ebook

## 📝 Markdown Support
The application supports:
- Headings
- Paragraphs
- Tables
- Code blocks
- Footnotes

## 🎨 Customization
- Modify CSS in `create_epub()` function to change ebook styling
- Adjust metadata fields as needed

## 🔍 Technical Details
- Uses `ebooklib` for EPUB generation
- Converts Markdown to HTML
- Generates a professionally formatted ebook
- Supports multiple chapters
- Handles cover images and metadata

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🌈 Future Improvements
- Export to other formats (PDF, MOBI)
- Advanced styling options
- Collaborative writing features
- Integration with cloud storage
