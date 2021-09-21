class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title',  'content', 'image']
        labels = {
            'title':'タイトル',
            'content':'説明',
            'image':'画像',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label