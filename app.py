from tornado.ncss import Server
from db import *
from template_language.parser import render_template

def index_handler(request):
    cookie = request.get_secure_cookie('user_id')
    if cookie == None:
        request.write(render_template('homepage.html', {}))
    else:
        request.write(render_template('news-feed.html', {'title' : 'News Feed'}))

def login_handler(request):
    method = request.request.method
    if method == 'GET':
        request.write(render_template('login.html', {'location' : '/login'}))
    elif method == 'POST':
        username = request.get_field('username')
        password = request.get_field('password')
        user = User.get(username)
        print("Loggin in: {}".format(user))
        if user is not None and password == user.password:
            request.set_secure_cookie('user_id', str(user.id))
        request.redirect(r'/')

def list_creation_handler(request):
    method = request.request.method
    if method == 'GET':
        request.write(render_template('create.html', {'title' : 'Create A List'}))
        # with open("not_instagram.html") as f:
        #     request.write(f.read())
        #     return
    elif method == 'POST':
        user = User.get_by_id(request.get_secure_cookie('user_id'))
        title = request.get_field('description')
        if user is not None:
            print("HERE")
            l = List(title, user.id)
            l.add()
            print("creating list : {}".format(l))
            request.redirect('/list/{}/'.format(l.id))

def list_display_handler(request, list_id):
    method = request.request.method
    if method == 'GET':
        ls = List.get(int(list_id))
        user = User.get_by_id(ls.uid)
        request.write(render_template('my_bucket_list.html', {'list_title' : ls.title, 'user_name' : user.name, 'list_id' : ls.id}))
    elif method == 'POST':
        # submit checkboxes to database
        pass

def signup_handler(request):
    method = request.request.method
    if method == 'GET':
        request.write(render_template('login.html', {'title' : 'Sign Up'}))
    elif method == 'POST':
        print("running post")
        username = request.get_field('username')
        password = request.get_field('password')
        repeat_password = request.get_field('repeat_password')
        if password == repeat_password:
            user = User.get(username)
            if user is not None:
                raise Exception("User already exists cant add account.")
            user = User(username, password)
            print("creating user : {}".format(user))
            user.add()
            request.set_secure_cookie('user_id', str(user.id))
        request.redirect(r'/')

def logout_handler(request):
    request.clear_cookie('user_id')
    request.redirect(r'/')

# GET /list/create - Call create screen
# POST /list/create - Post list to server and redirects to created list.
# GET /list/<listID> - Shows list referring to listID or says list not found.
# GET / - If not logged in, Shows decription and if you are, shows feed.

server = Server()
server.register(r'/', index_handler)
server.register(r'/login', login_handler)
server.register(r'/list/create', list_creation_handler)
server.register(r'/list/(\d+)/', list_display_handler)
server.register(r'/logout', logout_handler)
server.register(r'/user/create', signup_handler)

server.run()
