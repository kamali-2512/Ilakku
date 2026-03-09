document.addEventListener("DOMContentLoaded", function () {
    // Load Header
    fetch("components/header.html")
        .then(response => response.text())
        .then(data => {
            const headerPlaceholder = document.getElementById("header-placeholder");
            if (headerPlaceholder) {
                headerPlaceholder.innerHTML = data;

                // Highlight active link
                let path = window.location.pathname;
                let page = path.split("/").pop();
                if (page === "") {
                    page = "home.html";
                }

                let links = headerPlaceholder.querySelectorAll(".nav-link");
                links.forEach(link => {
                    if (link.getAttribute("href") === page) {
                        link.parentElement.classList.add("active");
                    } else {
                        // Remove active just in case
                        link.parentElement.classList.remove("active");
                    }
                });
            }
        });

    // Load Footer
    fetch("components/footer.html")
        .then(response => response.text())
        .then(data => {
            const footerPlaceholder = document.getElementById("footer-placeholder");
            if (footerPlaceholder) {
                footerPlaceholder.innerHTML = data;
                setupSubscriptionForm();
            }
        });
});

function setupSubscriptionForm() {
    const form = document.getElementById('subscribeForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Use FormData for multipart/form-data support in FastAPI
            const formData = new FormData(this);

            fetch('http://localhost:8000/api/subscribe', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Thank you for subscribing!');
                        form.reset();
                    } else {
                        alert('Submission failed: ' + (data.detail || 'Unknown error'));
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Could not connect to the server. Please check if the backend is running at http://localhost:8000');
                });
        });
    }
}

