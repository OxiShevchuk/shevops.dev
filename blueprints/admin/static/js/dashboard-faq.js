const editFaqForm = document.getElementById('edit-faq-form');

const editFaqButtons = document.querySelectorAll('.edit-faq-btn');
const editFaqId = document.getElementById('edit-faq-id');
const editFaqTitle = document.getElementById('edit-faq-title');
const editFaqDesc = document.getElementById('edit-faq-desc');


editFaqButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        editFaqId.value = btn.dataset.id;
        editFaqTitle.value = btn.dataset.title;
        editFaqDesc.value = btn.dataset.desc;
        editFaqForm.action = "/admin/editfaq/" + editFaqId.value;
    });
});

const deleteFaqForm = document.getElementById('delete-faq-form');
const deleteFaqId = document.getElementById('delete-faq-id');
const deleteFaqButtons = document.querySelectorAll('.delete-faq-btn');

deleteFaqButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        // console.log(btn.dataset.id);
        deleteFaqId.value = btn.dataset.id;
        deleteFaqForm.action = "/admin/deletefaq/" + deleteFaqId.value;
    });
});



const orderFaqButtons = document.querySelectorAll('.table-col-icons button');
orderFaqButtons.forEach(btn => {
    btn.addEventListener('click', async function () {
        const orderFaqId = btn.dataset.id;
        const orderFaqDirection = btn.dataset.direction;
        console.log(orderFaqId, orderFaqDirection);

        try {
            const response = await fetch('/admin/reorderfaq', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: orderFaqId, direction: orderFaqDirection})
            });
            const result = await response.json();
            if (result.success) {
                // Reload page or table to show updated order
                location.reload();
            } else if (result.message) {
                alert(result.message);
            }
        } catch (err) {
            console.error('Error reordering faq:', err);
        }
    });
});