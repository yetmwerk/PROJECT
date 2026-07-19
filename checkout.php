<?php

session_start();

include "api/db.php";


if(!isset($_SESSION['user_id'])){

header("Location:login.php");

exit();

}



$user_id=$_SESSION['user_id'];



$result=$conn->query("

SELECT

foods.food_name,

foods.price,

cart.quantity


FROM cart


JOIN foods


ON cart.food_id=foods.food_id


WHERE cart.user_id=$user_id


");



$total=0;


?>



<!DOCTYPE html>

<html>


<head>

<title>
Checkout
</title>


<link rel="stylesheet" href="assets/css/styles.css">


</head>


<body>



<nav>


<h2>
FoodExpress
</h2>


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

Checkout

</h1>



<table border="1" width="70%" align="center">


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



<?php while($row=$result->fetch_assoc()){ 



$item_total=
$row['price']*$row['quantity'];


$total += $item_total;


?>


<tr>


<td>

<?php echo $row['food_name']; ?>

</td>


<td>

<?php echo $row['quantity']; ?>

</td>


<td>

$

<?php echo $item_total; ?>

</td>


</tr>



<?php } ?>


<tr>


<td colspan="2">

<h3>
Total
</h3>

</td>


<td>

<h3>

$

<?php echo $total; ?>

</h3>

</td>


</tr>


</table>



<br>


<center>


<form action="api/order.php" method="POST">


<button type="submit">

Confirm Order

</button>


</form>


</center>



</body>

</html>