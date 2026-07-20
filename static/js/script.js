let selectedSeat = null;

document.querySelectorAll(".seat-btn").forEach(button => {

    button.addEventListener("click", function () {

        document.querySelectorAll(".seat-btn").forEach(btn => {

            btn.classList.remove("btn-primary");
            btn.classList.add("btn-outline-success");

        });

        this.classList.remove("btn-outline-success");
        this.classList.add("btn-primary");

        selectedSeat = this.dataset.seat;

    });

});

document.getElementById("continueBtn")?.addEventListener("click", function () {

    if (!selectedSeat) {

        alert("Please select a seat.");

        return;

    }

    alert("Selected Seat: " + selectedSeat);

});