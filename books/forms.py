from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        required=True
    )
