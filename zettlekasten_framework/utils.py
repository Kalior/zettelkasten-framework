import dataclasses
from pathlib import Path
import textwrap

from dash import dcc, html


@dataclasses.dataclass
class Note:
    header: str
    uid: str
    date: str
    categories: list[str]
    content: str
    links: list[str]

    @property
    def excerpt(self) -> str:
        return textwrap.shorten(self.content,  width=70, placeholder="...")


def get_markdown_pages():
    root_dir = Path(".")

    md_pages = [p for p in root_dir.iterdir() if p.suffix == ".md" and p.stem != "README"]

    return md_pages


def path_to_markdown_element(p: Path):
    with p.open("r") as f:
        contents = f.read()

    return dcc.Markdown(contents, mathjax=True)


def fix_link(link: str) -> str:
    splits = link.split(".")
    if len(splits) == 2:
        return link.replace(".md", "")
    elif link[0:4] == "http":
        return link
    else:
        return link


def read_path_to_note(path: Path) -> Note:
    with path.open("r") as f:
        lines = list(f.readlines())

    title = lines[0].replace("# ", "").replace("\n", "")
    print(title)
    header = title.split(" ")[1].replace("-", " ")
    uid = title.replace(" ", "-")

    categories = [c.replace("#", "") for c in lines[1].replace("\n", "").split(" ") if c != ""]

    main_content = "\n".join([line.replace("\n", "") for line in lines if line[0] not in ['#', '-']])
    links = [line.replace("[[", "").replace("]]", "").replace("- ", "").replace("\n", "") for line in lines if
             line[0] == '-']
    links = list(set(fix_link(link).strip() for link in links))

    date = title.split(" ")[0]

    return Note(
        header=header, uid=uid, date=date, categories=categories, content=main_content, links=links
    )

