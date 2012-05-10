from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from band.models import * # strange that you don't need to import this in views - threw you off for a sec
from band.decorators import *

def setup_char(char):
    # note - after changing these values, you must *save* it for it to actually be stored to the database
    # next, lower the distributions here and allow the user to pick what to do with the brunt of the attribute points! :D (figure out how to make this into an html form where users can dynamically adjust points around - need any javascript/jQuery perhaps?)

    # 6 points distributed here
    if char.race == 'H':
        char.strength = char.strength + 1
        char.intelligence = char.intelligence + 1
        char.wisdom = char.wisdom + 1
        char.dexterity = char.dexterity + 1
        char.constitution = char.constitution + 1
        char.charisma = char.charisma + 1
    elif char.race == 'E':
        char.strength = char.strength + 0
        char.intelligence = char.intelligence + 2
        char.wisdom = char.wisdom + 0
        char.dexterity = char.dexterity + 2
        char.constitution = char.constitution + 0
        char.charisma = char.charisma + 2
    elif char.race == 'D':
        char.strength = char.strength + 3
        char.intelligence = char.intelligence + 0
        char.wisdom = char.wisdom + 0
        char.dexterity = char.dexterity + 0
        char.constitution = char.constitution + 3
        char.charisma = char.charisma + 0

    # 15 points distributed total here
    if char.char_class == 'W':
        char.strength = char.strength + 6
        char.intelligence = char.intelligence + 0
        char.wisdom = char.wisdom + 0
        char.dexterity = char.dexterity + 3
        char.constitution = char.constitution + 6
        char.charisma = char.charisma + 0
    elif char.char_class == 'R':
        char.strength = char.strength + 3
        char.intelligence = char.intelligence + 2
        char.wisdom = char.wisdom + 0
        char.dexterity = char.dexterity + 6
        char.constitution = char.constitution + 2
        char.charisma = char.charisma + 2
    elif char.char_class == 'M':
        char.strength = char.strength + 0
        char.intelligence = char.intelligence + 8
        char.wisdom = char.wisdom + 5
        char.dexterity = char.dexterity + 2
        char.constitution = char.constitution + 0
        char.charisma = char.charisma + 0

    char.max_hp = char.current_hp = char.constitution / 2 # returns a rounded-down integer by default it seems, pretty handy

    # total points: 18 (beginning 3 value * 6 attribs) + 6 + 15 = 39
    # 69 total after validation

    # char.save() # don't save here since then given the way you have the current first() view setup someone could game the system - only save once, which is set up elsewhere in the view

# there must be a better way to do this than calling this in every single view function, but I haven't found it yet..
# actually, for now - just put it in the functions that could possibly change it - which would be everything that either a changing function redirects to or a changing function itself
def update_sidebar(request):
    try:
        request.session['char_object'] = Character.objects.get(id=request.session['char_object'].id)
    except KeyError:
        pass

@login_required(login_text='Please login before venturing off.')
def render_store(request, store):
    store_name = store
    try:
        store_text = request.session['store_text']
        del request.session['store_text']
    except KeyError:
        store_text = None
    return render_to_response('store.html', {'store_name': store_name, 'store_text': store_text}, context_instance=RequestContext(request))