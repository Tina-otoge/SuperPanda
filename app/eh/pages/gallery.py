from datetime import datetime

from app import eh
from app.eh.models.category import Category
from app.eh.models.gallery import Gallery


def get_gallery(id, token):
    soup = eh.get(f"/g/{id}/{token}")
    meta = soup.find(class_="gm")

    if not meta:
        raise Exception("Could not find gallery")

    title = meta.find(id="gn").text
    title_orig = meta.find(id="gj").text
    category = meta.find(id="gdc").text
    category = Category.from_str(category)

    uploader = meta.find(id="gdn").find("a").text
    meta_column = {
        x.find(class_="gdt1").text: x.find(class_="gdt2").text
        for x in meta.find(id="gdd").find_all("tr")
    }
    created_at = meta_column["Posted:"]
    created_at = datetime.fromisoformat(created_at)
    pages_count = meta_column["Length:"].split(" ")[0]
    pages_count = int(pages_count)

    tags = [
        x["href"].split("/")[-1] for x in meta.find(id="taglist").find_all("a")
    ]
    return Gallery(
        id=id,
        token=token,
        title=title,
        title_orig=title_orig,
        category=category,
        uploader=uploader,
        created_at=created_at,
        pages_count=pages_count,
        tags=tags,
    )
