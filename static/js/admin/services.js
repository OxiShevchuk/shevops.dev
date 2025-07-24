const editServiceForm = document.getElementById('edit-service-form');

const editServiceButtons = document.querySelectorAll('.edit-service-btn');
const editServiceId = document.getElementById('edit-service-id');
const editServiceIcon = document.getElementById('edit-service-icon');
const editServiceName = document.getElementById('edit-service-name');
const editServiceDesc = document.getElementById('edit-service-desc');

editServiceButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        editServiceId.value = btn.dataset.id;
        editServiceIcon.value = btn.dataset.icon;
        editServiceName.value = btn.dataset.name;
        editServiceDesc.value = btn.dataset.desc;
        editServiceForm.action = "/editservice/" + editServiceId.value;
    });
});

const deleteServiceForm = document.getElementById('delete-service-form');
const deleteServiceId = document.getElementById('delete-service-id');
const deleteServiceButtons = document.querySelectorAll('.delete-service-btn');

deleteServiceButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        deleteServiceId.value = btn.dataset.id;
        deleteServiceForm.action = "/deleteservice/" + deleteServiceId.value;
    });
});