from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import pandas as pd
from .models import Topic
from .forms import TopicForm, SelectTopicsForm, FileUploadForm




def tool_view(request):
    topics = Topic.objects.all()
    topic_form = TopicForm()
    file_form = FileUploadForm()
    select_topics_form = SelectTopicsForm()
    processed_data = None
    column_options = []

    if request.method == 'POST':
        # Handle adding new topic
        if 'add_topic' in request.POST:
            topic_form = TopicForm(request.POST)
            if topic_form.is_valid():
                topic_form.save()

        # Handle selecting and deselecting topics
        elif 'select_topic' in request.POST:
            select_topics_form = SelectTopicsForm(request.POST)
            if select_topics_form.is_valid():
                selected_topics = select_topics_form.cleaned_data['selected_topics'] #HUH
                # Deselect all
                Topic.objects.update(selected = False) 
                # Mark selected topics as active
                for topic in selected_topics:
                    topic.selected = True
                    topic.save()

        # Hanlde file upload
        elif 'upload_file' in request.POST:
            file_form = FileUploadForm(request.POST, request.FILES)
            if file_form.is_valid():
                uploaded_file = request.FILES['file']
                data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                request.session['data'] = data.to_dict('records')
                column_options = list(data.columns)

        # Handle processing the data
        elif 'process_data' in request.POST:
            data = pd.DataFrame(request.session.get('data'))
            selected_column = request.POST.get('text_column')
            if selected_column:
                data['cleaned_text'] = data[selected_column].str.lower().str.replace(r'[^\w\s]', '', regex=True)
                processed_data = process_topics(data)
                processed_data = processed_data.to_dict('records')

    return render(request, 'tool_view.html', {
    'topics': topics,
    'topic_form': topic_form,
    'file_form': file_form,
    'select_topics_form': select_topics_form,
    'data': processed_data,
    'columns': column_options,
})



def process_topics(data):
    # Use only selected topics for processing
    topics = {topic.key: topic.values.split(',') for topic in Topic.objects.filter(selected=False)}
    print(topics)
    results = []
    for text in data['cleaned_text']:
        topic_counts = {key: sum(word in text.split() for word in values) for key, values in topics.items()}
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        dominant_topic = sorted_topics[0][0] if sorted_topics else "None"
        additional_topics = [t[0] for t in sorted_topics[1:4]]
        results.append({'dominant_topic': dominant_topic, 'subtopics': ', '.join(additional_topics)})

    data['dominant_topic'] = [res['dominant_topic'] for res in results]
    data['subtopics'] = [res['subtopics'] for res in results]
    return data


def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('tool_view')  # Redirect back to the main page

    else:
        form = TopicForm(instance=topic)

    return render(request, 'edit_topic.html', {'form': form, 'topic': topic})