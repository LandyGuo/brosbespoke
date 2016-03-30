import django
 
def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    body=['django version: {0} \n'.format(django.get_version())]
    return body
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)