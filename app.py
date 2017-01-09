from tornado.ncss import Server

def index_handler(request):
    request.write('<strong>Hello</strong> World')

def login(request):
    method = request.request.method
    if method == 'GET':
        with open("not_instagram.html") as f:
            request.write(f.read())
            return
    elif method == 'POST':
        username = request.get_field('username')
        password = request.get_field('password')
        request.redirect(r'/')




# GET /list/create - Call create screen
# POST /list/create - Post list to server and redirects to created list.
# GET /list/<listID> - Shows list referring to listID or says list not found.
# GET / - If not logged in, Shows decription and if you are, shows feed.

server = Server()
server.register(r'/', index_handler)
server.register(r'/login', login)

server.run()
