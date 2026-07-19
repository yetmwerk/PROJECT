<?php

session_start();

include "api/db.php";



// Check login

if(!isset($_SESSION['user_id'])){


header("Location:login.php");

exit();


}


$user_id=$_SESSION['user_id'];



// Get customer orders


$orders=$conn->query("


SELECT *

FROM orders

WHERE user_id=$user_id

ORDER BY order_date DESC


");


?>


<!DOCTYPE html>

<html>


<head>


<title>

My Orders

</title>


<link rel="stylesheet" href="assets/css/styles.css">


</head>


<body>



<nav>


<h2>
FoodExpress
</h2>


<a href="index.php">
Home
</a>


<a href="menu.php">
Menu
</a>


<a href="cart.php">
Cart
</a>


<a href="logout.php">
Logout
</a>



</nav>



<h1 class="title">

My Order History

</h1>




<?php while($order=$orders->fetch_assoc()){ ?>



<div class="food-card" style="width:70%;margin:20px auto;">



<h3>

Order ID:

#

<?php echo $order['order_id']; ?>


</h3>



<p>

Date:

<?php echo $order['order_date']; ?>

</p>



<p>

Total Amount:

$

<?php echo $order['total_amount']; ?>

</p>



<p>

Status:

<strong>

<?php echo $order['order_status']; ?>

</strong>


</p>




<h4>

Order Items

</h4>



<table border="1" width="100%">


<tr>

<th>
Food
</th>

<th>
Quantity
</th>

<th>
Price
</th>


</tr>



<?php



$order_id=$order['order_id'];



$items=$conn->query("


SELECT

foods.food_name,

order_details.quantity,

order_details.price


FROM order_details


JOIN foods


ON order_details.food_id=foods.food_id


WHERE order_id=$order_id



");



while($item=$items->fetch_assoc()){


?>



<tr>


<td>

<?php echo $item['food_name']; ?>

</td>


<td>

<?php echo $item['quantity']; ?>

</td>



<td>

$

<?php echo $item['price']; ?>

</td>



</tr>



<?php } ?>



</table>



</div>



<?php } ?>



</body>

</html>