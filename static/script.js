let fabricTypes = [];

// 🔄 Fetch fabric types from backend on load
async function fetchFabricTypes() {
    try {
        const res = await fetch('/fabric_types');
        fabricTypes = await res.json();
    } catch (error) {
        console.error("⚠️ Failed to load fabric types:", error);
        fabricTypes = ['Others']; // fallback
    }
}

function addFabric() {
    const fabricList = document.getElementById('fabricList');
    const div = document.createElement('div');
    div.className = 'fabric-entry';

    // Fabric type dropdown
    const select = document.createElement('select');
    select.name = 'fabricType';
    select.required = true;
    fabricTypes.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        select.appendChild(option);
    });

    // Quantity input
    const qtyInput = document.createElement('input');
    qtyInput.type = 'number';
    qtyInput.name = 'fabricQty';
    qtyInput.min = 1;
    qtyInput.required = true;
    qtyInput.placeholder = 'Quantity';

    // Remove button
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.textContent = '❌';
    removeBtn.onclick = () => div.remove();

    // Combine and add to DOM
    div.appendChild(select);
    div.appendChild(qtyInput);
    div.appendChild(removeBtn);
    fabricList.appendChild(div);
}

// 🧾 Form submission handler
document.getElementById('createOrderForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fabricDivs = document.querySelectorAll('#fabricList > div');
    if (fabricDivs.length === 0) {
        alert("Please add at least one fabric.");
        return;
    }

    const fabrics = [];
    fabricDivs.forEach(div => {
        const type = div.querySelector('select')?.value;
        const quantity = parseInt(div.querySelector('input')?.value);
        if (type && !isNaN(quantity) && quantity > 0) {
            fabrics.push({ type, quantity });
        }
    });

    const payload = {
        customer_name: document.getElementById('customerName')?.value || "",
        contact_number: document.getElementById('contactNumber')?.value || "",
        total_weight: parseFloat(document.getElementById('totalWeight')?.value || 0).toFixed(2),
        order_received_date: document.getElementById('dateReceived')?.value,
        due_date: document.getElementById('dateToBeCollected')?.value,
        notes: document.getElementById('notes')?.value || "",
        fabrics: fabrics
    };

    console.log("📤 Submitting order:", JSON.stringify(payload, null, 2));

    try {
        const res = await fetch('/add_order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            const data = await res.json();
            alert(`✅ Order created! Order Number: ${data.order_number}`);
            window.location.href = "/pending";
        } else {
            const error = await res.json();
            console.error("❌ Error from server:", error);
            alert("Failed to create order: " + (error.error || 'Unknown error'));
        }
    } catch (err) {
        console.error("❌ Network error:", err);
        alert("Network error while submitting order.");
    }
});

// 🚀 Load fabric types on page load
window.addEventListener('DOMContentLoaded', fetchFabricTypes);

