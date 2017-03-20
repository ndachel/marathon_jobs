<!DOCTYPE html>
<html>
<head>
<title></title>About Page
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Secret Page</h1>
<p>Here is a secret from the DCOS vault:</p>
<?php print_r(getenv('SECRET_ENV_VAR')); ?>

</body>
</html>
