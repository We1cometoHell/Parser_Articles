from bs4 import BeautifulSoup
import requests


class Parser:
    def __init__(self, url):
        self.url = url
        try:
            self.response = self.get_response()
            self.soup = self.get_soup()
            self.title = self.get_title()
            self.first_image = self.get_image_article()
            self.text_article = self.get_text_article()
        except AttributeError:
            pass

    def get_response(self):
        response = None

        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            print('Проверьте корректность введенного URL адреса и повторите попытку')

        return response

    def get_soup(self):
        return BeautifulSoup(self.response.text, 'html.parser')

    def get_title(self):
        title = self.soup.find('title')
        if title:
            return title.text
        return 'NotFound'

    def get_image_article(self):
        article = self.soup.find('article')
        if article:
            img = article.find('img')
            return img.get('src')
        return 'NotFound'

    def get_text_article(self):
        article = self.soup.find('article')
        if article:
            paragraphs = article.find_all('p')
            article_text = '\n'.join([p.text for p in paragraphs if len(p.text) > 35])
            return article_text
        return 'NotFound\n'


if __name__ == '__main__':
    while True:
        url = input('Введите url адрес (или "Стоп" для выхода): ')

        if url.lower() == 'стоп' or url.lower() == 'cnjg':
            break

        parser = Parser(url)
        try:
            print(f'\nЗаголовок сайта: {parser.title}\n')
            print(f'Ссылка на первое изображение в статье: {parser.first_image}\n')
            print(f'Текст статьи:\n\n{parser.text_article}')
        except AttributeError:
            pass

    input('\nНажмите Enter, чтобы закрыть программу')
