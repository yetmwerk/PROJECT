<?php

session_start();

include "api/db.php";


// Get food items

$sql = "
SELECT * FROM foods
WHERE status='available'
LIMIT 6
";


$result = $conn->query($sql);


?>


<!DOCTYPE html>

<html>

<head>

<title>
Food Ordering System
</title>


<link rel="stylesheet" href="assets/css/styles.css">


</head>


<body>


<!-- Navigation -->

<nav>


<h2>
FoodExpress
</h2>


<a href="index.php">
Home
</a>
<a href="cart.php">
Cart
</a>
<a href="order_history.php">
My Orders
</a>

<a href="menu.php">
Menu
</a>


<?php if(isset($_SESSION['user_id'])){ ?>


<span>

Welcome 
<?php echo $_SESSION['name']; ?>

</span>


<a href="order_history.php">
My Orders
</a>


<a href="logout.php">
Logout
</a>


<?php }else{ ?>


<a href="login.php">
Login
</a>


<a href="register.php">
Register
</a>


<?php } ?>


</nav>



<!-- Hero Section -->


<section class="hero">


<h1>
Delicious Food Delivered To You
</h1>


<p>
Order your favorite meals online
</p>


<a href="menu.php">

<button>
View Menu
</button>

</a>


</section>




<!-- Featured Foods -->


<h2 class="title">

Popular Foods

</h2>



<div class="food-container">


<?php while($food=$result->fetch_assoc()){ ?>


<div class="food-card">



<img 
src="assets/images/<?php echo $food['image']; ?>"
width="200"
height="150"
>



<h3>

<?php echo $food['food_name']; ?>

</h3>



<p>

<?php echo $food['description']; ?>

</p>



<h4>

$<?php echo $food['price']; ?>

</h4>



<a href="cart.php?add=<?php echo $food['food_id']; ?>">


<button>

Add To Cart

</button>


</a>



</div>


<?php } ?>


</div>



</body>

</html>