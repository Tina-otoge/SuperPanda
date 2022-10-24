from datetime import datetime

from app import eh
from app.eh.models.category import Category
from app.eh.models.gallery import Gallery


def get_galleries() -> list[Gallery]:
    soup = eh.get("/")
    table = soup.find("table", class_="itg")
    if not table:
        raise Exception("Could not find gallery table")
    galleries = []
    for row in table:
        content_block = row.find(class_="gl4e")
        if not content_block:
            # Could not find title, probably not a gallery, maybe an ad
            continue
        title = content_block.find(class_="glink").text
        cover_url = row.find(class_="gl1e").find("img")["src"]
        link = row.find(class_="gl1e").find("a")["href"]
        id, token = link.split("/")[4:6]
        id = int(id)

        meta_column = row.find(class_="gl3e").find_all("div", recursive=False)
        category = meta_column[0].text
        category = Category.from_str(category)
        created_at = meta_column[1].text
        created_at = datetime.fromisoformat(created_at)
        uploader = meta_column[3].text
        pages_count = meta_column[4].text.split(" ")[0]
        pages_count = int(pages_count)

        tags_table = row.find(class_="gl4e").find("table")
        tags = (
            [x["title"] for x in tags_table.select("[title]")]
            if tags_table
            else []
        )

        galleries.append(
            Gallery(
                title=title,
                id=id,
                token=token,
                category=category,
                created_at=created_at,
                cover_url=cover_url,
                uploader=uploader,
                pages_count=pages_count,
                tags=tags,
            )
        )
    return galleries
