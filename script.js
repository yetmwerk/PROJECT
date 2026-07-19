// ===============================
// Food Ordering System - Part 1
// ===============================

const apiBase = "api";

let menuItems = [];
let filteredItems = [];
let cart = [];

// Elements
const menuGrid = document.getElementById("menu-grid");
const cartItems = document.getElementById("cart-items");
const cartTotal = document.getElementById("cart-total");
const orderButton = document.getElementById("order-button");

// ===============================
// Currency
// ===============================

function formatCurrency(price) {
    return "$" + price.toFixed(2);
}

// ===============================
// Toast Message
// ===============================

function showToast(message) {

    let toast = document.getElementById("toast");

    if (!toast) {

        toast = document.createElement("div");

        toast.id = "toast";

        toast.className = "toast";

        document.body.appendChild(toast);

    }

    toast.innerHTML = message;

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 2500);

}

// ===============================
// Render Menu
// ===============================

function renderMenu(items = filteredItems) {

    if (items.length === 0) {

        menuGrid.innerHTML = "<p>No foods found.</p>";

        return;

    }

    menuGrid.innerHTML = items.map(food => `

        <div class="food-card">

            <img src="${food.image}" class="food-image">

            <h3>${food.name}</h3>

            <p>${food.description}</p>

            <div class="rating">
                ⭐⭐⭐⭐⭐
            </div>

            <div class="food-meta">

                <span class="food-price">

                    ${formatCurrency(food.price)}

                </span>

            </div>

            <button
                class="add-button"
                onclick="addToCart(${food.id})">

                Add to Cart

            </button>

        </div>

    `).join("");

}

// ===============================
// Search Food
// ===============================

function searchFood() {

    const keyword =
        document
        .getElementById("search")
        .value
        .toLowerCase();

    filteredItems =
        menuItems.filter(food =>

            food.name.toLowerCase().includes(keyword)

        );

    renderMenu();

}

// ===============================
// Filter Category
// ===============================

function filterCategory(category) {

    if (category === "All") {

        filteredItems = [...menuItems];

    } else {

        filteredItems =
            menuItems.filter(food =>
                food.category === category
            );

    }

    renderMenu();

}

// ===============================
// Sort Price
// ===============================

function sortPrice(order) {

    if (order === "low") {

        filteredItems.sort((a, b) => a.price - b.price);

    } else {

        filteredItems.sort((a, b) => b.price - a.price);

    }

    renderMenu();

}

// ===============================
// Add to Cart
// ===============================

function addToCart(id) {

    const food =
        menuItems.find(item => item.id === id);

    if (!food) return;

    const existing =
        cart.find(item => item.id === id);

    if (existing) {

        existing.quantity++;

    } else {

        cart.push({

            ...food,

            quantity: 1

        });

    }

    renderCart();

    showToast(food.name + " added to cart.");

}

// ===============================
// Render Cart
// ===============================

function renderCart() {

    if (cart.length === 0) {

        cartItems.innerHTML =

        `<li class="cart-item">

            Your cart is empty.

        </li>`;

        cartTotal.innerHTML = "$0.00";

        return;

    }

    cartItems.innerHTML = cart.map(item => `

        <li class="cart-item">

            <strong>

                ${item.name}

            </strong>

            <span>

                Qty : ${item.quantity}

            </span>

            <span>

                ${formatCurrency(item.price * item.quantity)}

            </span>

        </li>

    `).join("");

    const total =
        cart.reduce(

            (sum, item) =>

            sum + item.price * item.quantity,

            0

        );

    cartTotal.innerHTML = formatCurrency(total);

}

// ===============================
// Load Menu
// ===============================

async function loadMenu() {

    menuGrid.innerHTML =

    `<div class="loader"></div>`;

    try {

        const response =
            await fetch(apiBase + "/data.php");

        const data =
            await response.json();

        menuItems = data;

        filteredItems = [...menuItems];

        renderMenu();

    }

    catch (error) {

        console.error(error);

        menuGrid.innerHTML =

        `<p>Unable to load menu.</p>`;

    }

}

// ===============================
// Place Order
// ===============================

function placeOrder() {

    if (cart.length === 0) {

        alert("Your cart is empty.");

        return;

    }

    const total =

        cart.reduce(

            (sum, item) =>

            sum + item.price * item.quantity,

            0

        );

    alert(

`Order Successful!

Items : ${cart.length}

Total : ${formatCurrency(total)}

Estimated Delivery :

30 Minutes

Thank You!`

    );

    cart = [];

    renderCart();

}

// ===============================
// Events
// ===============================

orderButton.addEventListener(

    "click",

    placeOrder

);

// ===============================
// Start
// ===============================

loadMenu();

renderCart();