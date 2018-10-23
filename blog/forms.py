from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        # 这里表明使用哪个模型构建表单，这里使用Comment模型
        model = Comment
        # 明确表明表单需要包含的的一些字段 name email body
        fields = ('name', 'email', 'body')
