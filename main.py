import json
from bs4 import BeautifulSoup
from tqdm import tqdm


def main(file_path):
    # parse html
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    bookmarks = []
    for a_tag in soup.find_all("a"):
        title = a_tag.get_text()
        url = a_tag.get("href")
        bookmarks.append((title, url))

    chunk_len = 200
    num_chunks = len(bookmarks) // chunk_len
    pages = []
    for i in tqdm(range(num_chunks + 1)):
        chunk = bookmarks[i * chunk_len : (i + 1) * chunk_len]
        page = {
            "title": f"{bookmark_title}-{i:03}",
            "lines": [
                f"`{elem}`" if not elem.startswith("http") else elem
                for pair in chunk
                for elem in pair
            ],  # title \n url \n title \n url \n ...
        }
        page["lines"].insert(0, page["title"])
        page["lines"].append("")
        pages.append(page)
        # break

    json_data = json.dumps({"pages": pages})
    with open(f"{bookmark_title}.json", "w", encoding="utf-8") as f:
        f.write(json_data)


if __name__ == "__main__":
    # bookmark_title = "debug"
    bookmark_title = "bookmark20230329"
    file_path = "bookmarks_2023_03_29.html"
    main(file_path)
