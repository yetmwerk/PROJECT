<?php

session_start();

if(isset($_SESSION['user_id'])){

header("Location:index.php");

exit();

}

?>


<!DOCTYPE html>
<html>

<head>

<title>Login</title>

<link rel="stylesheet" href="assets/css/styles.css">

</head>


<body>


<div class="container">


<h2>User Login</h2>



<form action="api/login.php" method="POST">



<label>Email</label>

<input 
type="email"
name="email"
required>



<label>Password</label>

<input 
type="password"
name="password"
required>



<button type="submit">

Login

</button>



</form>



<p>

Don't have account?

<a href="register.php">

Register

</a>


</p>



</div>


</body>

</html>