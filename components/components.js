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
            }
        });
});
