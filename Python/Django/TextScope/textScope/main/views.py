import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FileUploadForm, SelectTopicsForm, TopicForm
from .models import Topic
from io import StringIO
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
    """Main view for the topic categorization tool."""
    file_uploaded = False
    column_selected = False
    processed_data = None
    column_choices = []
    topics = Topic.objects.all()  # Get all topics to display in the form
    
    # Debugging: Check the tooltip_text for each topic
    for topic in topics:
        print(f"Topic: {topic.key}, Tooltip: {topic.tooltip_text}")  # This will print to the console

    if request.method == 'POST':
        # Handle file upload
        upload_form = FileUploadForm(request.POST, request.FILES)
        if 'file' in request.FILES:
            file = request.FILES['file']
            data = handle_uploaded_file(file)
            if data is None:
                return HttpResponse("Invalid file type, please upload a CSV or XLSX file.")
            # Save uploaded data in session
            request.session['data'] = data.to_json()  # Convert DataFrame to JSON for storage
            # Dynamically create column choices for the file's columns
            column_choices = [(col, col) for col in data.columns]
            # Create SelectTopicsForm to let the user select topics for categorization
            select_form = SelectTopicsForm(request.POST)
            return render(request, 'tool_view.html', {
                'file_uploaded': True, 
                'select_form': select_form,
                'column_choices': column_choices,
                'topics': topics  # Pass topics to the template
            })
        # Handle column selection and process data
        if 'selected_column' in request.POST and 'selected_topics' in request.POST:
            data_json = request.session.get('data')
            data = pd.read_json(data_json)
            selected_column = request.POST.get('selected_column')
            selected_topics_ids = request.POST.getlist('selected_topics')
            # Retrieve selected topics from the database
            selected_topics = Topic.objects.filter(id__in=selected_topics_ids)
            # Process the data with the selected topics
            processed_data = process_topics(data, selected_topics, selected_column)
            # Save the processed data in session
            request.session['processed_data'] = processed_data.to_json()  # Save processed data in session
            # Convert processed_data to a list of dictionaries (for dynamic table rendering)
            processed_data_dict = processed_data.head(10).to_dict(orient='records')  # Limit to first 10 rows
            return render(request, 'tool_view.html', {
                'file_uploaded': True, 
                'column_selected': True, 
                'processed_data': processed_data_dict,
                'topics': topics  # Pass topics to the template
            })
        # Handle reset (start over)
        if 'reset' in request.POST:
            # Clear session data to reset the tool
            request.session.flush()  # This will clear all session data
            return redirect('tool_view')  # Redirect to the same view to start fresh
    else:
        upload_form = FileUploadForm()
    # Initial render with empty forms
    return render(request, 'tool_view.html', {
        'upload_form': upload_form, 
        'file_uploaded': False, 
        'column_selected': False,
        'topics': topics  # Pass topics for initial page load
    })