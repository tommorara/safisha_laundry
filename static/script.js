function addFabric() {
    const fabricList = document.getElementById('fabricList');
    const div = document.createElement('div');
    div.innerHTML = `
        <select required>
            <option value="Cotton">Cotton</option>
            <option value="Denim">Denim</option>
            <option value="Silk">Silk</option>
        </select>
        <input type="number" placeholder="Quantity" required>
        <button type="button" onclick="this.parentNode.remove()">❌</button>
    `;
    fabricList.appendChild(div);
}

document.getElementById('createOrderForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fabrics = [];
    document.querySelectorAll('#fabricList > div').forEach(div => {
        const type = div.querySelector('select').value;
        const quantity = parseInt(div.querySelector('input').value);
        fabrics.push({ type, quantity });
    });

    const payload = {
        customer_name: document.getElementById('customerName').value,
        contact_number: document.getElementById('contactNumber').value,
        order_received_date: document.getElementById('dateReceived').value,
        due_date: document.getElementById('dateToBeCollected').value,
        notes: document.getElementById('notes').value,
        fabrics: fabrics
    };

    const res = await fetch('/add_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert("Order created!");
        window.location.href = "/pending";
    } else {
        alert("Failed to create order");
    }
});

