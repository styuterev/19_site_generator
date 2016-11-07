import jinja2
import json
import markdown
import os
import string


def render_template(template, context=None, template_folder='templates'):
    if not os.path.exists(os.path.join(template_folder, template)):
        return None
    if context is None:
        context = {}
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_folder))
    environment.globals['load_article'] = load_article
    environment.globals['generate_id'] = generate_id
    return environment.get_template(template).render(context)


def read_config(config_file='config.json'):
    if not os.path.exists(config_file):
        return None
    with open(config_file) as json_file:
        data = json.load(json_file)
    return data


def reorganize_data(data):
    topics, articles = {}, {}
    for topic in data['topics']:
        articles[topic['slug']] = []
        topics[topic['slug']] = topic['title']
    for article in data['articles']:
        if article['topic'] in articles:
            articles[article['topic']].append(article)
    return topics, articles


def load_article(filepath):
    articles_folder = 'articles'
    article_filepath = os.path.join(articles_folder, filepath)
    if not os.path.exists(article_filepath):
        return None
    with open(article_filepath) as article_file:
        markdown_text = article_file.read()
        html_text = markdown.markdown(markdown_text)
    return html_text


def generate_id(id_class, string_id):
    unsuitable_symbols = string.punctuation + ' '
    for symbol in unsuitable_symbols:
        string_id = string_id.replace(symbol, '_')
    return 'id_{}_{}'.format(id_class, string_id)


# TODO: Move CSS and JS to separate files

if __name__ == '__main__':
    data = read_config()
    topics, articles = reorganize_data(data)
    context = {
        'articles': articles,
        'topics': topics
    }
    print(topics)
    print(articles)
    result = render_template('index.html', context)
    with open('test.html', 'w') as export_file:
        #print(result)
        export_file.write(result)
        export_file.close()