from waitress import serve
import GameManager

game_manager = GameManager()

def application(environ, start_response):
    response_body = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)

    # Adding strings to the response body
    response_body = [
        'The Beggining\n',
        '*' * 30 + '\n',
        response_body,
        '\n' + '*' * 30,
        '\nThe End'
    ]

    # So the content-length is the sum of all string's lengths
    content_length = sum([len(s) for s in response_body])

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(content_length))
    ]

    start_response(status, response_headers)

    print game_manager.gameIdExists("bogus")

    return response_body

serve(application, listen='*:8080')