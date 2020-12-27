function toggleEdit() {
    var editDisplay = document.getElementById("editform");
    var timelineDisplay = document.getElementById("timeline");
    if (editDisplay.style.display === "none") {
        editDisplay.style.display = "block";
        //Toggle edit/save button (uhoh not work)
        document.getElementById("toggleButton").value = '<i class="fas fa-check"></i>&ensp;Save';
    } else {
        editDisplay.style.display = "none";
        //Toggle edit/save button
        document.getElementById("toggleButton").value = '<i class="fas fa-edit"></i>&ensp;Edit';
    }
    //there was an attempt at dynamic prefilled form fields
    document.getElementById("input_dateTime").value = document.getElementById("dateTime").value;
}