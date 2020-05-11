from django.db import models

class Game(models.Model):
    owner = models.CharField(max_length=50) # Possibly bad
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=50)
    games = models.ManyToManyField(Game)

    def __str__(self):
        return self.name

class Snippet(models.Model):
    file = models.FileField(upload_to="user_files/snippets")
    artist = models.CharField(max_length=50)
    song = models.CharField(max_length=50)
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    sections = models.ManyToManyField(Section)

class Solution(models.Model):
    author = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Answer(models.Model):
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    authorAns = models.CharField(max_length=50)
    songAns = models.CharField(max_length=50)
    otherAns = models.CharField(max_length=100)

class GameBlueprint(models.Model):
    name = models.CharField(max_length=50)
    owner = models.CharField(max_length=50) # Possibly bad

class SectionBlueprint(models.Model):
    name = models.CharField(max_length=50)
    game = models.ForeignKey(GameBlueprint, on_delete=models.CASCADE)

class SnippetBlueprint(models.Model):
    file_set = models.IntegerField(default=0)
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to="user_files/snippets")
    artist = models.CharField(max_length=50)
    trackname = models.CharField(max_length=50)
    section = models.ForeignKey(SectionBlueprint, on_delete=models.CASCADE)
