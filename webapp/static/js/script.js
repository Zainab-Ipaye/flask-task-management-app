    // Toggle the visibility of the filter button
document.addEventListener('DOMContentLoaded', function() {
    const filterToggleButton = document.getElementById('filter-toggle-btn');
    const filterForm = document.getElementById('filter-form');

    if (filterToggleButton && filterForm) {
        filterToggleButton.addEventListener('click', function () {
            // Toggle the visibility of the filter form
            if (filterForm.style.display === 'none' || !filterForm.style.display) {
                filterForm.style.display = 'block'; // Show the form
            } else {
                filterForm.style.display = 'none'; // Hide the form
            }
        });
    }
});




    // Timeout Notifications

document.addEventListener('DOMContentLoaded', function () {
    // Get the flash message container
    const flashMessage = document.getElementById('flash-messages');

    // Check if flash message exists on the page
    if (flashMessage) {
        // Set the timeout to automatically hide the flash message after 3-5 seconds
        setTimeout(function () {
            flashMessage.classList.add('hidden'); // Add hidden class to trigger fade-out
        }, 5000); // Change the duration (3000ms = 3 seconds) as desired

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



document.addEventListener('DOMContentLoaded', () => {
    const toggleLink = document.getElementById('toggle-profile-form-link');
    const profileForm = document.getElementById('profile-form');

    toggleLink.addEventListener('click', (e) => {
        e.preventDefault();
        if (profileForm.style.display === 'none' || profileForm.style.display === '') {
            profileForm.style.display = 'block';
            toggleLink.textContent = 'Hide Edit Profile Form';
        } else {
            profileForm.style.display = 'none';
            toggleLink.textContent = 'Show Edit Profile Form';
        }
    });

    // Confirmation before submitting update form
    const updateForm = document.getElementById('profile-update-form');
    updateForm.addEventListener('submit', (e) => {
        if (!confirm('Are you sure you want to update your profile?')) {
            e.preventDefault();
        }
    });
});




document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-delete').forEach(button => {
    button.addEventListener('click', function(event) {
      if (!confirm('Are you sure you want to delete this task?')) {
        event.preventDefault();  // Prevent form submission if cancelled
      }
    });
  });
});
