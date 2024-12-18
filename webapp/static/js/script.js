document.addEventListener('DOMContentLoaded', function() {
    const filterToggleBtn = document.getElementById('filter-toggle-btn');
    const filterForm = document.getElementById('filter-form');

    filterToggleBtn.addEventListener('click', function() {
        if (filterForm.style.display === 'none' || filterForm.style.display === '') {
            filterForm.style.display = 'block';
        } else {
            filterForm.style.display = 'none';
        }
    });
});



document.addEventListener('DOMContentLoaded', function () {
    // Get the flash message container
    const flashMessage = document.getElementById('flash-messages');

    // Check if flash message exists on the page
    if (flashMessage) {
        // Set the timeout to automatically hide the flash message after 3-5 seconds
        setTimeout(function () {
            flashMessage.classList.add('hidden'); // Add hidden class to trigger fade-out
        }, 3000); // Change the duration (3000ms = 3 seconds) as desired

        // Optionally, make the flash message clickable to manually dismiss it
        flashMessage.addEventListener('click', function () {
            flashMessage.classList.add('hidden');
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const taskProjectSelect = document.getElementById('project');
    const selectedProjectId = "{{ task.project.id if task.project else '' }}";

    if (taskProjectSelect && selectedProjectId) {
        taskProjectSelect.value = selectedProjectId;
    }
});


document.addEventListener('DOMContentLoaded', function () {
    // Get the logout link element
    const logoutLink = document.getElementById('logout-link');

    // Attach a click event listener
    logoutLink.addEventListener('click', function(event) {
        // Ask for confirmation before logging out
        const userConfirmed = confirm("Are you sure you want to log out?");
        
        // If the user cancels the action, prevent the logout
        if (!userConfirmed) {
            event.preventDefault();
        }
    });
});



    /* Toggle the visibility of the password change form
    document.getElementById('toggle-password-form').addEventListener('click', function() {
        var form = document.getElementById('password-form');
        if (form.style.display === 'none' || form.style.display === '') {
            form.style.display = 'block';
            this.textContent = 'Hide Change Password Form';
        } else {
            form.style.display = 'none';
            this.textContent = 'Show Change Password Form';
        }
    }); */ 

    // Toggle the visibility of the profile edit form
    document.getElementById('toggle-profile-form').addEventListener('click', function() {
        var form = document.getElementById('profile-form');
        if (form.style.display === 'none' || form.style.display === '') {
            form.style.display = 'block';
            this.textContent = 'Hide Edit Profile Form';
        } else {
            form.style.display = 'none';
            this.textContent = 'Show Edit Profile Form';
        }
    });
