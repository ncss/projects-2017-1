from tornado.ncss import Server
from db import *
from template_language.parser import render_template

def index_handler(request):
    cookie = request.get_secure_cookie('user_id')
    if cookie == None:
        request.write('Welcome to our site!')
    else:
        request.write('This is the news feed!')

def login(request):
    method = request.request.method
    if method == 'GET':
        request.write(render_template('not_instagram.html', {'location' : '/login'}))
    elif method == 'POST':
        username = request.get_field('username')
        password = request.get_field('password')
        user = User.get(username)
        print("Loggin in: {}".format(user))
        if user is not None and password == user.password:
            request.set_secure_cookie('user_id', str(user.id))
        request.redirect(r'/')

def create(request):
    method = request.request.method
    if method == 'GET':
        request.write(render_template('not_instagram.html', {'location' : '/list/create'}))
        # with open("not_instagram.html") as f:
        #     request.write(f.read())
        #     return
    elif method == 'POST':
        username = request.get_field('username')
        title = request.get_field('password')
        user = User.get(username)
        if user is not None:
            l = List(title, user.id)
            l.add()
            print("creating list : {}".format(l))
            request.redirect('/list/{}/'.format(l.id))

def list_handler(request, list_id):
    method = request.request.method
    if method == 'GET':
        request.write(str(List.get(int(list_id))))
        # request.write(render_template('not_instagram.html', {'location' : '/list/{}/'.format(list_id)}))
    elif method == 'POST':
        # submit checkboxes to database
        pass

def signup_handler(request):
    method = request.request.method
    if method == 'GET':
        request.write(render_template('not_instagram.html', {'location' : '/user/create'}))
    elif method == 'POST':
        print("running post")
        username = request.get_field('username')
        password = request.get_field('password')
        repeat_password = request.get_field('repeat_password')
        user = User.get(username)
        if user is not None:
            raise Exception("User already exists cant add account.")
        user = User(username, password)
        print("creating user : {}".format(user))
        user.add()
        request.set_secure_cookie('user_id', str(user.id))
        request.redirect(r'/')

def logout(request):
    request.clear_cookie('user_id')
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
