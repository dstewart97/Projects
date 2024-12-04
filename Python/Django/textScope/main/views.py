import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FileUploadForm, SelectTopicsForm, TopicForm
from .models import Topic
from io import StringIO
import time
import csv


def handle_uploaded_file(file):
    """Handles file upload and returns the data in a DataFrame."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    return None



def process_topics(data, selected_topics, selected_column):
    """Process the topics by matching exact phrases in the selected column with the selected topics."""
    # Build the topics dictionary from the selected topics, ensuring case-insensitive matching
    # topics = {topic.key.lower(): [value.lower() for value in topic.values.split(',')] for topic in selected_topics}
    topics = {}
    for topic in selected_topics:
        if isinstance(topic, dict):
            key = topic['key'].lower()
            values = [value.strip() for value in topic['values'].split(',')]
        else:
            key = topic.key.lower()
            values = [value.strip().lower() for value in topic.values.split(',')]
        topics[key] = values
    results = []

    # Fill Null with blank before processing 
    data[selected_column] = data[selected_column].fillna('')

    # Iterate through each text entry in the selected column
    for text in data[selected_column]:
        # Convert the text to lowercase for case-insensitive matching
        text = text.lower()  

        # Count the occurrences of each topic (as a full phrase) in the text
        topic_counts = {key: sum(phrase in text for phrase in values) for key, values in topics.items()}   

        # Filter out topics with a count of 0
        topic_counts = {key: count for key, count in topic_counts.items() if count > 0}      

        # If there are any matching topics, sort them by count (descending)
        if topic_counts:
            sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)          
            # Dominant topic (most frequent)
            dominant_topic = sorted_topics[0][0]           
            # Subtopics (top 3 after the dominant topic)
            additional_topics = [t[0] for t in sorted_topics[1:4]]
        else:
            dominant_topic = "None"
            additional_topics = []       
        # Store the results (only the text, dominant topic, and subtopics)
        results.append({
            'selected_text': text,  # Keep the original text column
            'dominant_topic': dominant_topic,
            'subtopics': ', '.join(additional_topics)
        })

    # Convert the results into a DataFrame
    processed_data = pd.DataFrame(results)
    return processed_data



def export_data(request, file_type):
    """Export processed data as CSV or XLSX."""
    # Retrieve the processed data from the session
    processed_data_json = request.session.get('processed_data')
    # If processed data is not found, return an error
    if not processed_data_json:
        return HttpResponse("No processed data available for export.", status=400)
    processed_data = pd.read_json(processed_data_json)
    # Convert data to either CSV or XLSX based on the requested file type
    if file_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed_data.csv"'
        processed_data.to_csv(response, index=False)
    elif file_type == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="processed_data.xlsx"'
        processed_data.to_excel(response, index=False)
    else:
        return HttpResponse("Invalid file type", status=400)
    return response



def tool_view(request):
    file_uploaded = False
    column_selected = False
    processed_data = None
    topics = Topic.objects.all()

    # Load permanent topics from the database
    permanent_topics = Topic.objects.all()
    # Load session-based topics or initialize if not present
    session_topics = request.session.get('session_topics', [])

    if request.method == 'POST':
        # Handle Add Temporary Topic
        if 'add_session_topic' in request.POST:
            new_topic = {
                'id': f"session_{len(session_topics) + 1}",
                'key' : request.POST['session_topic_name'],
                'values' : request.POST['session_topic_keywords']
            }
            session_topics.append(new_topic)
            request.session['session_topics'] = session_topics
            return redirect('tool_view') # Avoid reloading form

        # Handle Process Data Form
        elif 'process_data' in request.POST:
            data_json = request.session.get('data')
            if not data_json:
                return HttpResponse("Session expired or data missing. Please upload a file again.", status=400)
            
            data = pd.read_json(data_json)
            selected_column = request.POST.get('selected_column')
            selected_topics_ids = request.POST.getlist('selected_topics')

            if not selected_column or not selected_topics_ids:
                return HttpResponse("Please select a column and at least one topic for categorization.", status=400)
            
            # Seperate session and permanenet topics
            permanent_topic_ids = []
            session_topic_keys = []
            
            for topic_id in selected_topics_ids:
                if topic_id.startswith("session_"):
                    session_topic_keys.append(topic_id.split("_", 1)[1])
                else:
                    permanent_topic_ids.append(int(topic_id))

            # Fetch permanent topics and session topics 
            permanent_topics = Topic.objects.filter(id__in=permanent_topic_ids)
            session_topics_dict = {str(topic['id']): topic for topic in session_topics}

            # Convert session topics into object-like structures
            session_topic_objects = [
                type('TempTopic', (object), {'key': topic['key'], 'values': topic['values']})
                for key, topic in session_topics_dict.items() if key in session_topic_keys
            ]

            #combine permanenet and session topics
            selected_topics = list(permanent_topics) + session_topic_objects
            
            # Process data with combined topics
            processed_data = process_topics(data, selected_topics, selected_column)
            request.session['processed_data'] = processed_data.to_json()
            time.sleep(5)
            processed_data_dict = processed_data.head(10).to_dict(orient='records')
            return render(request, 'tool_view.html', {
                'file_uploaded': True,
                'column_selected': True,
                'processed_data': processed_data_dict,
                'permanent_topics' : permanent_topics,
                'session_topics' : session_topics
            })
        
        # Handle File Upload
        upload_form = FileUploadForm(request.POST, request.FILES)
        if 'file' in request.FILES:
            file = request.FILES['file']
            max_size_kb = 3000
            allowed_file_types = ['.csv', '.xlsx']
            if file.size > max_size_kb * 1024:
                messages.error(request, "The file is too large....maximum size allowed is 3000 KB")
            elif not any(file.name.endswith(ext) for ext in allowed_file_types):
                messages.error(request, "Invalid file type...only CSV and XLSX will be processed")
            else:
                data = handle_uploaded_file(file)
                messages.success(request, "File uploaded successfully...")
                if data is None:
                    messages.error(request, "Invalid file type...only CSV and XLSX will be processed") # MAYBE CHANGE????
                request.session['data'] = data.to_json()
                column_choices = [(col, col) for col in data.columns]
                select_form = SelectTopicsForm(request.POST)
                return render(request, 'tool_view.html', {
                    'file_uploaded': True,
                    'select_form': select_form,
                    'column_choices': column_choices,
                    'topics': topics,
                    'permanent_topics' : permanent_topics,
                    'session_topics' : session_topics
                })
            
        # Handle Reset
        elif 'reset' in request.POST:
            request.session.flush()
            return redirect('tool_view')
    else:
        upload_form = FileUploadForm()

    combined_topics = list(permanent_topics) + session_topics
    return render(request, 'tool_view.html', {
        'upload_form': upload_form,
        'file_uploaded': False,
        'column_selected': False,
        'topics': combined_topics,
        'permanent_topics' : permanent_topics,
        'session_topics' : session_topics
    })