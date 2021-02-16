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

const urlParams = new URLSearchParams(window.location.search);
const arg = urlParams.get('gotoChat');
console.log(arg)

if (arg === 'true') {
    openTab(event, 'Chat')
}

function editItinerary() {
    document.getElementById("editItineraryButtons").classList.remove("is-hidden");
    document.getElementById("ItineraryForm").classList.remove("is-hidden");
    document.getElementById("editButton").classList.add("is-hidden");
}

function SaveItinerary() {
    document.getElementById("editItineraryButtons").classList.add("is-hidden");
    document.getElementById("ItineraryForm").classList.add("is-hidden");
    document.getElementById("editButton").classList.remove("is-hidden");
}