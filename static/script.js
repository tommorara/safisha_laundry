document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('orderForm').addEventListener('submit', async (event) => {
        event.preventDefault();

        const customerName = document.getElementById('customerName').value;
        const contactNumber = document.getElementById('contactNumber').value;
        const totalWeight = parseFloat(document.getElementById('totalWeight').value) || 0;
        const orderReceivedDate = document.getElementById('orderReceivedDate').value;
        const dueDate = document.getElementById('dueDate').value;
        const notes = document.getElementById('notes').value;

        const fabrics = [];
        document.querySelectorAll('.fabric-item').forEach(item => {
            const type = item.querySelector('select').value;
            const quantity = parseInt(item.querySelector('input').value) || 0;
            fabrics.push({ type, quantity });
        });

        const newOrder = {
            customer_name: customerName,
            contact_number: contactNumber,
            fabrics: fabrics,
            total_weight: totalWeight,
            order_received_date: orderReceivedDate,
            due_date: dueDate,
            notes: notes
        };

        const response = await fetch('/add_order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newOrder)
        });

        if (response.ok) {
            loadOrders();
            document.getElementById('orderForm').reset();
            document.getElementById('fabricList').innerHTML = '';
        }
    });

    async function loadOrders() {
        const response = await fetch('/get_orders');
        const orders = await response.json();

        const orderList = document.getElementById('orderList');
        orderList.innerHTML = orders.map(order => `
            <div>
                <strong>${order.customer_name}</strong> (${order.contact_number})<br>
                Fabrics: ${order.fabrics.map(f => `${f.quantity} x ${f.type}`).join(', ')}<br>
                Total Weight: ${order.total_weight.toFixed(2)} kg<br>
                Status: ${order.status}
            </div>
        `).join('');
    }

    loadOrders();
});

function addFabric() {
    const fabricList = document.getElementById('fabricList');
    const fabricItem = document.createElement('div');
    fabricItem.className = 'fabric-item';
    fabricItem.innerHTML = `
        <select>
            <option value="Shirts">Shirts</option>
            <option value="Trousers">Trousers</option>
            <option value="Jackets">Jackets</option>
            <option value="Duvets">Duvets</option>
            <option value="Others">Others</option>
        </select>
        <input type="number" placeholder="Qty" min="1" />
        <button type="button" onclick="this.parentNode.remove()">❌</button>
    `;
    fabricList.appendChild(fabricItem);
}

