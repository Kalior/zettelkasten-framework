from pathlib import Path

items = [p for p in Path(".").iterdir() if p.suffix == ".md" and p.stem != "README"]

out_dir = Path() / "graph" / "src" / "notes"
out_dir.mkdir(exist_ok=True, parents=True)

def fix_link(link: str) -> str:
    splits = link.split(".")
    if len(splits) == 2:
        return link.replace(".md", "")
    elif link[0:4] == "http":
        return link
    else:
        return link

def convert(path: Path):
    with path.open("r") as f:
        lines = list(f.readlines())
    
    title = lines[0].replace("# ", "").replace("\n", "")
    header = title.split(" ")[1].replace("-", " ")
    uid = title.replace(" ", "-")

    categories = [c.replace("#", "") for c in lines[1].replace("\n", "").split(" ") if c != ""]
    
    main_content = "\n".join([line.replace("\n", "") for line in lines if line[0] not in ['#', '-']])
    links = [line.replace("[[", "").replace("]]", "").replace("- ", "").replace("\n", "") for line in lines if line[0] == '-']
    links = list(set(fix_link(link).strip() for link in links))

    date = title.split(" ")[0]


    return (
    "---\n"
    f'title: {header}\n'
    f'categories: {categories}\n'
    f'links: {links}\n'
    f'date: {date}\n'
    f'uid: "{uid}"\n'
    "---\n"
    f'{main_content}\n'
    )

outs = [convert(p) for p in items]

for out, p in zip(outs, items):
    out_f = out_dir / p

    with out_f.open("w") as f:
        f.write(out)
