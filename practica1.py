#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp


class shortUrlSrv(webapp.webApp):

    def __init__(self, hostname, port):
        self.name = hostname
        self.port = str(port)
        self.longShortUrls = {}
        self.shortLongUrls = {}
        self.shortUrl = 0
        webapp.webApp.__init__(self, hostname, port)

    def parse(self, request):
        method = request.split(" ")[0]
        resource = request.split(" ")[1]
        if method == "POST":
            body = request.split("\r\n\r\n")[-1]
        else:
            body = ""
        return (method, resource, body)

    def processGet(self, resource):
        form = "<form action='' method='POST'>URL a acortar: <input type=\
                'text' name='url'><input type='submit' value='Enviar'></form>"
        if resource == "/":
            code = "200 OK"
            html = "<html><body>"
            for url in self.longShortUrls:
                html += "<p><pre>" + url + "\t" + str(self.longShortUrls[url])\
                        + "</pre></p>"
            html += form + "</body></html>"
        elif resource[1:] in self.shortLongUrls:
            url = self.shortLongUrls[resource[1:]]
            print "REDIRECTING TO:", url
            code = "300 Redirect"
            html = "<html><body><meta http-equiv='refresh' content='0; \
                    URL=" + url + "'></body></html>"
        else:
            code = "404 Not Found"
            html = "<html><body><h1>Recurso no disponible</h1></body></html>"
        return code, html

    def processPost(self, resource, body):
        url = body.split("=")[1]
        if url == "":
            code = "400 Error"
            html = "<html><body><h1>Error: empty POST</h1></body></html>"
            return code, html
        if url.startswith("http%3A%2F%2F"):
            url = "http://" + url[13:]
        elif url.startswith("https%3A%2F%2F"):
            url = "https://" + url[14:]
        else:
            url = "http://" + url
        print "URL:", url
        if url in self.longShortUrls:
            shortUrl = self.longShortUrls[url]
        else:
            shortUrl = "http://" + self.name + ":" + self.port + "/" + \
                        str(self.shortUrl)
            self.longShortUrls[url] = shortUrl
            self.shortLongUrls[str(self.shortUrl)] = url
            self.shortUrl += 1
        code = "200 OK"
        html = "<html><body><p>url real: <a href=" + url + ">" + url + \
                "</a></p>url acortada: <a href=" + shortUrl + ">" + shortUrl +\
                "</a></body></html>"
        return code, html

    def process(self, request):
        method, resource, body = request
        if method == "GET":
            (code, html) = self.processGet(resource)
        elif method == "POST":
            (code, html) = self.processPost(resource, body)
        else:
            code = "400 Error"
            html = "<html><body><h1>Wrong method</h1></body></html>"
        return code, html

if __name__ == "__main__":
    try:
        shortenerSrv = shortUrlSrv("localhost", 9999)
    except KeyboardInterrupt:
        print "KeyboardInterrupt detected"
    except TypeError:
        print "host name[string]  port[int]"
