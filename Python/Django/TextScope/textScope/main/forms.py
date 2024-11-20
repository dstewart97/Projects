from django import forms
from .models import Topic



# Form for new topic creation and editing exisiting topics
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['key', 'values']


# Dynamically displays all topics and lets users toggle which ones to include during processing.
class SelectTopicsForm(forms.Form):
    selected_topics = forms.ModelMultipleChoiceField(
        queryset = Topic.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = "Select Topics for Analysis"
    )


# Accepts .csv or .xlsx files for processing.
class FileUploadForm(forms.Form):
    file = forms.FileField(label = "Upload CSV or XLSX file")