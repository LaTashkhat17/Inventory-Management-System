// Global variables
let authToken = '';
let currentUserRole = '';
const API_BASE = 'http://localhost:8000/api';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Check if already logged in
    const token = localStorage.getItem('authToken');
    const role = localStorage.getItem('userRole');
    
    if (token && role) {
        authToken = token;
        currentUserRole = role;
        showMainApp();
    }
    
    // Setup event listeners
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('supplierForm').addEventListener('submit', handleSupplierSubmit);
    document.getElementById('customerForm').addEventListener('submit', handleCustomerSubmit);
    document.getElementById('itemForm').addEventListener('submit', handleItemSubmit);
    document.getElementById('purchaseForm').addEventListener('submit', handlePurchaseSubmit);
    document.getElementById('salesForm').addEventListener('submit', handleSalesSubmit);
    document.getElementById('cashFlowForm').addEventListener('submit', handleCashFlowSubmit);
    
    // Set today's date for date inputs
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('purchaseDate').value = today;
    document.getElementById('salesDate').value = today;
    document.getElementById('cashFlowDate').value = today;
});

// API Helper Functions
async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (authToken) {
        options.headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        
        if (response.status === 401) {
            logout();
            return null;
        }
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.detail || 'An error occurred');
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        alert('Network error. Please check if the server is running.');
        return null;
    }
}

// Authentication
async function handleLogin(e) {
    e.preventDefault();
    console.log('Login attempt started');
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;
    
    console.log('Attempting login:', { username, role });
    
    const data = await apiCall('/auth/login', 'POST', { username, password, role });
    
    console.log('Login response:', data);
    
    if (data) {
        authToken = data.access_token;
        currentUserRole = data.role;
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('userRole', currentUserRole);
        console.log('Login successful, showing main app');
        showMainApp();
    } else {
        console.log('Login failed - no data returned');
    }
}

function logout() {
    authToken = '';
    currentUserRole = '';
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
    document.getElementById('loginScreen').style.display = 'flex';
    document.getElementById('mainApp').style.display = 'none';
}

function showMainApp() {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('mainApp').style.display = 'flex';
    document.getElementById('userRoleDisplay').textContent = `Role: ${currentUserRole}`;
    showModule('dashboard');
}

// Navigation
function showModule(moduleName) {
    // Hide all modules
    document.querySelectorAll('.module').forEach(m => m.style.display = 'none');
    
    // Show selected module
    document.getElementById(moduleName).style.display = 'block';
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    event.target.classList.add('active');
    
    // Load module data
    loadModuleData(moduleName);
}

function loadModuleData(moduleName) {
    switch(moduleName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'suppliers':
            loadSuppliers();
            break;
        case 'customers':
            loadCustomers();
            break;
        case 'items':
            loadItems();
            break;
        case 'purchases':
            loadPurchases();
            break;
        case 'sales':
            loadSales();
            break;
        case 'cashflow':
            loadCashFlow();
            break;
        case 'reports':
            loadReports();
            break;
    }
}

// Dashboard
let salesChart, purchaseChart, cashFlowChart;

async function loadDashboard() {
    const data = await apiCall('/reports/dashboard');
    if (!data) return;
    
    document.getElementById('totalSales').textContent = `TK${data.total_sales.toFixed(2)}`;
    document.getElementById('totalPurchases').textContent = `TK${data.total_purchases.toFixed(2)}`;
    document.getElementById('netCashFlow').textContent = `TK${data.net_cashflow.toFixed(2)}`;
    document.getElementById('totalItems').textContent = data.total_items;
    
    // Create charts
    createSalesChart(data.sales_data);
    createPurchaseChart(data.purchase_data);
    createCashFlowChart(data.cashflow_data);
}

function createSalesChart(data) {
    const ctx = document.getElementById('salesChart').getContext('2d');
    if (salesChart) salesChart.destroy();
    salesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Sales',
                data: data.map(d => d.amount),
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createPurchaseChart(data) {
    const ctx = document.getElementById('purchaseChart').getContext('2d');
    if (purchaseChart) purchaseChart.destroy();
    purchaseChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Purchases',
                data: data.map(d => d.amount),
                backgroundColor: '#2563eb'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createCashFlowChart(data) {
    const ctx = document.getElementById('cashFlowChart').getContext('2d');
    if (cashFlowChart) cashFlowChart.destroy();
    const inflows = data.filter(d => d.type === 'IN').map(d => d.amount);
    const outflows = data.filter(d => d.type === 'OUT').map(d => d.amount);
    
    cashFlowChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Inflow', 'Outflow'],
            datasets: [{
                data: [inflows.reduce((a, b) => a + b, 0), outflows.reduce((a, b) => a + b, 0)],
                backgroundColor: ['#10b981', '#ef4444']
            }]
        },
        options: {
            responsive: true
        }
    });
}

// Suppliers
async function loadSuppliers() {
    const suppliers = await apiCall('/suppliers');
    if (!suppliers) return;
    
    const tbody = document.getElementById('suppliersTableBody');
    tbody.innerHTML = suppliers.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.name}</td>
            <td>${s.contact || '-'}</td>
            <td>${s.email || '-'}</td>
            <td>${s.status}</td>
            <td>
                <button class="btn-edit" onclick="editSupplier(${s.id})">Edit</button>
                <button class="btn-danger" onclick="deleteSupplier(${s.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function openSupplierModal(id = null) {
    document.getElementById('supplierModal').style.display = 'block';
    document.getElementById('supplierId').value = id || '';
    document.getElementById('supplierModalTitle').textContent = id ? 'Edit Supplier' : 'Add Supplier';
    document.getElementById('supplierForm').reset();
}

function closeSupplierModal() {
    document.getElementById('supplierModal').style.display = 'none';
}

async function handleSupplierSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('supplierId').value;
    const data = {
        name: document.getElementById('supplierName').value,
        contact: document.getElementById('supplierContact').value,
        email: document.getElementById('supplierEmail').value,
        address: document.getElementById('supplierAddress').value,
        status: document.getElementById('supplierStatus').value
    };
    
    if (id) {
        await apiCall(`/suppliers/${id}`, 'PUT', data);
    } else {
        await apiCall('/suppliers', 'POST', data);
    }
    
    closeSupplierModal();
    loadSuppliers();
}

async function editSupplier(id) {
    const suppliers = await apiCall(`/suppliers`);
    const s = suppliers.find(s => s.id === id);
    if (s) {
        document.getElementById('supplierId').value = s.id;
        document.getElementById('supplierName').value = s.name;
        document.getElementById('supplierContact').value = s.contact || '';
        document.getElementById('supplierEmail').value = s.email || '';
        document.getElementById('supplierAddress').value = s.address || '';
        document.getElementById('supplierStatus').value = s.status;
        openSupplierModal(id);
    }
}

async function deleteSupplier(id) {
    if (confirm('Are you sure you want to delete this supplier?')) {
        await apiCall(`/suppliers/${id}`, 'DELETE');
        loadSuppliers();
    }
}

// Customers
async function loadCustomers() {
    const customers = await apiCall('/customers');
    if (!customers) return;
    
    const tbody = document.getElementById('customersTableBody');
    tbody.innerHTML = customers.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${c.name}</td>
            <td>${c.contact || '-'}</td>
            <td>${c.email || '-'}</td>
            <td>${c.status}</td>
            <td>
                <button class="btn-edit" onclick="editCustomer(${c.id})">Edit</button>
                <button class="btn-danger" onclick="deleteCustomer(${c.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function openCustomerModal(id = null) {
    document.getElementById('customerModal').style.display = 'block';
    document.getElementById('customerId').value = id || '';
    document.getElementById('customerModalTitle').textContent = id ? 'Edit Customer' : 'Add Customer';
    document.getElementById('customerForm').reset();
}

function closeCustomerModal() {
    document.getElementById('customerModal').style.display = 'none';
}

async function handleCustomerSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('customerId').value;
    const data = {
        name: document.getElementById('customerName').value,
        contact: document.getElementById('customerContact').value,
        email: document.getElementById('customerEmail').value,
        address: document.getElementById('customerAddress').value,
        status: document.getElementById('customerStatus').value
    };
    
    if (id) {
        await apiCall(`/customers/${id}`, 'PUT', data);
    } else {
        await apiCall('/customers', 'POST', data);
    }
    
    closeCustomerModal();
    loadCustomers();
}

async function editCustomer(id) {
    const customers = await apiCall(`/customers`);
    const c = customers.find(c => c.id === id);
    if (c) {
        document.getElementById('customerId').value = c.id;
        document.getElementById('customerName').value = c.name;
        document.getElementById('customerContact').value = c.contact || '';
        document.getElementById('customerEmail').value = c.email || '';
        document.getElementById('customerAddress').value = c.address || '';
        document.getElementById('customerStatus').value = c.status;
        openCustomerModal(id);
    }
}

async function deleteCustomer(id) {
    if (confirm('Are you sure you want to delete this customer?')) {
        await apiCall(`/customers/${id}`, 'DELETE');
        loadCustomers();
    }
}

// Items
async function loadItems() {
    const items = await apiCall('/items');
    if (!items) return;
    
    const tbody = document.getElementById('itemsTableBody');
    tbody.innerHTML = items.map(i => `
        <tr>
            <td>${i.id}</td>
            <td>${i.name}</td>
            <td>${i.unit_of_measure || '-'}</td>
            <td>${i.current_stock}</td>
            <td>
                <button class="btn-edit" onclick="editItem(${i.id})">Edit</button>
                <button class="btn-danger" onclick="deleteItem(${i.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function openItemModal(id = null) {
    document.getElementById('itemModal').style.display = 'block';
    document.getElementById('itemId').value = id || '';
    document.getElementById('itemModalTitle').textContent = id ? 'Edit Item' : 'Add Item';
    document.getElementById('itemForm').reset();
}

function closeItemModal() {
    document.getElementById('itemModal').style.display = 'none';
}

async function handleItemSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('itemId').value;
    const data = {
        name: document.getElementById('itemName').value,
        unit_of_measure: document.getElementById('itemUnit').value,
        current_stock: parseFloat(document.getElementById('itemStock').value)
    };
    
    if (id) {
        await apiCall(`/items/${id}`, 'PUT', data);
    } else {
        await apiCall('/items', 'POST', data);
    }
    
    closeItemModal();
    loadItems();
}

async function editItem(id) {
    const items = await apiCall(`/items`);
    const i = items.find(i => i.id === id);
    if (i) {
        document.getElementById('itemId').value = i.id;
        document.getElementById('itemName').value = i.name;
        document.getElementById('itemUnit').value = i.unit_of_measure || '';
        document.getElementById('itemStock').value = i.current_stock;
        openItemModal(id);
    }
}

async function deleteItem(id) {
    if (confirm('Are you sure you want to delete this item?')) {
        await apiCall(`/items/${id}`, 'DELETE');
        loadItems();
    }
}

// Purchases
let purchaseItems = [];

async function loadPurchases() {
    const purchases = await apiCall('/purchases');
    if (!purchases) return;
    
    const tbody = document.getElementById('purchasesTableBody');
    tbody.innerHTML = purchases.map(p => `
        <tr>
            <td>${p.id}</td>
            <td>${p.purchase_date}</td>
            <td>${p.supplier_id}</td>
            <td>TK${p.total_amount.toFixed(2)}</td>
            <td>
                <button class="btn-edit" onclick="viewPurchase(${p.id})">View</button>
            </td>
        </tr>
    `).join('');
}

function openPurchaseModal() {
    document.getElementById('purchaseModal').style.display = 'block';
    purchaseItems = [];
    updatePurchaseItemsList();
    loadSuppliersForPurchase();
}

function closePurchaseModal() {
    document.getElementById('purchaseModal').style.display = 'none';
    purchaseItems = [];
}

async function loadSuppliersForPurchase() {
    const suppliers = await apiCall('/suppliers');
    if (!suppliers) return;
    
    const select = document.getElementById('purchaseSupplier');
    select.innerHTML = '<option value="">Select Supplier</option>' + 
        suppliers.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
}

function addPurchaseItem() {
    purchaseItems.push({ item_id: '', quantity: 0, rate: 0 });
    updatePurchaseItemsList();
}

function removePurchaseItem(index) {
    purchaseItems.splice(index, 1);
    updatePurchaseItemsList();
}

async function updatePurchaseItemsList() {
    const items = await apiCall('/items');
    if (!items) return;
    
    const container = document.getElementById('purchaseItemsList');
    container.innerHTML = purchaseItems.map((item, index) => `
        <div class="purchase-item-row">
            <select onchange="purchaseItems[${index}].item_id = this.value">
                <option value="">Select Item</option>
                ${items.map(i => `<option value="${i.id}">${i.name}</option>`).join('')}
            </select>
            <input type="number" placeholder="Quantity" step="0.01" onchange="purchaseItems[${index}].quantity = parseFloat(this.value); updatePurchaseTotal()">
            <input type="number" placeholder="Rate" step="0.01" onchange="purchaseItems[${index}].rate = parseFloat(this.value); updatePurchaseTotal()">
            <button type="button" class="btn-danger" onclick="removePurchaseItem(${index})">Remove</button>
        </div>
    `).join('');
}

function updatePurchaseTotal() {
    const total = purchaseItems.reduce((sum, item) => sum + (item.quantity * item.rate), 0);
    document.getElementById('purchaseTotal').textContent = total.toFixed(2);
}

async function handlePurchaseSubmit(e) {
    e.preventDefault();
    const data = {
        purchase_date: document.getElementById('purchaseDate').value,
        supplier_id: parseInt(document.getElementById('purchaseSupplier').value),
        details: purchaseItems.filter(item => item.item_id && item.quantity > 0 && item.rate > 0)
    };
    
    await apiCall('/purchases', 'POST', data);
    closePurchaseModal();
    loadPurchases();
}

async function viewPurchase(id) {
    const purchase = await apiCall(`/purchases/${id}`);
    if (purchase) {
        alert(`Purchase #${id}\nSupplier: ${purchase.master.supplier_id}\nTotal: TK${purchase.master.total_amount.toFixed(2)}`);
    }
}

// Sales
let salesItems = [];

async function loadSales() {
    const sales = await apiCall('/sales');
    if (!sales) return;
    
    const tbody = document.getElementById('salesTableBody');
    tbody.innerHTML = sales.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.sales_date}</td>
            <td>${s.customer_id}</td>
            <td>TK${s.total_amount.toFixed(2)}</td>
            <td>
                <button class="btn-edit" onclick="viewSale(${s.id})">View</button>
            </td>
        </tr>
    `).join('');
}

function openSalesModal() {
    document.getElementById('salesModal').style.display = 'block';
    salesItems = [];
    updateSalesItemsList();
    loadCustomersForSales();
}

function closeSalesModal() {
    document.getElementById('salesModal').style.display = 'none';
    salesItems = [];
}

async function loadCustomersForSales() {
    const customers = await apiCall('/customers');
    if (!customers) return;
    
    const select = document.getElementById('salesCustomer');
    select.innerHTML = '<option value="">Select Customer</option>' + 
        customers.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
}

function addSalesItem() {
    salesItems.push({ item_id: '', quantity: 0, rate: 0 });
    updateSalesItemsList();
}

function removeSalesItem(index) {
    salesItems.splice(index, 1);
    updateSalesItemsList();
}

async function updateSalesItemsList() {
    const items = await apiCall('/items');
    if (!items) return;
    
    const container = document.getElementById('salesItemsList');
    container.innerHTML = salesItems.map((item, index) => `
        <div class="sales-item-row">
            <select onchange="salesItems[${index}].item_id = this.value">
                <option value="">Select Item</option>
                ${items.map(i => `<option value="${i.id}">${i.name} (Stock: ${i.current_stock})</option>`).join('')}
            </select>
            <input type="number" placeholder="Quantity" step="0.01" onchange="salesItems[${index}].quantity = parseFloat(this.value); updateSalesTotal()">
            <input type="number" placeholder="Rate" step="0.01" onchange="salesItems[${index}].rate = parseFloat(this.value); updateSalesTotal()">
            <button type="button" class="btn-danger" onclick="removeSalesItem(${index})">Remove</button>
        </div>
    `).join('');
}

function updateSalesTotal() {
    const total = salesItems.reduce((sum, item) => sum + (item.quantity * item.rate), 0);
    document.getElementById('salesTotal').textContent = total.toFixed(2);
}

async function handleSalesSubmit(e) {
    e.preventDefault();
    const data = {
        sales_date: document.getElementById('salesDate').value,
        customer_id: parseInt(document.getElementById('salesCustomer').value),
        details: salesItems.filter(item => item.item_id && item.quantity > 0 && item.rate > 0)
    };
    
    await apiCall('/sales', 'POST', data);
    closeSalesModal();
    loadSales();
}

async function viewSale(id) {
    const sale = await apiCall(`/sales/${id}`);
    if (sale) {
        alert(`Sale #${id}\nCustomer: ${sale.master.customer_id}\nTotal: TK${sale.master.total_amount.toFixed(2)}`);
    }
}

// Cash Flow
async function loadCashFlow() {
    const cashflows = await apiCall('/cashflow');
    if (!cashflows) return;
    
    const tbody = document.getElementById('cashFlowTableBody');
    tbody.innerHTML = cashflows.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${c.transaction_date}</td>
            <td>${c.type}</td>
            <td>TK${c.amount.toFixed(2)}</td>
            <td>${c.description || '-'}</td>
            <td>
                <button class="btn-edit" onclick="editCashFlow(${c.id})">Edit</button>
                <button class="btn-danger" onclick="deleteCashFlow(${c.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function openCashFlowModal(id = null) {
    document.getElementById('cashFlowModal').style.display = 'block';
    document.getElementById('cashFlowId').value = id || '';
    document.getElementById('cashFlowModalTitle').textContent = id ? 'Edit Transaction' : 'Add Transaction';
    document.getElementById('cashFlowForm').reset();
}

function closeCashFlowModal() {
    document.getElementById('cashFlowModal').style.display = 'none';
}

async function handleCashFlowSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('cashFlowId').value;
    const data = {
        transaction_date: document.getElementById('cashFlowDate').value,
        type: document.getElementById('cashFlowType').value,
        amount: parseFloat(document.getElementById('cashFlowAmount').value),
        description: document.getElementById('cashFlowDescription').value
    };
    
    if (id) {
        await apiCall(`/cashflow/${id}`, 'PUT', data);
    } else {
        await apiCall('/cashflow', 'POST', data);
    }
    
    closeCashFlowModal();
    loadCashFlow();
}

async function editCashFlow(id) {
    const cashflows = await apiCall(`/cashflow`);
    const c = cashflows.find(c => c.id === id);
    if (c) {
        document.getElementById('cashFlowId').value = c.id;
        document.getElementById('cashFlowDate').value = c.transaction_date;
        document.getElementById('cashFlowType').value = c.type;
        document.getElementById('cashFlowAmount').value = c.amount;
        document.getElementById('cashFlowDescription').value = c.description || '';
        openCashFlowModal(id);
    }
}

async function deleteCashFlow(id) {
    if (confirm('Are you sure you want to delete this transaction?')) {
        await apiCall(`/cashflow/${id}`, 'DELETE');
        loadCashFlow();
    }
}

// Reports
async function loadReports() {
    const items = await apiCall('/items');
    if (!items) return;
    
    const select = document.getElementById('reportItemSelect');
    select.innerHTML = '<option value="">All Items</option>' + 
        items.map(i => `<option value="${i.id}">${i.name}</option>`).join('');
    
    generateInventoryReport();
}

async function generateInventoryReport() {
    const itemId = document.getElementById('reportItemSelect').value;
    const endpoint = itemId ? `/reports/inventory?item_id=${itemId}` : '/reports/inventory';
    const ledger = await apiCall(endpoint);
    if (!ledger) return;
    
    const tbody = document.getElementById('inventoryReportTableBody');
    tbody.innerHTML = ledger.map(l => `
        <tr>
            <td>${l.movement_date}</td>
            <td>${l.item_id}</td>
            <td>${l.movement_type}</td>
            <td>${l.quantity}</td>
            <td>${l.movement_reference || '-'}</td>
        </tr>
    `).join('');
}

