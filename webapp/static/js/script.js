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
    const taskProjectSelect = document.getElementById('project');
    const selectedProjectId = "{{ task.project.id if task.project else '' }}";

    if (taskProjectSelect && selectedProjectId) {
        taskProjectSelect.value = selectedProjectId;
    }
});
