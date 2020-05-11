from django.contrib import admin

# Register your models here.

from .models import Game, Section, Snippet, GameBlueprint, SectionBlueprint, SnippetBlueprint

admin.site.register(Game)
admin.site.register(Section)
admin.site.register(Snippet)
admin.site.register(GameBlueprint)
admin.site.register(SectionBlueprint)
admin.site.register(SnippetBlueprint)
