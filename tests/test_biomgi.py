from biomgi import __version__
import frontmatter

def test_version():
    assert __version__ == '0.1.0'

def test_markdown_format():
    md = frontmatter.load('FORMAT.md')
    print(md.content)
    print(md.metadata)

