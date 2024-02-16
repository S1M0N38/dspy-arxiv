import chromadb
import json


client = chromadb.HttpClient(host="localhost", port="11435")

client.reset()
collection = client.get_or_create_collection(name="papers")
counter = 1

with open("arxiv-metadata-oai-snapshot.json") as file:
    for line in file:
        paper = json.loads(line.strip())

        # select a subset of field
        id_: str = paper["id"]
        abstract: str = paper["abstract"].strip().replace("\n", " ")
        metadata: dict = {
            "title": paper["title"].strip().replace("\n", " "),
            "doi": paper["doi"] or "",
        }
        collection.add(documents=[abstract], ids=[id_], metadatas=[metadata])
        print(f"\r[{counter:<7} / 2417693]", end="")
        counter += 1
