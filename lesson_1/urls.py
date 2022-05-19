from controllers import render

url_map = {
    '': (render, 'main.html'),
    'about': (render, 'about.html'),
    'not_found': (render, 'not_found.html')
}

class UrlDispatcher:
    def __init__(self, url: str, method: str):
        self.url = url.strip('/')
        self.method = method

    def get_page(self):
        if self.url in url_map:
            controller, page = url_map[self.url]
            return controller(page)
        else:
            controller, page = url_map['not_found']
            return controller(page, error=self.url)
