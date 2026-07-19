# Food Ordering System

A simple web-based food ordering interface built with HTML, CSS, and JavaScript. Users can browse a menu, add items to a shopping cart, and place an order without any backend or database.

## Features

- Menu display with food names, prices, and images
- Add to cart functionality
- Shopping cart review with remove item option
- Instant total price calculation
- Responsive layout for mobile, tablet, and desktop
- Clean user interface with simple styling
- No backend required; works entirely in the browser

## How to use

1. Open `index.html` in your browser.
2. Click **Add to Cart** for any menu item.
3. Review items in the cart and place the order.

## Files

- `index.html` - main page structure
- `styles.css` - page styling and responsive layout
- `script.js` - menu data, cart logic, and price calculation
- `api/data.php` - backend endpoint that returns menu items
- `api/order.php` - backend endpoint that receives order data and returns confirmation

## Backend Overview

The project includes a simple PHP backend for XAMPP:

- `api/data.php` returns the menu item list as JSON.
- `api/order.php` accepts POST requests with cart items and total, then returns a JSON order confirmation.

## Project Overview

This project is designed for beginners to learn how to build interactive web applications using only front-end code. It simulates a food ordering experience with a menu, cart, and instant total calculation.
