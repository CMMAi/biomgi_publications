#%%
import os
from pathlib import Path
from typing import Dict
from itertools import groupby
from argparse import ArgumentParser
import frontmatter
import bibtexparser
from bibtexparser.bparser import BibTexParser
from mdutils import MdUtils

parser = ArgumentParser()
parser.add_argument('--bibtex', '--bib', '-b', help='path to bibtex')
parser.add_argument('--format', '-f', help='FORMAT.md')
parser.add_argument('--output', '-o', default='./')
args = parser.parse_args()

BIBTEX_PATH = args.bibtex
FORMAT_PATH = args.format
OUTPUT_PATH = Path(args.output).resolve()

# %%
parser = BibTexParser(common_strings=True)
with open(BIBTEX_PATH) as bibtex_file:
  bib_database = bibtexparser.load(bibtex_file, parser=parser)
# %%
md = frontmatter.load(FORMAT_PATH)
FORMAT = md.content
GROUPBY = md.metadata.get('groupBy')
SORTBY = md.metadata.get('sortBy')
# %%
entries = bib_database.entries
entries.sort(key=lambda x: x.get(GROUPBY, ''))
#%%
md_file = MdUtils(file_name=OUTPUT_PATH.stem, title=OUTPUT_PATH.stem)
# %%
def format_entry(md_file: MdUtils, entry: Dict):
  assert entry.get('title')
  formatted = FORMAT.format(
    TITLE=entry.get('title'), 
    AUTHOR=entry.get('author', '').replace(' and', ','),
    YEAR=entry.get('year', ''),
    JOURNAL=entry.get('journal', ''))
  md_file.new_line(formatted)
#%%
for key, group in groupby(entries, lambda x: x.get(GROUPBY, '')):
  md_file.new_header(level=1, title=f'{key}')
  for entry in sorted(group, key=lambda x: x.get(SORTBY, '')):
    format_entry(md_file=md_file, entry=entry)

# %%
md_file.create_md_file()
# %%
os.rename(f'./{OUTPUT_PATH.stem}.md', OUTPUT_PATH)