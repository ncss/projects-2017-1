from tornado.ncss import Server
from db import *
import os
from template_language.parser import render_template

def is_authorised(request):
    cookie = request.get_secure_cookie('user_id')
    if not cookie:
        return False
    user = User.get_by_id(int(cookie))
    if not user:
        return False
    return True

def index_handler(request):
    cookie = request.get_secure_cookie('user_id')
    if cookie == None:
        request.write(render_template('homepage.html', {'is_user' : is_authorised(request), 'title' : "Home Page"}))
    else:
        user = User.get_by_id(int(cookie))
        ls = List.get_user_lists(user)
        print(ls)
        names = user.get_newsfeed()
        names = [user.get_by_id(a.userid).name for a in names]
        request.write(render_template('news-feed.html', {'list_id': ls[0].id, 'user_id': user.id, 'names':names, 'is_user' : is_authorised(request), 'title' : 'News Feed', 'user' : user.name}))


def login_handler(request):
    method = request.request.method
    if is_authorised(request):
        request.redirect(r'/')
        return

    if method == 'GET':
        request.write(render_template('login.html', {'is_user' : is_authorised(request), 'location' : '/login', 'title' : "Login" }))
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
    if not is_authorised(request):
        request.redirect(r'/login')
        return

    user = User.get_by_id(int(request.get_secure_cookie('user_id')))

    if method == 'GET':
        request.write(render_template('create.html', {'user' : user.name, 'is_user' : is_authorised(request), 'title' : 'Create A List'}))
        # with open("not_instagram.html") as f:
        #     request.write(f.read())
        #     return
    elif method == 'POST':
        textdesc = request.get_field('description')
        ##Get the User
        user = User.get_by_id(int(request.get_secure_cookie('user_id')))
        #Get a new Item object
        ls = List.get_user_lists(user)
        if ls:
            item = Item(ls[0].id, text=textdesc)
            item.add()
            head, contype, body = request.get_file('file_upload')
            if head != '':
                item.image = head
                head = head.split('.')[-1]
                filename = 'static/img/list/{}/item{}.{}'.format(user.name, item.id, head)
                with open(filename, 'wb') as f:
                    f.write(body)
                item.update()
                request.redirect(r'/list/{}/'.format(item.list_id))

def list_display_handler(request, list_id):
    method = request.request.method
    if method == 'GET':
        ls = List.get(int(list_id))
        if ls:
            user = User.get_by_id(ls.userid)
            bucket = [a.id for a in ls.get_items()]
            items = {}
            for item in bucket:
                items[item] = Item.get(item)
            print(items)
            request.write(render_template('my_bucket_list.html', {'bucket' : bucket, 'items':items, 'user' : user.name, 'is_user' : is_authorised(request), 'list_title' : ls.title, 'user_name' : user.name, 'list_id' : ls.id, 'title' : "{}\'s Bucket List\'".format(user.name)}))
        else:
            pass
            # TODO pass list doesnt exist
    elif method == 'POST':
        # submit checkboxes to database
        pass

def signup_handler(request):
    method = request.request.method
    if is_authorised(request):
        request.redirect(r'/')
        return

    if method == 'GET':
        request.write(render_template('signup.html', {'is_user' : is_authorised(request), 'location' : '/user/create', 'title' : "Sign Up" }))
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
            l = List("", user.id)
            l.add()
            try:
                os.makedirs('static/img/list/{}'.format(user.name))
            except:
                print("Folder is already there stop being such a tryhard!")
            request.set_secure_cookie('user_id', str(user.id))
        request.redirect(r'/')

def logout_handler(request):
    if not is_authorised(request):
        request.redirect(r'/')
        return

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
server.register(r'/list/(\d+)', list_display_handler)
server.register(r'/logout', logout_handler)
server.register(r'/user/create', signup_handler)

server.run()
