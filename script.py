import markdown
import os
import re
import csv



yourpath = "/path/to/directory"
article_files = []
article_data = []



def create_data_object(files):
    for article_path in files:
        with open(os.path.expanduser(f"{article_path}")) as article:
            opened_article = article.read()
            html_article = markdown.markdown(opened_article)
            article.close()
            html_title = html_article.partition('\n')[0]
            h_title = re.sub('<[^<]+?>', '', html_title)
            title = re.sub(r'[^\w_. -]', '_', h_title)
            links = []
            if html_article.find('href'):
                res = [i.start() for i in re.finditer('href', html_article)]
                for i in res:
                    link = html_article[i:].partition('href=')[2].partition('>')[0]
                    link_text = html_article[i:].partition('>')[2].partition('<')[0]
                    links.append(f'{link_text}:{link}')
            data = {
                'directory': article_path.split('/')[5:6],
                'article_title': title,
                'links': links
            }
            print(data)


def get_paths(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith(".md"):
                file_path = os.path.join(root, name)
                article_files.append(file_path)
    create_data_object(article_files)


get_paths(yourpath)
