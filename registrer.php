<!DOCTYPE html>
<html>

<head>

<title>Customer Registration</title>

<link rel="stylesheet" href="assets/css/styles.css">

</head>


<body>


<div class="container">


<h2>Create Account</h2>


<form action="api/register.php" method="POST">


<label>Full Name</label>

<input 
type="text" 
name="full_name"
required>


<label>Email</label>

<input 
type="email" 
name="email"
required>



<label>Phone</label>

<input 
type="text" 
name="phone"
required>



<label>Password</label>

<input 
type="password"
name="password"
required>



<button type="submit">

Register

</button>


</form>


<p>
Already have account?

<a href="login.php">
Login
</a>

</p>


</div>



</body>

</html>