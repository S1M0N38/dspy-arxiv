import chromadb
import json
import pathlib
from arxiv.taxonomy import definitions

path_root = pathlib.Path(__file__).parent
path_dataset = path_root / "dataset"
path_dataset.mkdir(exist_ok=True)

SELECTED_CATS = {
    cat: meta
    for cat, meta in definitions.CATEGORIES_ACTIVE.items()
    if cat.split(".")[0] in ["cs", "math", "stat"]
    # Reduce the database dimension
}

with open(path_dataset / "categories.json", "w") as f:
    json.dump(SELECTED_CATS, f, indent=4)


# # arxiv.json is generated from the file "arxiv-metadata-oai-snapshot.json"
# # that can be download from kaggle dataset
# # https://www.kaggle.com/datasets/Cornell-University/arxiv
#
# with open(path_dataset / "arxiv.json", "w") as outfile:
#     with open("arxiv-metadata-oai-snapshot.json") as infile:
#         for line in infile:
#             paper = json.loads(line.strip())
#             cats = {cat for cat in paper["categories"].split(" ")}
#             if cats.issubset(SELECTED_CATS):
#                 outfile.write(line)


client = chromadb.HttpClient(host="localhost", port="11435")
# client.reset() # uncomment to reset chromadb. Destructive action!
collection = client.get_or_create_collection(name="papers")

ids, abstracts, metadatas = [], [], []
i = 0


def clean(text: str) -> str:
    return text.strip().replace("\n", " ")


with open(path_dataset / "arxiv.json") as file:
    for line in file:
        paper = json.loads(line.strip())
        ids.append(paper["id"])
        abstracts.append(clean(paper["abstract"]))
        metadatas.append({"title": clean(paper["title"]), "doi": paper["doi"] or ""})
        i += 1

        # total num of line in arxiv.json: `wc -l arxiv.json`
        print(f"\r[{i:>5}/926193]", end="")

        if i % 1000 == 0:
            for id_ in collection.get(ids)["ids"]:
                idx = ids.index(id_)
                del ids[idx]
                del abstracts[idx]
                del metadatas[idx]
            if ids:
                collection.add(ids=ids, documents=abstracts, metadatas=metadatas)
            ids, abstracts, metadatas = [], [], []
