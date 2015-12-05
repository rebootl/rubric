'''generate a list of articles of the current rubric'''


import tags

def articles(page):
    site = page.site
    rubric = page.rubric

    # find all the articles
    articles = []
    for page in rubric.pages:
        if page.type == 'article':
            articles.append(page)

    #print("ARTICLES", articles)

    # sort after title, date
    # --> sorting is done in Rubric obj. now
#    try:
#        articles.sort(key=lambda k: k.title)
#    except AttributeError:
#        print("Warning: Bad title, can't properly sort...")
#        pass
#    try:
#        articles.sort(key=lambda k: k.date_obj.timestamp())
#    except AttributeError:
#        print("Warning: Bad date, can't properly sort...")
#        pass
#    articles.reverse()

    articles.reverse()

    ul = '<ul id="article-list">\n'

    for article in articles:

        a = tags.A.format("", article.href, article.variables['title'])

        ul += '<li>{}<br />{}</li>\n'.format(article.variables['date'], a)

    ul += '</ul>\n'

    return ul
