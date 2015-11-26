'''generates thumbnail html for image pages of the current rubric'''

import os

A_IMG = '<a class="thumb" href="{}"><img class="thumb" title="{}" alt="{}" src="{}" /></a>\n'

def image_thumbs(page):
    site = page.site
    rubric = page.rubric

    # find all image pages from the current rubric
    imagepages = []
    for page in rubric.pages:
        if page.type == 'imagepage':
            imagepages.append(page)

    # sort after title, date
    imagepages.sort(key=lambda k: k.title)
    imagepages.sort(key=lambda k: k.date_obj.timestamp())
    imagepages.reverse()

    html = '<div id="thumbs-box">\n'
    # generate thumbs html
    for page in imagepages:

        thumb_title = page.title
        thumb_src = os.path.join('/', page.thumb_src)
        image_href = page.href

        html += A_IMG.format(image_href, thumb_title, thumb_title, thumb_src)

    html += '</div>\n'

    return html
