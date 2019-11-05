#!/usr/bin/env python
# -*- coding: utf-8 -*-


from apps import create_app
from werkzeug.middleware.proxy_fix import ProxyFix


app = create_app()


def main():
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()


if __name__ == '__main__':
   main()
