from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class QForm(forms.Form):
    """
    컬럼명을 입력받는다.
    """

    q = forms.CharField()

    # TODO: Re-enable this after Django 1.11 #28105 is available
    # polygon = gisforms.PointField()

    required_css_class = 'bootstrap3-req'

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling.")
        return cleaned_data 