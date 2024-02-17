import random
import json
import pathlib
from arxiv2text import arxiv_to_text


random.seed(0)
path_root = pathlib.Path(__file__).parent
path_database = path_root / "database"
path_dataset = path_root / "dataset"
path_dataset.mkdir(exist_ok=True)


def random_sample(num: int, tot: int = 926193) -> set[int]:
    """
    Randomly samples a specified number of paper indices from a larger pool.

    Args:
        num: The number of paper indices to sample.
        tot: The total number of papers in the pool (defaults to num of lines in arxiv.json).

    Returns:
        A set containing the randomly selected paper indices.
        These are the lines in the  arxiv kaggle dump.
    """
    lines = set()
    while len(lines) < num:
        line = random.randint(0, tot - 1)
        if line not in lines:
            lines.add(line)
    return lines


lines = random_sample(10)
i = 0

with open(path_database / "arxiv.json") as file:
    for line_num, line in enumerate(file):
        if line_num in lines:
            i += 1
            paper = json.loads(line.strip())
            path_paper = path_dataset / f'{paper["id"].replace("/", "-")}.json'
            if not path_paper.exists():
                print(f"[{i:>3}/{len(lines)}] Processing {path_paper.stem}")
                url = f"https://arxiv.org/pdf/{paper['id']}.pdf"
                paper["text"] = arxiv_to_text(url)
                with open(path_paper, "w") as outfile:
                    json.dump(paper, outfile, indent=4)
