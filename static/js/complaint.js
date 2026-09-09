/* =========================================================
   SMART COLLEGE GRIEVANCE MANAGEMENT SYSTEM
   Complaint JavaScript
   R. C. Patel College of Engineering and Polytechnic
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* -----------------------------------------------------
       Complaint Description Character Counter
    ----------------------------------------------------- */

    const description = document.getElementById("description");
    const charCount = document.getElementById("charCount");

    if (description && charCount) {

        function updateCharacterCount() {
            const length = description.value.length;
            charCount.textContent = length + " / 1000";

            if (length > 900) {
                charCount.classList.add("text-danger");
                charCount.classList.remove("text-muted");
            } else {
                charCount.classList.remove("text-danger");
                charCount.classList.add("text-muted");
            }
        }

        description.addEventListener("input", updateCharacterCount);
        updateCharacterCount();
    }


    /* -----------------------------------------------------
       File Upload Validation
    ----------------------------------------------------- */

    const attachment = document.getElementById("attachment");

    if (attachment) {

        attachment.addEventListener("change", function () {

            const file = this.files[0];

            if (!file) {
                return;
            }

            const maxSize = 5 * 1024 * 1024;

            const allowedTypes = [
                "image/jpeg",
                "image/png",
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ];

            if (file.size > maxSize) {

                alert("File size must be less than 5 MB.");

                this.value = "";
                return;
            }

            if (!allowedTypes.includes(file.type)) {

                alert(
                    "Invalid file type.\n\n" +
                    "Allowed: JPG, PNG, PDF, DOC and DOCX"
                );

                this.value = "";
                return;
            }

            console.log("File selected:", file.name);
        });
    }


    /* -----------------------------------------------------
       Complaint Form Validation
    ----------------------------------------------------- */

    const complaintForm = document.getElementById("complaintForm");

    if (complaintForm) {

        complaintForm.addEventListener("submit", function (event) {

            const title = document.getElementById("title");
            const category = document.getElementById("category");
            const priority = document.getElementById("priority");
            const desc = document.getElementById("description");
            const confirmation = document.getElementById("confirmation");

            let valid = true;

            if (title && title.value.trim().length < 5) {

                alert("Complaint title must contain at least 5 characters.");
                title.focus();

                event.preventDefault();
                return;
            }

            if (category && category.value === "") {

                alert("Please select a complaint category.");
                category.focus();

                event.preventDefault();
                return;
            }

            if (priority && priority.value === "") {

                alert("Please select complaint priority.");
                priority.focus();

                event.preventDefault();
                return;
            }

            if (desc && desc.value.trim().length < 10) {

                alert("Complaint description must contain at least 10 characters.");
                desc.focus();

                event.preventDefault();
                return;
            }

            if (desc && desc.value.length > 1000) {

                alert("Description cannot exceed 1000 characters.");
                desc.focus();

                event.preventDefault();
                return;
            }

            if (confirmation && !confirmation.checked) {

                alert("Please confirm that the information provided is correct.");
                confirmation.focus();

                event.preventDefault();
                return;
            }

            if (valid) {

                const submitButton =
                    complaintForm.querySelector('button[type="submit"]');

                if (submitButton) {

                    submitButton.disabled = true;

                    submitButton.innerHTML =
                        '<span class="spinner-border spinner-border-sm me-2"></span>' +
                        'Submitting...';
                }
            }
        });
    }


    /* -----------------------------------------------------
       Complaint Search
    ----------------------------------------------------- */

    const complaintSearch = document.getElementById("complaintSearch");

    if (complaintSearch) {

        complaintSearch.addEventListener("input", function () {

            const searchValue = this.value.toLowerCase().trim();

            const rows = document.querySelectorAll(
                "#complaintsTable tbody tr"
            );

            rows.forEach(function (row) {

                const text = row.textContent.toLowerCase();

                if (text.includes(searchValue)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }

            });
        });
    }


    /* -----------------------------------------------------
       Complaint Status Filter
    ----------------------------------------------------- */

    const statusFilter = document.getElementById("statusFilter");

    if (statusFilter) {

        statusFilter.addEventListener("change", function () {

            const selectedStatus = this.value.toLowerCase();

            const rows = document.querySelectorAll(
                "#complaintsTable tbody tr"
            );

            rows.forEach(function (row) {

                if (selectedStatus === "") {

                    row.style.display = "";

                    return;
                }

                const rowText = row.textContent.toLowerCase();

                if (rowText.includes(selectedStatus)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }

            });
        });
    }


    /* -----------------------------------------------------
       Complaint Priority Filter
    ----------------------------------------------------- */

    const priorityFilter = document.getElementById("priorityFilter");

    if (priorityFilter) {

        priorityFilter.addEventListener("change", function () {

            const selectedPriority = this.value.toLowerCase();

            const rows = document.querySelectorAll(
                "#complaintsTable tbody tr"
            );

            rows.forEach(function (row) {

                if (selectedPriority === "") {

                    row.style.display = "";

                    return;
                }

                const rowText = row.textContent.toLowerCase();

                if (rowText.includes(selectedPriority)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }

            });
        });
    }


    /* -----------------------------------------------------
       Reset Complaint Filters
    ----------------------------------------------------- */

    const resetFilters = document.getElementById("resetFilters");

    if (resetFilters) {

        resetFilters.addEventListener("click", function () {

            if (complaintSearch) {
                complaintSearch.value = "";
            }

            if (statusFilter) {
                statusFilter.value = "";
            }

            if (priorityFilter) {
                priorityFilter.value = "";
            }

            const categoryFilter =
                document.getElementById("categoryFilter");

            if (categoryFilter) {
                categoryFilter.value = "";
            }

            const departmentFilter =
                document.getElementById("departmentFilter");

            if (departmentFilter) {
                departmentFilter.value = "";
            }

            const rows = document.querySelectorAll(
                "#complaintsTable tbody tr"
            );

            rows.forEach(function (row) {
                row.style.display = "";
            });

        });
    }


    /* -----------------------------------------------------
       Complaint Action Confirmation
    ----------------------------------------------------- */

    window.confirmComplaintAction = function (message) {

        if (confirm(message || "Are you sure you want to continue?")) {
            return true;
        }

        return false;
    };


    /* -----------------------------------------------------
       View Complaint Details
    ----------------------------------------------------- */

    window.viewComplaint = function (
        id,
        title,
        category,
        priority,
        status,
        description
    ) {

        const modalTitle =
            document.getElementById("modalComplaintTitle");

        const modalCategory =
            document.getElementById("modalComplaintCategory");

        const modalPriority =
            document.getElementById("modalComplaintPriority");

        const modalStatus =
            document.getElementById("modalComplaintStatus");

        const modalDescription =
            document.getElementById("modalComplaintDescription");

        if (modalTitle) {
            modalTitle.textContent = title;
        }

        if (modalCategory) {
            modalCategory.textContent = category;
        }

        if (modalPriority) {
            modalPriority.textContent = priority;
        }

        if (modalStatus) {
            modalStatus.textContent = status;
        }

        if (modalDescription) {
            modalDescription.textContent = description;
        }

    };


    /* -----------------------------------------------------
       Complaint Status Color
    ----------------------------------------------------- */

    window.getStatusClass = function (status) {

        if (!status) {
            return "status-pending";
        }

        const value = status.toLowerCase();

        switch (value) {

            case "pending":
                return "status-pending";

            case "in progress":
                return "status-progress";

            case "resolved":
                return "status-resolved";

            case "rejected":
                return "status-rejected";

            default:
                return "status-pending";
        }
    };


    /* -----------------------------------------------------
       Complaint Priority Color
    ----------------------------------------------------- */

    window.getPriorityClass = function (priority) {

        if (!priority) {
            return "priority-medium";
        }

        const value = priority.toLowerCase();

        switch (value) {

            case "low":
                return "priority-low";

            case "medium":
                return "priority-medium";

            case "high":
                return "priority-high";

            case "critical":
                return "priority-critical";

            default:
                return "priority-medium";
        }
    };


    /* -----------------------------------------------------
       Faculty / HOD Status Update UI
    ----------------------------------------------------- */

    window.updateStatusPreview = function (selectElement) {

        const status = selectElement.value;

        const parent = selectElement.closest(".status-container");

        if (!parent) {
            return;
        }

        const badge = parent.querySelector(".status-badge");

        if (!badge) {
            return;
        }

        badge.className = "status-badge";

        const statusClass = getStatusClass(status);

        badge.classList.add(statusClass);

        badge.textContent = status;
    };


    /* -----------------------------------------------------
       Prevent Multiple Form Submission
    ----------------------------------------------------- */

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButtons =
                form.querySelectorAll('button[type="submit"]');

            submitButtons.forEach(function (button) {

                if (!button.dataset.allowMultiple) {

                    setTimeout(function () {

                        button.disabled = true;

                    }, 100);

                }

            });

        });

    });


    /* -----------------------------------------------------
       Auto Hide Success Messages
    ----------------------------------------------------- */

    const alerts = document.querySelectorAll(
        ".alert-success, .alert-info"
    );

    alerts.forEach(function (alertBox) {

        setTimeout(function () {

            if (alertBox && alertBox.parentNode) {

                alertBox.style.transition = "opacity 0.5s ease";
                alertBox.style.opacity = "0";

                setTimeout(function () {
                    alertBox.remove();
                }, 500);

            }

        }, 5000);

    });


    /* -----------------------------------------------------
       Console Information
    ----------------------------------------------------- */

    console.log(
        "Smart College Grievance System - Complaint JS Loaded"
    );

});
