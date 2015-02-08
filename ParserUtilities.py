import BeautifulSoup


def get_text_content(soupnode, strip=True):
    if len(soupnode) > 1 and type(soupnode) is not BeautifulSoup.NavigableString:
        contents = ''.join([get_text_content(child) for child in soupnode])
    else:
        if type(soupnode) == BeautifulSoup.Tag:
            contents = ''.join([get_text_content(content) for content in soupnode.contents])
        else:
            contents = soupnode

    if strip:
        return contents.replace('&nbsp;', ' ').strip()
    else:
        return contents