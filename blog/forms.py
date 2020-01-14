from django import forms
from django.core.exceptions import ValidationError
from .models import Tag, Post

#lass TagForm(forms.Form):
class TagForm(forms.ModelForm):
    ### убрали т.к. forms.ModelForm связывает форму и модель
    # title = forms.CharField(max_length=50)
    # slug = forms.CharField(max_length=50)
    # title.widget.attrs.update({'class': 'form-control'}) # задаем класс для поля html формы
    # slug.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tag
        fields = ['title', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), # задаем класс для поля html формы
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()  #self.cleaned_data.get('slug')
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(f'Slug must be unique. We have "{new_slug}" slug already')
        return new_slug

    ### forms.ModelForm свой авто сайв и апдейт
    # def save(self):
    #     new_tag = Tag.objects.create(
    #         title=self.cleaned_data['title'],
    #         slug=self.cleaned_data['slug']
    #     )
    #     return new_tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        # для bootstrap добавляем формат и классы полям
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()  # self.cleaned_data.get('slug')
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        # if Tag.objects.filter(slug__iexact=new_slug).count():
        #     raise ValidationError(f'Slug must be unique. We have "{new_slug}" slug already')
        return new_slug



