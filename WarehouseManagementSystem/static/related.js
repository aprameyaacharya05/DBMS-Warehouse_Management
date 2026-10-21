// Both key values always identify a related record; edits keep the original keys.
const relatedTables = {
    inventory: {keys: ['W_id', 'P_id'], fields: ['W_id', 'P_id', 'P_quantity']},
    'order-item': {keys: ['O_id', 'Item_no'], fields: ['O_id', 'Item_no', 'I_quantity', 'Sell_price', 'P_id']},
    'supplier-phone': {keys: ['S_id', 'S_phone'], fields: ['S_id', 'S_phone']},
    'supplier-address': {keys: ['S_id', 'Addr_no'], fields: ['S_id', 'Addr_no', 'S_Area', 'S_City', 'S_State', 'S_Pincode']},
    supplies: {keys: ['S_id', 'P_id'], fields: ['S_id', 'P_id']}
};
let relatedContext;

function refreshRelated() {
    return showRelated(relatedContext.type, relatedContext.id);
}

async function relatedRequest(url, method = 'GET', data) {
    const response = await fetch(url, {
        method,
        headers: {'Content-Type': 'application/json'},
        ...(data ? {body: JSON.stringify(data)} : {})
    });
    let result;
    try { result = await response.json(); }
    catch { throw new Error('The server could not complete this operation. Please try again.'); }
    if (!response.ok || result.success === false) throw new Error(result.message || 'Operation failed.');
    return result;
}

function relatedMessage(text, success = false) {
    const message = document.getElementById('relatedMessage');
    if (message) {
        message.textContent = text;
        message.className = success ? 'message success' : 'message error';
    }
}

async function showRelated(type, id) {
    relatedContext = {type, id};
    const area = document.getElementById('formArea');
    area.replaceChildren();
    const back = document.createElement('button');
    back.className = 'back-to-list';
    back.textContent = '← Back to list';
    back.onclick = () => viewRecords(currentTable);
    const message = document.createElement('p');
    message.id = 'relatedMessage';
    area.append(back, message);
    const sections = {
        product: [['supplies', `/view-supplies-product/${id}`, {P_id: id}]],
        supplier: [
            ['supplier-phone', `/view-supplier-phones/${id}`, {S_id: id}],
            ['supplier-address', `/view-supplier-addresses/${id}`, {S_id: id}]
        ],
        warehouse: [['inventory', `/view-inventory/${id}`, {W_id: id}]],
        order: [['order-item', `/view-order-items/${id}`, {O_id: id}]]
    };
    try {
        for (const [table, url, defaults] of sections[type]) {
            const records = await relatedRequest(url);
            if (document.getElementById('relatedMessage') !== message) return;
            renderRelatedTable(table, records, defaults, area);
        }
    } catch (error) { relatedMessage(error.message); }
}

function renderRelatedTable(table, records, defaults, area) {
    const config = relatedTables[table];
    const section = document.createElement('section');
    const heading = document.createElement('h3');
    heading.textContent = capitalize(table);
    const add = document.createElement('button');
    add.textContent = `Add ${capitalize(table)}`;
    add.onclick = () => relatedForm(table, defaults, false, section);
    section.append(heading, add);
    const grid = document.createElement('table');
    const header = grid.createTHead().insertRow();
    for (const name of [...config.fields, 'Actions']) {
        const cell = document.createElement('th');
        cell.textContent = fieldLabels[name] || name;
        header.append(cell);
    }
    const body = grid.createTBody();
    for (const record of records) {
        const row = body.insertRow();
        for (const field of config.fields) row.insertCell().textContent = record[field] ?? '';
        const actions = row.insertCell();
        const edit = document.createElement('button');
        edit.textContent = 'Edit';
        edit.onclick = () => relatedForm(table, record, true, section);
        const remove = document.createElement('button');
        remove.textContent = 'Delete';
        remove.onclick = async () => {
            const keys = config.keys.map(key => encodeURIComponent(record[key])).join('/');
            if (!confirm(`Delete ${capitalize(table)} (${config.keys.map(key => record[key]).join(', ')})?`)) return;
            try {
                const result = await relatedRequest(`/delete-${table}/${keys}`, 'DELETE');
                await refreshRelated();
                relatedMessage(result.message, true);
            } catch (error) { relatedMessage(error.message); }
        };
        actions.append(edit, remove);
    }
    section.append(grid);
    if (!records.length) {
        const empty = document.createElement('p');
        empty.textContent = 'No records found. Use Add to create one.';
        section.append(empty);
    }
    area.append(section);
}

function relatedForm(table, record, editing, section) {
    document.querySelectorAll('.related-form').forEach(form => form.remove());
    const config = relatedTables[table];
    const form = document.createElement('form');
    form.className = 'related-form';
    const inputs = {};
    for (const field of config.fields) {
        const label = document.createElement('label');
        label.textContent = fieldLabels[field] || field;
        const input = document.createElement('input');
        input.dataset.label = fieldLabels[field] || field;
        input.value = record[field] ?? '';
        input.required = true;
        input.type = /(_id|_no|quantity|price)$/i.test(field) ? 'number' : 'text';
        if (input.type === 'number') {
            input.min = '0';
            input.step = field === 'Sell_price' ? '0.01' : '1';
        }
        // Phone and supply edits can change a key, using the saved original pair.
        input.readOnly = editing
            ? config.keys.includes(field) && table !== 'supplies' && field !== 'S_phone'
            : Object.hasOwn(record, field);
        label.append(input);
        form.append(label);
        inputs[field] = input;
    }
    const save = document.createElement('button');
    save.type = 'submit';
    save.textContent = editing ? 'Save changes' : 'Add record';
    const cancel = document.createElement('button');
    cancel.type = 'button';
    cancel.textContent = 'Cancel';
    cancel.onclick = () => form.remove();
    form.append(save, cancel);
    form.onsubmit = async event => {
        event.preventDefault();
        const data = Object.fromEntries(config.fields.map(field => [field.toLowerCase(), inputs[field].value.trim()]));
        if (editing && table === 'supplier-phone') data.old_phone = record.S_phone;
        if (editing && table === 'supplies') {
            data.old_s_id = record.S_id;
            data.old_p_id = record.P_id;
        }
        save.disabled = true;
        try {
            const result = await relatedRequest(`/${editing ? 'update' : 'add'}-${table}`, editing ? 'PUT' : 'POST', data);
            await refreshRelated();
            relatedMessage(result.message, true);
        } catch (error) { relatedMessage(error.message); }
        finally { save.disabled = false; }
    };
    section.append(form);
}
