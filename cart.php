<?php

session_start();

include "api/db.php";


// User must login

if(!isset($_SESSION['user_id'])){


header("Location:login.php");

exit();

}



$user_id=$_SESSION['user_id'];



// ADD FOOD TO CART


if(isset($_GET['add'])){


$food_id=$_GET['add'];



// Check existing cart item


$check=$conn->prepare(

"SELECT * FROM cart 
WHERE user_id=? AND food_id=?"

);



$check->bind_param(

"ii",

$user_id,

$food_id

);



$check->execute();


$result=$check->get_result();



if($result->num_rows>0){



$conn->query(

"UPDATE cart

SET quantity=quantity+1

WHERE user_id=$user_id

AND food_id=$food_id"

);



}

else{


$stmt=$conn->prepare(

"INSERT INTO cart
(user_id,food_id,quantity)

VALUES(?,?,1)"

);



$stmt->bind_param(

"ii",

$user_id,

$food_id

);



$stmt->execute();


}



header("Location:cart.php");


}



// REMOVE ITEM


if(isset($_GET['remove'])){


$cart_id=$_GET['remove'];



$conn->query(

"DELETE FROM cart

WHERE cart_id=$cart_id"

);



header("Location:cart.php");


}




// GET CART ITEMS



$sql="

SELECT

cart.cart_id,

cart.quantity,

foods.food_name,

foods.price,

foods.image


FROM cart


JOIN foods


ON cart.food_id=foods.food_id


WHERE cart.user_id=$user_id


";



$result=$conn->query($sql);



$total=0;


?>



<!DOCTYPE html>

<html>

<head>


<title>

Shopping Cart

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


<a href="logout.php">
Logout
</a>


</nav>



<h1 class="title">

My Shopping Cart

</h1>




<table border="1" width="80%" align="center">


<tr>

<th>
Image
</th>


<th>
Food
</th>


<th>
Price
</th>


<th>
Quantity
</th>


<th>
Total
</th>


<th>
Action
</th>


</tr>



<?php while($item=$result->fetch_assoc()){ 



$item_total =
$item['price']*$item['quantity'];


$total += $item_total;


?>



<tr>


<td>


<img

src="assets/images/<?php echo $item['image'];?>"

width="80"


>


</td>



<td>

<?php echo $item['food_name'];?>

</td>



<td>

$

<?php echo $item['price'];?>

</td>



<td>

<?php echo $item['quantity'];?>

</td>



<td>

$

<?php echo $item_total;?>

</td>



<td>


<a href="cart.php?remove=<?php echo $item['cart_id'];?>">


<button>

Remove

</button>


</a>


</td>



</tr>



<?php } ?>



<tr>


<td colspan="4">

<h2>

Total

</h2>

</td>


<td colspan="2">


<h2>

$

<?php echo $total;?>


</h2>


</td>


</tr>



</table>



<br>


<center>


<a href="checkout.php">


<button>

Proceed To Checkout

</button>


</a>


</center>




</body>


</html>