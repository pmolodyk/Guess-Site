from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings

from .models import Game, Section, Snippet, GameBlueprint, SectionBlueprint, SnippetBlueprint, GameSolution, SnippetSolution

#Login Functions
def loginView(request):
    if request.user.is_authenticated:
        return redirect('dashboard/')
    return render(request, 'game_manager/login.html')

def authAction(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('game_manager:dashboard')
    else:
        return render(request, 'game_manager/login.html', {
            'error_message': "Username or password incorrect!",
        })

#dashboard and info pages
@login_required
def myGamesView(request):
    username = request.user.username
    userGames = Game.objects.filter(owner=username)
    return render(request, 'game_manager/list-games.html', {'games': userGames, 'title' : 'My Games'})

@login_required
def gameView(request, gameNum):
    game = Game.objects.filter(id = gameNum)[0]
    username = request.user.username
    if username != game.owner:
        return render(request, 'game_manager/access-denied.html', {'message' : 'Access to game denied!'})
    return render(request, 'game_manager/game-view.html', {'game' : game})

@login_required
def dashboardView(request):
    return myGamesView(request)

#Game creation
@login_required
def createBlueprint(request):
    blueprint = GameBlueprint(name="New Game", owner=request.user.username)
    blueprint.save()
    print("Blueprint created")
    num = blueprint.id
    return redirect("/game_manager/gameCreator/" + str(num))

@login_required
def createGameView(request, num):
    blueprint = GameBlueprint.objects.filter(id = num)[0] # Add existence check!
    if blueprint.owner != request.user.username:
        return render(request, 'game_manager/access-denied.html', {'message' : 'You can only edit your own games! (You are doing nasty things, stop!)'})
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)

        blueprint.name = request.POST.get("game-title")

        for key in request.POST:
            if key == "game-title":
                continue
            if "section-title" in key:
                sectionNum = int(''.join(filter(str.isdigit, key)))
                section = SectionBlueprint.objects.filter(id = sectionNum)[0]
                section.name = request.POST.get(key)
                section.save()
                # print(sectionNum, section.name)
            if "snippet-trackname" in key:
                snippetNum = int(''.join(filter(str.isdigit, key)))
                snippet = SnippetBlueprint.objects.filter(id = snippetNum)[0]
                snippet.trackname = request.POST.get(key)
                snippet.save()
            if "snippet-artist" in key:
                snippetNum = int(''.join(filter(str.isdigit, key)))
                snippet = SnippetBlueprint.objects.filter(id = snippetNum)[0]
                snippet.artist = request.POST.get(key)
                snippet.save()
            # if "snippet-file" in key:
            #     snippetNum = int(''.join(filter(str.isdigit, key)))
            #     snippet = SnippetBlueprint.objects.filter(id = snippetNum)[0]
            #     snippet.filename = request.POST.get(key)
            #     snippet.file = request.FILES[key]
            #     snippet.save()
            if "snippet-setfile" in key:
                snippetNum = int(''.join(filter(str.isdigit, key)))
                snippet = SnippetBlueprint.objects.filter(id = snippetNum)[0]
                snippet.filename = ("snippet-file-" + str(snippetNum))
                snippet.file = request.FILES[snippet.filename]
                print(snippet.file)
                snippet.file_set = 1
                snippet.save()
                if default_storage.size(snippet.file.path) > int(settings.MAX_UPLOAD_SIZE):
                    default_storage.delete(snippet.file.path)
                    snippet.file_set = 0
                    snippet.save()
                    blueprint.save()
                    return render(request, 'game_manager/newgame.html', {'blueprint' : blueprint, 'error_message' : "FILE TOO LARGE (must be under 10Mb)"})
            if "snippet-changefile" in key:
                snippetNum = int(''.join(filter(str.isdigit, key)))
                snippet = SnippetBlueprint.objects.filter(id = snippetNum)[0]
                default_storage.delete(snippet.file.path)
                snippet.file_set = 0
                snippet.save()
        blueprint.save()

        if request.POST.get("add-section"):
            newSection = SectionBlueprint(name="New Section", game=blueprint)
            newSection.save()
            # print(blueprint.sectionblueprint_set.all())
        elif request.POST.get("add-snippet"):
            sectionNum = int(request.POST.get("add-snippet"))
            sec = SectionBlueprint.objects.filter(id = sectionNum)[0]
            newSnippet = SnippetBlueprint(artist="Artist", trackname="Trackname", section=sec)
            newSnippet.save()
        elif request.POST.get("create"):
            newGame = Game(name=blueprint.name, owner=blueprint.owner)
            newGame.save()
            for sectionBp in blueprint.sectionblueprint_set.all():
                newSection = Section(name = sectionBp.name)
                newSection.save()
                newSection.games.add(newGame)
                newSection.save()
                for snippetBp in sectionBp.snippetblueprint_set.all():
                    newSnippet = Snippet(artist=snippetBp.artist, song=snippetBp.trackname)
                    newSnippet.save()
                    newSnippet.sections.add(newSection)
                    newSnippet.file = snippetBp.file
                    newSnippet.save()
            return redirect('/game_manager/dashboard')

    return render(request, 'game_manager/newgame.html', {'blueprint' : blueprint})

#Gameplay
@login_required
def playGame(request, num):
    if len(Game.objects.filter(id = num)) == 0:
        return render(request, 'game_manager/access-denied.html', {'message' : 'This game does not exist! (probably)'})
    game = Game.objects.filter(id = num)[0]
    return render(request, 'game_manager/access-denied.html', {'message' : 'If you see this message, something is broken, please contact the developer.'})
