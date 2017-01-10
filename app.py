from tornado.ncss import Server

def index_handler(request):
    cookie = request.get_secure_cookie('user_id')
    if cookie == None:
        request.write('Welcome to our site!')
    else:
        request.write('This is the news feed!')

def login(request):
    method = request.request.method
    if method == 'GET':
        with open("not_instagram.html") as f:
            request.write(f.read())
            return
    elif method == 'POST':
        username = request.get_field('username')
        password = request.get_field('password')
        #user = db.get(username)
        #if user is not None
        if username == 'meme' and password == '123': #user.password:
            request.set_secure_cookie('user_id', '1') #user.id)
        request.redirect(r'/')

def create(request):
    method = request.request.method
    if method == 'GET':
        with open("not_instagram.html") as f:
            request.write(f.read())
            return
    elif method == 'POST':
        # To Do: When we know what the html form data will be, extract in here.
        pass

def list_handler(request, list_id):
    method = request.request.method
    if method == 'GET':
        with open("not_instagram.html") as f:
            request.write(f.read())
            return
    elif method == 'POST':
        # submit checkboxes to database
        pass

def logout(request):
    request.clear_cookie('user_id')
    request.redirect(r'/')

def signup_handler(request):
    method = request.request.method
    if method == 'GET':
        with open("not_instagram.html") as f:
            request.write(f.read())
            return
    elif method == 'POST':
        username = request.get_field('username')
        password = request.get_field('password')
        repeat_password = request.get_field('repeat_password')
        #To do, here is where we put the database
        #user = db.get(username)
        #if user is not None
        #user.password:
        user_id = '1'
        request.set_secure_cookie('user_id', user_id) #user.id)
        request.redirect(r'/')


# GET /list/create - Call create screen
# POST /list/create - Post list to server and redirects to created list.
# GET /list/<listID> - Shows list referring to listID or says list not found.
# GET / - If not logged in, Shows decription and if you are, shows feed.

server = Server()
server.register(r'/', index_handler)
server.register(r'/login', login)
server.register(r'/list/create', create)
server.register(r'/list/(\d+)/', list_handler)
server.register(r'/logout', logout)
server.register(r'/user/create', signup_handler)

server.run()
