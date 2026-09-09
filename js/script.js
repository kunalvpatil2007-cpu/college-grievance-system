// ============================================
// SMART COLLEGE GRIEVANCE MANAGEMENT SYSTEM
// Common JavaScript
// ============================================


// ============================================
// PAGE LOAD
// ============================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Smart College Grievance System Loaded");

    initializeNavbar();

    initializeAlerts();

    initializeScrollAnimation();

});


// ============================================
// NAVBAR SCROLL EFFECT
// ============================================

function initializeNavbar() {

    const navbar = document.querySelector(".navbar");

    if (!navbar) {
        return;
    }

    window.addEventListener("scroll", function () {

        if (window.scrollY > 50) {

            navbar.classList.add("navbar-scrolled");

        } else {

            navbar.classList.remove("navbar-scrolled");

        }

    });

}


// ============================================
// AUTO HIDE ALERTS
// ============================================

function initializeAlerts() {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            if (typeof bootstrap !== "undefined") {

                const alertInstance =
                    bootstrap.Alert.getOrCreateInstance(alert);

                alertInstance.close();

            }

        }, 5000);

    });

}


// ============================================
// SCROLL ANIMATION
// ============================================

function initializeScrollAnimation() {

    const elements =
        document.querySelectorAll(
            ".feature-card, .step-card, .hero-card"
        );

    if (elements.length === 0) {
        return;
    }

    const observer =
        new IntersectionObserver(
            function (entries) {

                entries.forEach(function (entry) {

                    if (entry.isIntersecting) {

                        entry.target.classList.add(
                            "show-animation"
                        );

                    }

                });

            },
            {
                threshold: 0.15
            }
        );


    elements.forEach(function (element) {

        observer.observe(element);

    });

}


// ============================================
// CONFIRM DELETE
// ============================================

function confirmDelete(message) {

    if (!message) {

        message =
            "Are you sure you want to delete this record?";

    }

    return confirm(message);

}


// ============================================
// CONFIRM ACTION
// ============================================

function confirmAction(message) {

    if (!message) {

        message =
            "Are you sure you want to perform this action?";

    }

    return confirm(message);

}


// ============================================
// SHOW LOADING BUTTON
// ============================================

function showLoading(button, text = "Processing...") {

    if (!button) {
        return;
    }

    button.disabled = true;

    button.dataset.originalText =
        button.innerHTML;

    button.innerHTML = `
        <span
            class="spinner-border spinner-border-sm me-2"
            role="status"
            aria-hidden="true">
        </span>
        ${text}
    `;

}


// ============================================
// RESET BUTTON
// ============================================

function resetButton(button) {

    if (!button) {
        return;
    }

    button.disabled = false;

    if (button.dataset.originalText) {

        button.innerHTML =
            button.dataset.originalText;

    }

}


// ============================================
// CHARACTER COUNTER
// ============================================

function setupCharacterCounter(
    textareaId,
    counterId,
    maxLength
) {

    const textarea =
        document.getElementById(textareaId);

    const counter =
        document.getElementById(counterId);


    if (!textarea || !counter) {
        return;
    }


    function updateCounter() {

        const currentLength =
            textarea.value.length;

        counter.innerText =
            currentLength + " / " + maxLength;


        if (currentLength >= maxLength) {

            counter.classList.add("text-danger");

        } else {

            counter.classList.remove("text-danger");

        }

    }


    textarea.addEventListener(
        "input",
        updateCounter
    );

    updateCounter();

}


// ============================================
// EMAIL VALIDATION
// ============================================

function validateEmail(email) {

    const pattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return pattern.test(email);

}


// ============================================
// PASSWORD STRENGTH
// ============================================

function checkPasswordStrength(password) {

    let strength = 0;


    if (password.length >= 6) {

        strength++;

    }


    if (password.length >= 10) {

        strength++;

    }


    if (/[A-Z]/.test(password)) {

        strength++;

    }


    if (/[a-z]/.test(password)) {

        strength++;

    }


    if (/[0-9]/.test(password)) {

        strength++;

    }


    if (/[^A-Za-z0-9]/.test(password)) {

        strength++;

    }


    return strength;

}


// ============================================
// SEARCH TABLE
// ============================================

function searchTable(
    inputId,
    tableId
) {

    const input =
        document.getElementById(inputId);

    const table =
        document.getElementById(tableId);


    if (!input || !table) {
        return;
    }


    input.addEventListener(
        "keyup",
        function () {

            const searchValue =
                input.value.toLowerCase();

            const rows =
                table
                .getElementsByTagName("tr");


            for (
                let i = 1;
                i < rows.length;
                i++
            ) {

                const rowText =
                    rows[i].innerText.toLowerCase();


                if (
                    rowText.includes(searchValue)
                ) {

                    rows[i].style.display = "";

                } else {

                    rows[i].style.display = "none";

                }

            }

        }
    );

}


// ============================================
// FILTER BY STATUS
// ============================================

function filterByStatus(
    selectId,
    tableId
) {

    const select =
        document.getElementById(selectId);

    const table =
        document.getElementById(tableId);


    if (!select || !table) {
        return;
    }


    select.addEventListener(
        "change",
        function () {

            const selectedStatus =
                select.value.toLowerCase();

            const rows =
                table
                .getElementsByTagName("tr");


            for (
                let i = 1;
                i < rows.length;
                i++
            ) {

                const statusCell =
                    rows[i].querySelector(
                        ".complaint-status"
                    );


                if (!statusCell) {
                    continue;
                }


                const status =
                    statusCell.innerText.toLowerCase();


                if (
                    selectedStatus === "" ||
                    status === selectedStatus
                ) {

                    rows[i].style.display = "";

                } else {

                    rows[i].style.display = "none";

                }

            }

        }
    );

}


// ============================================
// GO TO TOP
// ============================================

function scrollToTop() {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}


// ============================================
// CURRENT YEAR
// ============================================

function setCurrentYear(elementId) {

    const element =
        document.getElementById(elementId);

    if (!element) {
        return;
    }

    element.innerText =
        new Date().getFullYear();

}


// ============================================
// NOTIFICATION TOAST
// ============================================

function showToast(
    message,
    type = "success"
) {

    const toastContainer =
        document.getElementById(
            "toastContainer"
        );


    if (!toastContainer) {
        return;
    }


    const toast =
        document.createElement("div");


    toast.className =
        `toast align-items-center text-bg-${type} border-0`;


    toast.setAttribute(
        "role",
        "alert"
    );


    toast.innerHTML = `

        <div class="d-flex">

            <div class="toast-body">

                ${message}

            </div>

            <button
                type="button"
                class="btn-close btn-close-white
                       me-2 m-auto"
                data-bs-dismiss="toast">
            </button>

        </div>

    `;


    toastContainer.appendChild(toast);


    if (typeof bootstrap !== "undefined") {

        const toastInstance =
            new bootstrap.Toast(toast);

        toastInstance.show();

    }


    setTimeout(function () {

        toast.remove();

    }, 5000);

}


// ============================================
// FILE SIZE VALIDATION
// ============================================

function validateFileSize(
    fileInputId,
    maxSizeMB = 5
) {

    const input =
        document.getElementById(
            fileInputId
        );


    if (
        !input ||
        !input.files ||
        input.files.length === 0
    ) {

        return true;

    }


    const file =
        input.files[0];


    const maxSize =
        maxSizeMB * 1024 * 1024;


    if (file.size > maxSize) {

        alert(
            `File size must be less than ${maxSizeMB} MB.`
        );

        input.value = "";

        return false;

    }


    return true;

}


// ============================================
// FILE TYPE VALIDATION
// ============================================

function validateFileType(
    fileInputId,
    allowedTypes
) {

    const input =
        document.getElementById(
            fileInputId
        );


    if (
        !input ||
        !input.files ||
        input.files.length === 0
    ) {

        return true;

    }


    const file =
        input.files[0];


    const extension =
        file.name
        .split(".")
        .pop()
        .toLowerCase();


    if (
        !allowedTypes
        .map(type => type.toLowerCase())
        .includes(extension)
    ) {

        alert(
            "Invalid file type. Allowed: " +
            allowedTypes.join(", ")
        );

        input.value = "";

        return false;

    }


    return true;

}


// ============================================
// LOGOUT CONFIRMATION
// ============================================

function confirmLogout() {

    return confirm(
        "Are you sure you want to logout?"
    );

}


// ============================================
// PRINT PAGE
// ============================================

function printPage() {

    window.print();

}
