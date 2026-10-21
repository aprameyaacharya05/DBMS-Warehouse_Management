// Database column names stay unchanged; only the displayed labels change.
const fieldLabels = {
    W_id: 'Warehouse ID', W_name: 'Warehouse Name', W_Area: 'Warehouse Area',
    W_City: 'Warehouse City', W_State: 'Warehouse State', W_Pincode: 'Warehouse Pincode',
    Capacity: 'Warehouse Capacity', Manager_id: 'Manager Employee ID',
    Cur_stock: 'Current Stock (Units)', Total_amt: 'Order Total',
    P_id: 'Product ID', P_name: 'Product Name', P_price: 'Product Price', Category: 'Product Category',
    S_id: 'Supplier ID', S_name: 'Supplier Name', S_phone: 'Supplier Phone Number',
    Addr_no: 'Supplier Address Number', S_Area: 'Supplier Area', S_City: 'Supplier City',
    S_State: 'Supplier State', S_Pincode: 'Supplier Pincode',
    C_id: 'Customer ID', C_name: 'Customer Name', C_phone: 'Customer Phone Number',
    E_id: 'Employee ID', E_name: 'Employee Name', Role: 'Employee Role',
    E_phone: 'Employee Phone Number', Supervisor_id: 'Supervisor Employee ID',
    O_id: 'Order ID', O_date: 'Order Date', Payment_Type: 'Payment Type',
    Item_no: 'Order Item Number', I_quantity: 'Order Item Quantity',
    Sell_price: 'Item Selling Price', P_quantity: 'Inventory Quantity'
};

function inputError(input) {
    const label = input.dataset.label || input.previousElementSibling?.textContent || 'Value';
    const value = input.value.trim();
    if (!value) return input.required ? `${label} is required.` : '';
    const integer = / ID$|Number$|Quantity$|Capacity$/.test(label) && !label.includes('Phone');
    const price = label.includes('Price');
    if (integer && !/^\d+$/.test(value)) return `${label} must be a whole number, zero or greater.`;
    if (price && (!/^\d+(\.\d{1,2})?$/.test(value) || !Number.isFinite(Number(value)))) {
        return `${label} must be zero or greater, with at most two decimal places.`;
    }
    return '';
}

function showInputError(input) {
    let error = input.nextElementSibling;
    if (!error?.classList.contains('field-error')) {
        error = document.createElement('span');
        error.className = 'field-error';
        error.setAttribute('aria-live', 'polite');
        input.after(error);
    }
    error.textContent = inputError(input);
    input.setAttribute('aria-invalid', error.textContent ? 'true' : 'false');
    return !error.textContent;
}

// Capture runs before the individual form's add/update handler.
document.addEventListener('submit', event => {
    let firstInvalid;
    for (const input of event.target.querySelectorAll('input')) {
        if (!showInputError(input) && !firstInvalid) firstInvalid = input;
    }
    if (firstInvalid) {
        event.preventDefault();
        event.stopImmediatePropagation();
        firstInvalid.focus();
    }
}, true);
document.addEventListener('input', event => {
    if (event.target.matches('input')) showInputError(event.target);
});
document.addEventListener('invalid', event => {
    if (event.target.matches('input')) showInputError(event.target);
}, true);
