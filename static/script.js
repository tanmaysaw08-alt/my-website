document.querySelectorAll("form").forEach(function(form) {
    form.addEventListener("submit", function() {
        const button = form.querySelector("button");
        if (button) {
            button.textContent = "Submitting...";
            button.disabled = true;
        }
    });
});
