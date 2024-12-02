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
    topics = {topic.key.lower(): [value.lower() for value in topic.values.split(',')] for topic in selected_topics}
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
    add_topic_form = TopicForm()
    edit_topic_forms = [TopicForm(instance=topic) for topic in topics]

    if request.method == 'POST':
        # Handle Add Topic Form
        if 'add-topic-form' in request.POST:
            add_topic_form = TopicForm(request.POST)
            if add_topic_form.is_valid():
                add_topic_form.save()
                return redirect('tool_view')
            else:
                return render(request, 'tool_view.html', {
                    'file_uploaded': file_uploaded,
                    'column_selected': column_selected,
                    'topics': topics,
                    'add_topic_form': add_topic_form,  # Return with errors if any
                    'edit_topic_forms': edit_topic_forms,
                })
            
        # Handle Edit Topic Form
        elif 'edit-topic-form' in request.POST:
            for topic in topics:
                print(topic)
                form = TopicForm(request.POST, instance=topic)
                print(form)
                if form.is_valid():
                    print(form)
                    form.save()
            return redirect('tool_view')
        
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
            selected_topics = Topic.objects.filter(id__in=selected_topics_ids)
            processed_data = process_topics(data, selected_topics, selected_column)
            request.session['processed_data'] = processed_data.to_json()
            time.sleep(5)
            processed_data_dict = processed_data.head(10).to_dict(orient='records')
            return render(request, 'tool_view.html', {
                'file_uploaded': True,
                'column_selected': True,
                'processed_data': processed_data_dict,
                'topics': topics,
                'add_topic_form': add_topic_form,
                'edit_topic_forms': edit_topic_forms,
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
                    return HttpResponse("Invalid file type, please upload a CSV or XLSX file.")
                request.session['data'] = data.to_json()
                column_choices = [(col, col) for col in data.columns]
                select_form = SelectTopicsForm(request.POST)
                return render(request, 'tool_view.html', {
                    'file_uploaded': True,
                    'select_form': select_form,
                    'column_choices': column_choices,
                    'topics': topics,
                    'add_topic_form': add_topic_form,
                    'edit_topic_forms': edit_topic_forms,
                })
        # Handle Reset
        elif 'reset' in request.POST:
            request.session.flush()
            return redirect('tool_view')
    else:
        upload_form = FileUploadForm()
    return render(request, 'tool_view.html', {
        'upload_form': upload_form,
        'file_uploaded': False,
        'column_selected': False,
        'topics': topics,
        'add_topic_form': add_topic_form,
        'edit_topic_forms': edit_topic_forms,
    })