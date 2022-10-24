from app import eh
from app.eh.models.preview import Preview


def get_previews(id, token):
    soup = eh.get(f"/g/{id}/{token}")
    previews = {}
    for div in soup.find(id="gdt").find_all(class_="gdtm"):
        inner_div = div.find("div")
        link = inner_div.find("a")["href"]
        page = link.split("-")[-1]
        page = int(page)
        page_token = link.split("/")[-2]
        # unsafe object, splitting on : also splits on https://
        styles = {
            x.split(":")[0].strip(): x.split(":")[1].strip()
            for x in inner_div["style"].split(";")
        }
        width = styles["width"].replace("px", "")
        width = int(width)
        height = styles["height"].replace("px", "")
        height = int(height)
        url, offset_x = inner_div["style"].split(" ")[-4:-2]
        url = url[4:-1]
        offset_x = offset_x.replace("px", "")
        offset_x = int(offset_x)
        previews[page] = Preview(
            url=url,
            width=width,
            height=height,
            offset_x=offset_x,
            page=page,
            page_token=page_token,
        )
    return previews
