// When the redirect from field is clicked enable save button and disable delete button
function fromClicked(element) {

    // Enable the save button
    element.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.classList.remove("saved");
    element.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.classList.add("save");

    // Disable the delete button
    element.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.classList.remove("del");
    element.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.classList.add("dis");

}

// When the redirect to field is clicked enable save button and disable delete button
function toClicked(element) {

    // Enable the save button
    element.previousElementSibling.previousElementSibling.classList.remove("saved");
    element.previousElementSibling.previousElementSibling.classList.add("save");

    // Disable the delete button
    element.previousElementSibling.classList.remove("del");
    element.previousElementSibling.classList.add("dis");

}

// When an embedded button is clicked toggle
function embeddedClicked(element) {

    // Toggle the embedded button
    element.classList.toggle("select_no");
    element.classList.toggle("select_yes");

    // Enable the save button
    element.nextElementSibling.nextElementSibling.nextElementSibling.classList.remove("saved");
    element.nextElementSibling.nextElementSibling.nextElementSibling.classList.add("save");

    // Disable the delete button
    element.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.classList.remove("del");
    element.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.classList.add("dis");

}

// When a maintenance button is clicked toggle
function maintClicked(element) {

    // Toggle the maintenance button
    element.classList.toggle("select_no");
    element.classList.toggle("select_yes");

    // Toggle the redirect to field
    element.previousElementSibling.classList.toggle("prod");
    element.previousElementSibling.classList.toggle("maint");

    // Toggle the redirect from field
    element.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.classList.toggle("prod");
    element.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.classList.toggle("maint");

    // Enable the save button
    element.previousElementSibling.previousElementSibling.previousElementSibling.classList.remove("saved");
    element.previousElementSibling.previousElementSibling.previousElementSibling.classList.add("save");

    // Disable the delete button
    element.previousElementSibling.previousElementSibling.classList.remove("del");
    element.previousElementSibling.previousElementSibling.classList.add("dis");

}