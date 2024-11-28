function toggleTopicManager() {
    const modal = document.getElementById('topic-modal');
    modal.classList.toggle('hidden');
    modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
}


function saveTopics() {
    const formData = new FormData(document.getElementById('selectTopicsForm'));
    fetch("", {
        method: "POST",
        headers: { "X-CSRFToken": "{{ csrf_token }}" },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert("Topics saved successfully!");
        }
    })
    .catch(error => console.error('Error:', error));
}


function updateFileName() {
    var fileInput = document.getElementById('file-input');
    var fileName = fileInput.files[0] ? fileInput.files[0].name : 'No file selected';
    document.getElementById('file-name').innerText = fileName;
}