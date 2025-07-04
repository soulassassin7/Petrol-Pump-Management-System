function deleteCustomer(customerId) {
    if (confirm("Are you sure you want to delete this customer?")) {
        fetch(`/delete_customer/${customerId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("Customer deleted successfully.");
                window.location.reload();
            } else {
                alert("Failed to delete customer. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while trying to delete the customer.");
        });
    }
}

function deleteTransaction(transactionId) {
    if (confirm("Are you sure you want to delete this transaction?")) {
        fetch(`/delete_transaction/${transactionId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("Transaction deleted successfully.");
                window.location.reload();
            } else {
                alert("Failed to delete transaction. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while trying to delete the transaction.");
        });
    }
}

function deleteEmployee(employeeId) {
    if (confirm("Are you sure you want to delete this employee?")) {
        fetch(`/delete_employee/${employeeId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("Employee deleted successfully.");
                window.location.reload();
            } else {
                alert("Failed to delete employee. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while trying to delete the employee.");
        });
    }
}

function deletePump(pumpId) {
    if (confirm("Are you sure you want to delete this pump?")) {
        fetch(`/delete_pump/${pumpId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("Pump deleted successfully.");
                window.location.reload();
            } else {
                alert("Failed to delete pump. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while trying to delete the pump.");
        });
    }
}

function deleteDeliveryVehicle(vehicleId) {
    if (confirm("Are you sure you want to delete this delivery vehicle?")) {
        fetch(`/delete_delivery_vehicle/${vehicleId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("Delivery vehicle deleted successfully.");
                window.location.reload();
            } else {
                alert("Failed to delete delivery vehicle. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while trying to delete the delivery vehicle.");
        });
    }
}

function deleteFuel(fuelId) {
    if (confirm("Are you sure you want to delete this fuel?")) {
        fetch(`/delete_fuel/${fuelId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("Fuel deleted successfully.");
                window.location.reload();
            } else {
                alert("Failed to delete fuel. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while trying to delete the fuel.");
        });
    }
}

function deleteReceipt(receiptId) {
    if (confirm("Are you sure you want to delete this receipt?")) {
        fetch(`/delete_receipt/${receiptId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("Receipt deleted successfully.");
                window.location.reload();
            } else {
                alert("Failed to delete receipt. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while trying to delete the receipt.");
        });
    }
}

let currentFuelId; // Global variable to store the current fuel ID

function modifyFuel(fuelId, currentStock, currentPrice) {
    currentFuelId = fuelId; // Store the fuel ID for later use
    document.getElementById('new_stock').value = currentStock;
    document.getElementById('new_price').value = currentPrice;
    document.getElementById('modifyModal').style.display = 'flex';
}

// Close modal function
function closeModal() {
    document.getElementById('modifyModal').style.display = 'none';
}

// Handle form submission
document.getElementById('modifyForm').onsubmit = function (event) {
    event.preventDefault(); // Prevent default form submission
    const newStock = document.getElementById('new_stock').value;
    const newPrice = document.getElementById('new_price').value;

    fetch(`/modify_fuel/${currentFuelId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `new_stock=${newStock}&new_price=${newPrice}`
    })
    .then(response => {
        if (response.ok) {
            alert("Fuel details updated successfully.");
            window.location.reload();
        } else {
            alert("Failed to update fuel details. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while trying to update the fuel details.");
    });

    closeModal();
};

