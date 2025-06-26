document.addEventListener('DOMContentLoaded', function() {
    const filterToggleButton = document.getElementById('filter-toggle-btn');
    const filterForm = document.getElementById('filter-form');

    if (filterToggleButton && filterForm) {
        filterToggleButton.addEventListener('click', function () {
            if (filterForm.style.display === 'none' || !filterForm.style.display) {
                filterForm.style.display = 'block'; 
            } else {
                filterForm.style.display = 'none'; 
            }
        });
    }
});




    // Timeout Notifications

document.addEventListener('DOMContentLoaded', function () {
    const flashMessage = document.getElementById('flash-messages');

    if (flashMessage) {

        setTimeout(function () {
            flashMessage.classList.add('hidden'); 
        }, 5000); 

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
    const logoutLink = document.getElementById('logout-link');

    logoutLink.addEventListener('click', function(event) {
        // Ask for confirmation before logging out
        const userConfirmed = confirm("Are you sure you want to log out?");
        
        // If the user cancels the action, prevent the logout
        if (!userConfirmed) {
            event.preventDefault();
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
  const clearFilterBtn = document.getElementById('clear-filter');
  const filterForm = document.getElementById('filter-form');

  clearFilterBtn.addEventListener('click', () => {
    filterForm.querySelectorAll('select').forEach(select => {
      select.value = "";
    });
    filterForm.querySelectorAll('input[type="text"]').forEach(input => {
      input.value = "";
    });
    
    filterForm.submit();
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
        event.preventDefault();  
      }
    });
  });
});
