from tornado.ncss import Server
from db import *
import hashlib
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
        names = user.get_newsfeed()
        names = [user.get_by_id(a.userid) for a in names]
        user_list = user.get_lists()[0]
        request.write(render_template('news-feed.html', {'user_id':str(request.get_secure_cookie('user_id'))[2:-1], 'user_id': user.id, 'names':names, 'is_user' : is_authorised(request), 'title' : 'News Feed', 'user' : user.name, 'user_list': user_list.id}))


def login_handler(request):
    method = request.request.method
    if is_authorised(request):
        request.redirect(r'/')
        return

    if method == 'GET':
        request.write(render_template('login.html', {'disp' : False, 'is_user' : is_authorised(request), 'location' : '/login', 'title' : "Login" }))
    elif method == 'POST':
        username = request.get_field('username')
        password = request.get_field('password')
        m = hashlib.sha256()
        password = password.encode()
        m.update(password)
        password = m.hexdigest()
        user = User.get(username)
        if user is not None and password == user.password:
            request.set_secure_cookie('user_id', str(user.id))
            request.redirect(r'/login')
        else:
            request.write(render_template('login.html', {'disp' : True, 'is_user' : is_authorised(request), 'location' : '/login', 'title' : "Login" }))

def list_creation_handler(request):
    method = request.request.method
    if not is_authorised(request):
        request.redirect(r'/login')
        return

    user = User.get_by_id(int(request.get_secure_cookie('user_id')))

    if method == 'GET':
        user_list = user.get_lists()[0]
        request.write(render_template('create.html', {'user_id':str(request.get_secure_cookie('user_id'))[2:-1],  'user' : user.name, 'is_user' : is_authorised(request), 'title' : 'Create A List', 'user_list': user_list.id}))
        # with open("not_instagram.html") as f:
        #     request.write(f.read())
        #     return
    elif method == 'POST':
        textdesc = request.get_field('description')
        ##Get the User
        user = User.get_by_id(int(request.get_secure_cookie('user_id')))
        head, contype, body = request.get_file('file_upload')
        #Get a new Item object
        ls = List.get_user_lists(user)
        if ls and (head or textdesc):
            item = Item(ls[0].id, text=textdesc)
            item.add()
            if head:
                item.image = head
                head = head.split('.')[-1]
                filename = 'static/img/list/{}/item{}.{}'.format(user.name, item.id, head)
                item.image = '/'+filename
                with open(filename, 'wb') as f:
                    f.write(body)
            item.update()
            request.redirect(r'/list/{}'.format(item.list_id))
        else:
            pass
            #TODO handle invalid item input here

def list_display_handler(request, list_id):
    method = request.request.method

    if not is_authorised(request):
        request.redirect(r'/')
        return

    if method == 'GET':
        ls = List.get(int(list_id))
        if ls:
            user = User.get_by_id(ls.userid)
            user_list = user.get_lists()[0]
            user2 = User.get_by_id(int(request.get_secure_cookie('user_id')))
            bucket = [a.id for a in ls.get_items()]
            comments = Comment.get_comments_for_list(int(list_id))
            items = {}
            for item in bucket:
                items[item] = Item.get(item)
            request.write(render_template('my_bucket_list.html',
                                          {'comments': comments, 'user_id':str(request.get_secure_cookie('user_id'))[2:-1],
                                           'logged_in_username' : user2.name, 'bucket' : bucket,
                                           'items':items, 'user' : user.name, 'is_user' : is_authorised(request),
                                           'list_title' : ls.title, 'user_name' : user.name, 'list_id' : ls.id,
                                           'title' : "{}\'s Bucket List\'".format(user.name), 'user_list': user_list.id}))
        else:
            error404_handler(request)
            return

    elif method == 'POST':
        # TODO submit checkboxes to database
        text = request.get_field('comment')
        if text:
            user = int(request.get_secure_cookie('user_id'))
            c = Comment(user, text, list_id)
            c.add()

        ls = List.get(int(list_id))
        for i in [a.id for a in ls.get_items()]:
            checked = request.get_field("check{}".format(i))
            item = Item.get(i)
            item.completed = bool(checked)
            item.update()
        request.redirect(r'/list/{}'.format(list_id))
        return

def signup_handler(request):
    method = request.request.method
    if is_authorised(request):
        request.redirect(r'/')
        return

    if method == 'GET':
        request.write(render_template('signup.html', {'disp':False, 'is_user' : is_authorised(request), 'location' : '/user/create', 'title' : "Sign Up" }))
    elif method == 'POST':
        print("running post")
        username = request.get_field('username')
        password = request.get_field('password')
        repeat_password = request.get_field('repeat_password')
        user = User.get(username)
        if user is None and password == repeat_password and len(password) > 1:
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
        else:
            request.write(render_template('signup.html', {'user_issue': user is not None, 'disp':True, 'is_user' : is_authorised(request), 'location' : '/user/create', 'title' : "Sign Up" }))

def logout_handler(request):
    if not is_authorised(request):
        request.redirect(r'/')
        return

    request.clear_cookie('user_id')
    request.redirect(r'/')

def error404_handler(request):
    request.write(render_template('error404.html', { 'title' : "Error 404" }))

# GET /list/create - Call create screen
# POST /list/create - Post list to server and redirects to created list.
# GET /list/<listID> - Shows list referring to listID or says list not found.
# GET / - If not logged in, Shows decription and if you are, shows feed.

server = Server(hostname = '0.0.0.0')
server.register(r'/', index_handler)
server.register(r'/login', login_handler)
server.register(r'/list/create', list_creation_handler)
server.register(r'/list/(\d+)', list_display_handler)
server.register(r'/logout', logout_handler)
server.register(r'/user/create', signup_handler)
server.register(r'/.+', error404_handler)

server.run()
