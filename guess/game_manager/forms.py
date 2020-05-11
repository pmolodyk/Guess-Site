from django import forms
from .models import Game, Section, Snippet

class SnippetForm(forms.Form):
    artist = forms.CharField(required=True)
    song = forms.CharField(required=True)
    start = forms.IntegerField(required=True)
    end = forms.IntegerField(required=True)
    file = forms.FileField(required=True)

class SectionForm(forms.Form):
    name = forms.charField(required=True)

    def __init__(self, *args, ** kwargs):
        addedSnippets = kwargs.pop('extra')
        super.init(*args, **kwargs)
        for i, snippet in enumerate(addedSnippets):
            self.fields['snippet_%s' % i] = SnippetForm(snippet)

    def getSnippets(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('snippet_'):
                yield value

class NewGameForm(forms.Form):
    name = forms.charField(required=True)

    def __init__(self, *args, **kwargs):
        addedSections = kwargs.pop('extra')
        super.init(*args, **kwargs)

        for i, section in enumerate(addedSections):
            self.fields['section_%s' % i] = SectionForm(section)

    def getSections(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('section_'):
                yield value
