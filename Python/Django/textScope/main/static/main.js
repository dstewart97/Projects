

// Updates the name when a file is uploaded
function updateFileName() {
    var fileInput = document.getElementById('file-input');
    var fileName = fileInput.files[0] ? fileInput.files[0].name : 'No file selected';
    document.getElementById('file-name').innerText = fileName;
};



// Show and Hide Add and Edit TOpic Modals
document.addEventListener("DOMContentLoaded", () => {
    const addTopicBtn = document.getElementById("openModalBtn");
    const addTopicModal = document.getElementById("addTopicModal");
    const closeAddTopic = document.getElementsByClassName("close")[0];

    console.log(closeAddTopic)

    // Open Modals
    addTopicBtn.addEventListener("click", () => addTopicModal.style.display = "block");

    // Close Modals
    closeAddTopic.addEventListener("click", () => addTopicModal.style.display = "none");

    window.addEventListener("click", (event) => {
        if (event.target === addTopicModal) addTopicModal.style.display = "none";
    });
});



// Toggle sidebar pop-out on main view
document.getElementById('toggle-sidebar').addEventListener('click', function() {
    document.querySelector('.sidebar').classList.toggle('sidebar-collapsed');
    document.querySelector('.content').classList.toggle('expanded');
});



// Spinner for file upload
document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const loadingSpinner = document.getElementById("loading-spinner");
    const messagesContainer = document.getElementById("messages-container");

    uploadForm.addEventListener("submit", () => {
        // Show spinner and hide messages
        loadingSpinner.style.display = "flex";
        loadingSpinner.style.justifyContent - "center";
        loadingSpinner.style.alignItems = "center";
        loadingSpinner.style.flexDirection = "column";
        loadingSpinner.style.marginTop = "2rem";
        loadingSpinner.style.marginBottom = "0";
        messagesContainer.style.display = "none";
    });

    // Hide spinner after a delay (if form submission is quick or processed asynch)
    setTimeout(() => {
        loadingSpinner.style.display = "none";
        messagesContainer.style.display = "block";
    }, 2000);
});



// Loader for Data Processing
document.addEventListener("DOMContentLoaded", () => {
    const processDataBtn = document.getElementById("process-data-btn")
    const loader = document.querySelector(".loader");

    processDataBtn.addEventListener("click", () => {
        loader.style.display = "block";
    });
});