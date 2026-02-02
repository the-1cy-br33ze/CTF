<?php
session_start();

if (!isset($_SESSION['username'])) {
    header('Location: login.php');
    exit;
}

if (isset($_SESSION['role']) && $_SESSION['role'] === 'admin') {
    header('Location: admin.php');
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secret Corp | Dashboard</title>
    <style>
        /* Аналогичные стили как в admin.php, но с другим контентом */
    </style>
</head>
<body>
    <div class="container">
        <h2>User Dashboard</h2>
        <p>Welcome, <?php echo htmlspecialchars($_SESSION['username']); ?>!</p>
        <p>Your role: <?php echo htmlspecialchars($_SESSION['role']); ?></p>
        <a href="logout.php">Logout</a>
    </div>
</body>
</html>