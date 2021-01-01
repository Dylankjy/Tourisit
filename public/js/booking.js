function openTab(evt, tabName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("content-tab");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" is-active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " is-active";
}

function editItinerary() {
    document.getElementById("editItineraryButtons").classList.remove("is-hidden");
    document.getElementById("editButton").classList.add("is-hidden");
}

function SaveItinerary() {
    document.getElementById("editItineraryButtons").classList.add("is-hidden");
    document.getElementById("editButton").classList.remove("is-hidden");
}

function editCost() {
    document.getElementById("Cost_EditButton").classList.add("is-hidden");
    document.getElementById("Cost_SaveButton").classList.remove("is-hidden");
    document.getElementById("editCostForm").classList.remove("is-hidden");
}

function SaveCost() {
    document.getElementById("Cost_EditButton").classList.remove("is-hidden");
    document.getElementById("Cost_SaveButton").classList.add("is-hidden");
    document.getElementById("editCostForm").classList.add("is-hidden");
}