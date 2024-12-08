from django import forms
from .models import Topic


# Form for new topic creation and editing exisiting topics
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['key', 'values']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically load topics for selection
        self.fields['key'].queryset = Topic.objects.all().values_list('key', flat=True)
        self.fields['values'].queryset = Topic.objects.all().values_list('values', flat=True)



# Dynamically displays all topics and lets users toggle which ones to include during processing.
class SelectTopicsForm(forms.Form):
    # Dynamically load all topics from the Topic model
    selected_topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),  # Get topics from the model
        widget=forms.CheckboxSelectMultiple,  # Allow multiple selection
        required=False,
        label=False
    )



# Accepts .csv or .xlsx files for processing.
class FileUploadForm(forms.Form):
    file = forms.FileField(label = "Upload CSV or XLSX file")



# Contact Form
class ContactForm(forms.Form):
    name = forms.CharField(label="Your Name", max_length=100)
    email = forms.EmailField(label="Your Email")
    message = forms.CharField(label="Your Message", widget=forms.Textarea)