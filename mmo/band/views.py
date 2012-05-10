from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth # django.contrib is a module
from django.contrib.auth.models import User
from django.template import RequestContext
from band.decorators import *
from band.forms import *
from band.functions import *
import datetime

## NOTE: Because you have CSRF enabled in your Middleware, all your render_to_response functions that have a form must have a third argument 'context_instance=RequestContext(request)', and all your forms must have the {% csrf_token %} . Remember to import all of these from django above too, like 'from django.template import RequestContext' - who would have guessed this was necessary?!

# Create your views here.

"""Cookies, Sessions, and Users

To set a cookie, use the 'set_cookie()' method on an HttpResponse object:

def set_color(request):
    if "favorite_color" in request.GET:

        # Create an HttpResponse object...
        response = HttpResponse("Your favorite color is now %s" % \
            request.GET["favorite_color"])

        # ... and set a cookie on the response
        response.set_cookie("favorite_color",
                            request.GET["favorite_color"]) # sets the variable 'favorite_color' equal to the 'request.GET's 'favorite_color', yes? So this is the value that can be retrieved from the cookie later

        return response

    else:
        return HttpResponse("You didn't give a favorite color.")


Django protects you from sending sensitive data in a cookie's plaintext by abstracting the cookie level away - stores data on the server side and cookies only use a hashed session ID, not the data itself - so the data still can't be retrieved, though if you steal a cookie you can still pretend to be someone else


Enabling Sessions

Make sure MIDDLEWARE_CLASSES in settings.py includes 'django.contrib.sessions.middleware.SessionMiddleware'
Make sure 'django.contrib.sesions' is in INSTALLED_APPS (and run manage.py syncdb after putting it there)

When SessionMiddleware is activated, each HttpRequest object will have a 'session' attribute, which is a dictionary-like object

# Set a session value:
request.session["fav_color"] = "blue"

# Get a session value -- this could be called in a different view,
# or many requests later (or both):
fav_color = request.session["fav_color"]

# Clear an item from the session:
del request.session["fav_color"]

# Check if the session has a given key:
if "fav_color" in request.session:
    stuff


Simple example of preventing a user from posting more than once:

def post_comment(request):
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')

    if 'comment' not in request.POST:
        raise Http404('Comment not submitted')

    if request.session.get('has_commented', False):
        return HttpResponse("You've already commented.")

    c = comments.Comment(comment=request.POST['comment'])
    c.save()
    request.session['has_commented'] = True
    return HttpResponse('Thanks for your comment!')

def login(request):
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    try:
        m = Member.objects.get(username=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['member_id'] = m.id
            return HttpResponseRedirect('/you-are-logged-in/')
        except Member.DoesNotExist:
            return HttpResponse("Your username and password didn't match.")

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


Can test if user's browser accepts cok=okies with
request.session.set_test_cookie()
and then in another view call
request.session.test_cookie_worked()

Can delete test cookie using
delete_test_cookie()


Typical usage example of test cookie:

def login(request):
    # If we submitted the form...
    if request.method == 'POST':

        # Check that the test cookie worked (we set it below):
        if request.session.test_cookie_worked():

            # The test cookie worked, so delete it.
            request.session.delete_test_cookie()

            # In practice, we'd need some logic to check username/password
            # here, but since this is an example...
            return HttpResponse("You're logged in.")

        # The test cookie failed, so display an error message.
        else:
            return HttpResponse("Please enable cookies and try again.")

    # If we didn't post, send the test cookie along with the login form.
    request.session.set_test_cookie()
    return render_to_response('foo/login_form.html')


The 'request.user' interface 

Django has a built-in authentication system - awesome. Can tell if a user is logged in with the 'is_authenticated()' method:

if request.user.is_authenticated():
    # Do something for authenticated users.
else:
    # Do somethihng for anonymous users


To limit access, use a 'request.user.is_authenticated()'

from django.http import HttpResponseRedirect

def my_view(request):
    if not request.user.is_authenticated():
        return HttpResponseResponseRedirect('/accounts/login/?next=%s' % request.path)

Creating Users:
Create users with the create_user helper function:

from django.contrib.auth.models import User
user = User.objects.create_user(username='john',
                                email='jlennon@beatles.com',
                                password='glass onion')
user.save()

Can change a password with 'set_password()'

user = User.objects.get(username='john')
user.set_password('goo goo goo joob')
user.save()

Don't set the password directly since it's stored as a salted hash and can't be edited directly


So, to handle Registration fucking finally:

from django import forms
from django.contrib.auth.forms import UserCreation Form
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })


assumes a template named registration/register.html - so let's go make that!

(wow, you actually got through all of this)
"""

# the 'request.session' etc isn't unique to view - it's passed *in* to all view functions - that's why every view function has 'function(request)' - you can just as easily pass to other functions. Fantastic.

def index(request):
    if request.user.is_authenticated():
        update_sidebar(request)
        try: # checks if there is 'login_text' - allows for the deleting of the session value so it isn't repeated every time. Also removes the need to use {{request.session.login_text}} in the template so the 'context processor' for that isn't necessary, but I kept that in settings anyway - just in case we'll need it later ;)
            index_text = request.session['index_text'] # seems a bit hackish - not sure 'request.session[]' is the most efficient way to get this done anymore since you don't need to pass it to the template directly from the other views without giving an argument to the HttpResponseRedirect...but it works
            del request.session['index_text']
        except KeyError:
            index_text = None
        return render_to_response('index.html', {'index_text': index_text}, context_instance=RequestContext(request))
    else:
        try:
            request.session['initial_visit'] # checks if 'initial_visit' exists - if it does, don't have any welcome_text
            try: # allows other views to pass in welcome_text
                welcome_text = request.session['index_text']
                del request.session['index_text']
            except:
                welcome_text = None
        except KeyError:
                request.session['initial_visit'] = False
                welcome_text = 'Welcome to AdventureBand! Please login.'
        return render_to_response('index.html', {'index_text': welcome_text}, context_instance=RequestContext(request))

def register(request):
    if request.user.is_authenticated():
        request.session['index_text'] = 'You are logged in. Please logout first.'
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid(): # This 'is_valid()' method is what runs all the functions in the form (the 'clean_username()', 'clean_email', etc. This is why your validation wasn't working earlier! This is also what checks all the form fields were filled out right and returns errors if they aren't!
                new_user = form.save()
                request.session['login_text'] = 'You have successfully registered! Please login to begin the game.'
                return HttpResponseRedirect('/login/')
        else:
            form = UserRegistrationForm()
        return render_to_response('login/register.html', {'form': form}, context_instance=RequestContext(request)) # for some reason this can't be indented. Hmm.

def login_view(request):
    if request.user.is_authenticated():
        request.session['index_text'] = 'You are already logged in.'
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = UserLogin(request.POST)
            if form.is_valid(): # not sure if this is running the 'clean_username' function or not in the 'UserLogin()' form. If not, then this is checking nothing I believe
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                # note 'username=username.lower()' - since all usernames are stored in lowercase, convert whatever input was given for username to lowercase before checking to see if the user exists
                user = auth.authenticate(username=username.lower(), password=password)
                if user is not None and user.is_active:
                    # Correct password, and the user is marked "active"
                    auth.login(request, user)
                    # Redirect to a success page.
                    request.session['index_text'] = 'You have successfully logged in!'
                    return HttpResponseRedirect('/')
                else:
                    request.session['login_text'] = 'The username and password did not work. Please try again.'
                    return HttpResponseRedirect('/login/')
            else:
                request.session['login_text'] = 'The username and password did not work. Please try again.'
                return HttpResponseRedirect('/login/')
        else:
            form = UserLogin()
            try:
                login_text = request.session['login_text']
                del request.session['login_text']
            except KeyError:
                login_text = None
        return render_to_response('login/login.html', {'form': form, 'login_text': login_text}, context_instance=RequestContext(request))

def logout_view(request):
    if request.user.is_authenticated():
        for sesskey in request.session.keys(): # delete all session keys
            del request.session[sesskey]
        auth.logout(request)
        request.session['login_text'] = 'You are now logged out.'
        return HttpResponseRedirect('/login/')
    else:
        for sesskey in request.session.keys():
            del request.session[sesskey]
        request.session['login_text'] = 'You are not logged in.'
        return HttpResponseRedirect('/login/')

@login_required(login_text='Nope, we checked and sadly you weren\'t logged in.')
def check_login(request):
    request.session['index_text'] = 'Yep, we checked and you\'re logged in!'
    return HttpResponseRedirect('/')

@login_required(login_text='Please login before creating a character.')
def create_character(request): # holy shit it all works perfectly. Look how amazing and straightforward coding is when you understand what you're doing :)=
    if request.method == 'POST':
        form = CreateCharacter(request.POST)
        if form.is_valid(): # ahh don't have an 'else' statement or else the standard validation errors won't be raised, the 'else' statement will override them
            char = form.save(commit=False)
            char.user = request.user # oh jesus that was way easier than you thought haha - you set a request.session['user_id'] equal to User.objects.get(username=username) and called that here...totally unnecessary and didn't work, turns out the foreign key requires inputting the *object* itself, not an id inside the object. Remember that.
            char.name_lower = request.POST.get('name', '').lower()
            char.create_date = datetime.datetime.now()
            char.level = 1
            char.exp = 0
            char.max_hp = 0
            char.current_hp = 0
            char.strength = char.intelligence = char.wisdom = char.dexterity = char.constitution = char.charisma = 3
            char.gold = 0
            char.first_time = True
            char.dungeon = 101
            char.save()
            form.save_m2m() # saves the many-to-many data here - needed when commit=False
            request.session['char_object'] = Character.objects.get(id=char.id)
            return HttpResponseRedirect('/first/')
    else:
        form = CreateCharacter()
    return render_to_response('character/create.html', {'form': form}, context_instance=RequestContext(request))

@login_required(login_text='Please login before choosing a character.')
def choose_character(request):
    if request.method == 'POST':
        try:
            request.session['char_object'] = Character.objects.get(id=request.POST.get('character', ''))
        except ValueError: # if no character is chosen
            char_choices = Character.objects.order_by('id').filter(user=request.user)
            return render_to_response('character/choose.html', {'choices': char_choices}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/venture/')
    else:
        char_choices = Character.objects.order_by('id').filter(user=request.user) # note - use 'filter', not get, when there's the possibility of more than one object (or no objects) being returned, since 'filter' always returns a QuerySet - a tuple list
    return render_to_response('character/choose.html', {'choices': char_choices}, context_instance=RequestContext(request))

@login_required(login_text='Please login before deselecting a character.')
def deselect(request):
    try:
        del request.session['char_object']
        request.session['index_text'] = 'Successfully deselected.'
        return HttpResponseRedirect('/')
    except KeyError:
        request.session['index_text'] = 'No character is selected.'
        return HttpResponseRedirect('/')

@login_required(login_text='Please login before deleting a character.')
def delete_char(request): #eventually make this a character manage page - also, super insecure, doesn't check if it's the right user logged in - add that in later, not hard at all
# also make sure they don't delete a currently selected character, or at least figuer out a way to process that
    if request.method == 'POST':
        try:
            char = Character.objects.get(id=request.POST.get('character', ''))
        except ValueError:
            char_choices = Character.objects.order_by('id').filter(user=request.user)
            return render_to_response('character/delete.html', {'choices': char_choices}, context_instance=RequestContext(request))
        try:
            if char == request.session['char_object']:
                del request.session['char_object']
        except KeyError:
            pass
        request.session['index_text'] = 'You have successfully deleted %s. =\'(' % char.name
        char.delete()
        return HttpResponseRedirect('/')
    else:
        char_choices = Character.objects.order_by('id').filter(user=request.user) # note - use 'filter', not get, when there's the possibility of more than one object (or no objects) being returned, since 'filter' always returns a QuerySet - a tuple list
    return render_to_response('character/delete.html', {'choices': char_choices}, context_instance=RequestContext(request))

@login_required(login_text='Please login before setting up your character.')
def first(request):
    try:
        char = Character.objects.get(id=request.session['char_object'].id)
    except KeyError:
        return HttpResponseRedirect('/start/')
    if char.first_time == True:
        if request.method =='POST':
            form = SetAttributes(request.POST)
            if form.is_valid():
                # figure out a way to clean these at some point
                char.strength = request.POST.get('strength', '')
                char.intelligence = request.POST.get('intelligence', '')
                char.wisdom = request.POST.get('wisdom', '')
                char.dexterity = request.POST.get('dexterity', '')
                char.constitution = request.POST.get('constitution', '')
                char.charisma = request.POST.get('charisma', '')
                char.max_hp = char.current_hp = request.POST.get('max_hp', '')
                char.gold = 100 + int(char.charisma) * 15
                char.first_time = False
                char.save()
                request.session['index_text'] = 'Congratulations, you have successfully set up %s!' % char.name
                return HttpResponseRedirect('/')
            else:
                setup_char(char)
                request.session['char_object'] = char
                form = SetAttributes(initial={'strength': char.strength, 'intelligence': char.intelligence, 'wisdom': char.wisdom, 'dexterity': char.dexterity, 'constitution': char.constitution, 'charisma': char.charisma, 'max_hp': char.max_hp})
                intro_text = 'Something didn\'t go quite right there. Care to try again?'
                return render_to_response('character/first.html', {'form': form, 'intro_text': intro_text, 'char_name': char.name}, context_instance=RequestContext(request))
        else:
            setup_char(char) # distributes attributes
            request.session['char_object'] = char
            form = SetAttributes(initial={'strength': char.strength, 'intelligence': char.intelligence, 'wisdom': char.wisdom, 'dexterity': char.dexterity, 'constitution': char.constitution, 'charisma': char.charisma, 'max_hp': char.max_hp}) # still an unbound form since you're using 'initial' - so no validation errors on empty fields (though there aren't any empty fields here - just better practice)
            intro_text = 'Choose %s\'s starting attributes' % char.name
            return render_to_response('character/first.html', {'form': form, 'intro_text': intro_text, 'char_name': char.name}, context_instance=RequestContext(request))
    else:
        request.session['index_text'] = ('%s has already distributed attribute points.' % char.name)
        return HttpResponseRedirect('/')

@login_required(login_text='Please login before venturing off.')
def venture(request):
    try:
        char = Character.objects.get(id=request.session['char_object'].id)
    except KeyError:
        return HttpResponseRedirect('/start/')
    if char.first_time == True:
        return HttpResponseRedirect('/first/')
    else:
        if char.dungeon == 0:
            return HttpResponseRedirect('/town/')
        elif char.dungeon == 101: # run this on first time playing
            char.dungeon = 0
            char.save() # remember to save every time you change an object's values
            request.session['town_text'] = 'Welcome to the town! Here, you can buy the equipment you need before heading out to the dungeon.'
            return HttpResponseRedirect('/town/')
    return HttpResponseRedirect('/dungeon/')

@login_required(login_text='Please login before venturing off.')
def town(request):
    try:
        char = Character.objects.get(id=request.session['char_object'].id)
        if char.dungeon == 0:
            try:
                town_text = request.session['town_text']
                del request.session['town_text']
            except KeyError:
                town_text = None 
            return render_to_response('town.html', {'town_text': town_text}, context_instance=RequestContext(request))
        elif char.dungeon == 101:
            return HttpResponseRedirect('/venture/')
        elif char.dungeon:
            return HttpResponseRedirect('/dungeon/')
    except KeyError:
        return HttpResponseRedirect('/venture/')

@login_required(login_text='Please login before venturing off.')
def dungeon(request):
    try:
        char = Character.objects.get(id=request.session['char_object'].id)
        if char.dungeon == 0:
            return HttpResponseRedirect('/town/')
        elif char.dungeon == 101:
            return HttpResponseRedirect('/venture/')
        elif char.dungeon:
            try:
                dungeon_text = request.session['dungeon_text']
                del request.session['dungeon_text']
            except KeyError:
                dungeon_text = None
            return render_to_response('dungeon.html', {'dungeon_text': dungeon_text}, context_instance=RequestContext(request))
    except KeyError:
        return HttpResponseRedirect('/venture/')

def town_general(request):
    return render_store(request, 'General Store')

def town_weapons(request):
    return render_store(request, 'Weapon Smith')

def town_armory(request):
    return render_store(request, 'Armory')

def town_magic(request):
    return render_store(request, 'Magic Shop')

def town_temple(request):
    return render_store(request, 'Temple')

def town_alchemist(request):
    return render_store(request, 'Alchemist')

def town_market(request):
    return render_store(request, 'Black Market')

def town_home(request):
    return render_store(request, 'Home')