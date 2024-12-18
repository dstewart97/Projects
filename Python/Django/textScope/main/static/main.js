// Updates the name when a file is uploaded
function updateFileName() {
    var fileInput = document.getElementById('file-input');
    var fileName = fileInput.files[0] ? fileInput.files[0].name : 'No file selected';
    document.getElementById('file-name').innerText = fileName;
};


// Hamburger menu in header
document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.querySelector(".menu-toggle");
    const headerLinks = document.querySelector(".header-links");

    if (menuToggle) {
        menuToggle.addEventListener("click", () => {
            headerLinks.classList.toggle("active");
        });
    };
});



// Spinner for file upload
// document.addEventListener("DOMContentLoaded", () => {
//     const uploadForm = document.getElementById("upload-form");
//     const loadingSpinner = document.getElementById("loading-spinner");
//     const messagesContainer = document.getElementById("messages-container");

//     uploadForm.addEventListener("submit", () => {
//         // Show spinner and hide messages
//         loadingSpinner.style.display = "flex";
//         loadingSpinner.style.justifyContent - "center";
//         loadingSpinner.style.alignItems = "center";
//         loadingSpinner.style.flexDirection = "column";
//         loadingSpinner.style.marginTop = "2rem";
//         loadingSpinner.style.marginBottom = "0";
//         messagesContainer.style.display = "none";
//     });

//     // Hide spinner after a delay (if form submission is quick or processed asynch)
//     setTimeout(() => {
//         loadingSpinner.style.display = "none";
//         messagesContainer.style.display = "block";
//     }, 2000);
// });


document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    if (uploadForm) {
        uploadForm.addEventListener("submit", () => {
            const loadingSpinner = document.getElementById("loading-spinner");
            const messagesContainer = document.getElementById("messages-container");
            if (loadingSpinner && messagesContainer) {
                loadingSpinner.style.display = "flex";
                loadingSpinner.style.justifyContent - "center";
                loadingSpinner.style.alignItems = "center";
                loadingSpinner.style.flexDirection = "column";
                loadingSpinner.style.marginTop = "2rem";
                loadingSpinner.style.marginBottom = "0";
                messagesContainer.style.display = "none";
            }
        });
    }
});



// Loader for Data Processing
document.addEventListener("DOMContentLoaded", () => {
    const processDataBtn = document.getElementById("process-data-btn")
    const loader = document.querySelector(".loader");

    processDataBtn.addEventListener("click", () => {
        loader.style.display = "block";
    });
});



// AJAX for Temporary Topic 
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('add-topic-form');
    const topicListContainer  = document.getElementById("topicList");
    const modal = document.getElementById("addTopicModal");
    const openModalBtn = document.getElementById("openModalBtn");
    const closeModalBtn = modal.querySelector(".close");

    // Open the modal when the "Add Temporary Topic" button is clicked
    openModalBtn.addEventListener("click", function () {
        modal.style.display = "block";  // Show the modal
    });

    // Close the modal when the close button (X) is clicked
    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";  // Hide the modal
    });

    // Close the modal if the user clicks outside of the modal content
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";  // Hide the modal
        }
    });

    const url = "/add_temp_topic/";

    // Handle the form submission
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        // Get the form data
        const formData = new FormData(form);

        // Convert FormData to a more readable object for debugging
        const formDataObj = {};
        formData.forEach((value, key) => {
            formDataObj[key] = value;
        });

        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json'
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Dynamically append the new topic checkbox
                    const newTopicHTML = `
                <div class="checkbox-group">
                    <input type="checkbox" id="session_topic_${data.topic.id}" name="selected_topics" value="session_${data.topic.id}">
                    <label for="session_topic_${data.topic.id}">
                        ${data.topic.key} <span style="font-size:0.6rem; font-style:italic;">(Temporary)</span>
                        <span class="tooltip-icon" data-tooltip="${data.topic.values}">?</span>
                    </label>
                </div>`;
                    topicListContainer.insertAdjacentHTML('beforeend', newTopicHTML);

                    // Reset form after success
                    form.reset();
                    modal.style.display = "none";  // Hide modal after successful submission
                } else {
                    alert('Error adding topic: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An unexpected error occurred.');
            });
    });
});



// Search bar functionality for Available Topics
const topicSearch = document.getElementById('topicSearch')
if (topicSearch) {
    topicSearch.addEventListener('keyup', function () {
        const searchValue = this.value.toLowerCase();
        const topics = document.querySelectorAll('#topicList .checkbox-group');
    
        topics.forEach(function (topic) {
            const topicLabel = topic.querySelector('label').innerText.toLowerCase();
            if (topicLabel.includes(searchValue)) {
                topic.style.display = 'block';
            } else {
                topic.style.display = 'none';
            }
        });
    });
};


// Get current page url for share on social buttons
document.addEventListener("DOMContentLoaded", function () {
    const currentURL = encodeURIComponent(window.location.href);
    const pageTitle = encodeURIComponent(document.title);
    const twitterText = "Check out this amazing tool!"

    const twitterBtn = document.getElementById('twitter-share');
    if (twitterBtn) {
        twitterBtn.href = `https://twitter.com/intent/tweet?text=${twitterText}&url=${currentURL}`
    }

    const facebookBtn =document.getElementById('facebook-share');
    if (facebookBtn) {
        facebookBtn.href = `https://www.facebook.com/sharer/sharer.php?u=${currentURL}`
    }

    const linkedinBtn = document.getElementById('linkedin-share');
    if (linkedinBtn) {
        linkedinBtn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${currentURL}`
    }

    const emailBtn = document.getElementById('email-share');
    if (emailBtn) {
        const emailSubject = "Check out this Tool";
        const emailBody = `I found this tool and thought you'd like it: ${window.location.href}`;
        emailBtn.href = `mailto:?subject=${encodeURIComponent(emailSubject)}&body=${encodeURIComponent(emailBody)}`;
    }
});


// Tip Modal
document.addEventListener('DOMContentLoaded', function () {
    // Get the modal and the button that opens it
    var modal = document.getElementById("tip-modal");
    var btn = document.getElementById("tip-jar-btn");
    var cryptoBtn = document.getElementById("crypto-tip-btn"); 
    var supportBtn = document.getElementById("support-site-btn");
    var ctaSupportBtn = document.getElementById("cta-support-site-btn");
    var span = document.getElementById("tipModalClose");

    

    // When the user clicks the tip button, open the modal
    if (btn) {
        btn.onclick = function () {
            modal.style.display = "block";
            console.log("Clicked")
        }
    }

    // When the user clicks the crypto button, open the modal (optional action)
    if (cryptoBtn) {
        cryptoBtn.onclick = function () {
            modal.style.display = "block";
        }
    }

    // When the user clicks the support site button on homepage
    if (supportBtn) {
        supportBtn.onclick = function () {
            modal.style.display = "block";
        }
    }

    // When the user clicks the support site button on cta box on homepage
    if (ctaSupportBtn) {
        ctaSupportBtn.onclick = function () {
            modal.style.display = "block";
        }
    }


    // When the user clicks the close button, close the modal
    if (modal) {
        span.onclick = function () {
            modal.style.display = "none";
        }
    }


    // When the user clicks anywhere outside the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});



// Form Validation for Process Data Button
document.addEventListener("DOMContentLoaded", function () {
    const processButton = document.querySelector('button[name="process_data"]');
    const columnSelect = document.querySelector('select[name="selected_column"]'); // Assuming it's a dropdown
    const topicCheckboxes = document.querySelectorAll('input[name="selected_topics"]');

    function validateForm() {
        const isColumnSelected = columnSelect && columnSelect.value !== "";
        const areTopicsSelected = Array.from(topicCheckboxes).some(checkbox => checkbox.checked);

        if (isColumnSelected && areTopicsSelected) {
            processButton.disabled = false;
        } else {
            processButton.disabled = true;
        }
    }

    // Run validation on change events
    if (columnSelect) {
        columnSelect.addEventListener("change", validateForm);
    }
    topicCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", validateForm);
    });

    // Initial validation
    validateForm();
});


