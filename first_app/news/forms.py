from django import forms
from .models import News, Commentaries

class NewsModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'article', 
            'body',
            'image',
        ]

    def clean_article(self):
        data = self.cleaned_data.get('article')
        if len(data) < 5:
            raise forms.ValidationError('Article is not long enough')
        return data

class CommentaryModelForm(forms.ModelForm):
    class Meta:
        model = Commentaries
        fields = [
            'text'
        ]