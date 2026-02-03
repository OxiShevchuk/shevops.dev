const editReasonForm = document.getElementById('edit-reason-form');

const editReasonButtons = document.querySelectorAll('.edit-reason-btn');
const editReasonId = document.getElementById('edit-reason-id');
const editReasonTitle = document.getElementById('edit-reason-title');
const editReasonDesc = document.getElementById('edit-reason-desc');


editReasonButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        editReasonId.value = btn.dataset.id;
        editReasonTitle.value = btn.dataset.title;
        editReasonDesc.value = btn.dataset.desc;
        editReasonForm.action = "/admin/edit-why-choose-me/" + editReasonId.value;
    });
});

const deleteReasonForm = document.getElementById('delete-reason-form');
const deleteReasonId = document.getElementById('delete-reason-id');
const deleteReasonButtons = document.querySelectorAll('.delete-reason-btn');

deleteReasonButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        // console.log(btn.dataset.id);
        deleteReasonId.value = btn.dataset.id;
        deleteReasonForm.action = "/admin/delete-why-choose-me/" + deleteReasonId.value;
    });
});



const orderReasonButtons = document.querySelectorAll('.table-col-icons button');
orderReasonButtons.forEach(btn => {
    btn.addEventListener('click', async function () {
        const orderReasonId = btn.dataset.id;
        const orderReasonDirection = btn.dataset.direction;
        console.log(orderReasonId, orderReasonDirection);

        try {
            const response = await fetch('/admin/reorderwhychooseme', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: orderReasonId, direction: orderReasonDirection})
            });
            const result = await response.json();
            if (result.success) {
                // Reload page or table to show updated order
                location.reload();
            } else if (result.message) {
                alert(result.message);
            }
        } catch (err) {
            console.error('Error reordering reason:', err);
        }
    });
});