<?php

session_start();

include "api/db.php";



$search="";


if(isset($_GET['search'])){

$search=$_GET['search'];

}



$sql="
SELECT 

foods.*,
categories.category_name


FROM foods


JOIN categories

ON foods.category_id=categories.category_id


WHERE foods.status='available'


AND foods.food_name LIKE '%$search%'

";



$result=$conn->query($sql);


?>


<!DOCTYPE html>

<html>


<head>


<title>

Food Menu

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


<a href="menu.php">
Menu
</a>


<a href="cart.php">
Cart
</a>



<?php if(isset($_SESSION['user_id'])){ ?>


<span>

<?php echo $_SESSION['name']; ?>

</span>


<a href="logout.php">
Logout
</a>


<?php }else{ ?>


<a href="login.php">
Login
</a>


<?php } ?>


</nav>



<h1 class="title">

Our Food Menu

</h1>



<!-- Search -->


<form method="GET" 
style="text-align:center;">


<input 
type="text"
name="search"
placeholder="Search food..."
value="<?php echo $search;?>"
>


<button>

Search

</button>


</form>




<div class="food-container">


<?php while($food=$result->fetch_assoc()){ ?>



<div class="food-card">


<img

src="assets/images/<?php echo $food['image'];?>"

width="200"

height="150"

>



<h3>

<?php echo $food['food_name'];?>

</h3>



<p>

Category:

<?php echo $food['category_name'];?>

</p>



<p>

<?php echo $food['description'];?>

</p>



<h3>

$<?php echo $food['price'];?>

</h3>




<a href="cart.php?add=<?php echo $food['food_id'];?>">


<button>

Add To Cart

</button>


</a>



</div>


<?php } ?>


</div>



</body>

</html>