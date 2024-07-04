document.addEventListener("DOMContentLoaded", function() {
    const addForm = document.getElementById("add-contact-form");
    const addButton = document.querySelector(".add-button");

    addButton.addEventListener("click", function() {
          if (addForm.style.display === "none" || addForm.style.display === "") {
                addForm.style.display = "block";
                addButton.style.display = "none";

            } else {
                addForm.style.display = "none";
                addButton.textContent = "DODAJ NOWY KONTAKT";
            }
    });
});
