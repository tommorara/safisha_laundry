// ✅ Automatically set today's date for "Date Received"
document.getElementById('dateReceived').valueAsDate = new Date();

// ✅ Available fabric types in Kenyan Market
const fabricTypes = [
    'Cotton', 'Polyester', 'Denim', 'Silk', 'Linen', 
    'Wool', 'Chiffon', 'Leather', 'Canvas', 'Velvet', 'Other'
];

// ✅ Add new fabric entry
function addFabric() {
    const fabricList = document.getElementById('fabricList');

    const fabricItem = document.createElement('div');
    fabricItem.className = 'fabric-item';

    fabricItem.innerHTML = `
        <select class="fabric-type" required>
            <option value="" disabled selected>Select Fabric Type</option>
            ${fabricTypes.map(type => `<option value="${type}">${type}</option>`).join('')}
        </select>
        <input type="number" class="fabric-quantity" min="1" placeholder="Quantity" required />
        <button type="button" class="remove-fabric-btn" onclick="this.parentNode.remove()">❌</button>
    `;

    fabricList.appendChild(fabricItem);
}

// ✅ Submit order to backend
document.getElementById('createOrderForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const customerName = document.getElementById('customerName').value;
    const contactNumber = document.getElementById('contactNumber').value;
    const dateReceived = document.getElementById('dateReceived').value;
    const dateToBeCollected = document.getElementById('dateToBeCollected').value;
    const notes = document.getElementById('notes').value;

    const fabrics = [];
    document.querySelectorAll('.fabric-item').forEach(item => {
        const type = item.querySelector('.fabric-type').value;
        const quantity = parseInt(item.querySelector('.fabric-quantity').value);
        fabrics.push({ type, quantity });
    });

    if (fabrics.length === 0) {
        alert('Please add at least one fabric.');
        return;
    }

    const newOrder = {
        customer_name: customerName,
        contact_number: contactNumber,
        fabrics,
        total_weight: 0,
        order_received_date: dateReceived,
        due_date: dateToBeCollected,
        notes,
        status: 'pending'
    };

    try {
        const response = await fetch('/add_order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newOrder)
        });

        if (response.ok) {
            alert('Order created successfully!');
            window.location.href = '/pending';
        }
    } catch (error) {
        alert('Error submitting order');
    }
});

