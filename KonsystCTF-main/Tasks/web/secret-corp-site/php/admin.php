<?php
session_start();

if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'admin') {
    session_destroy();
    header('Location: index.php');
    exit;
}

$flag = "flag{!N0_WAY_U_CAN!}";
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secret Corp | Admin Panel</title>
    <style>
        :root {
            --primary: #6c5ce7;
            --dark: #2d3436;
            --light: #f5f6fa;
            --success: #00b894;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            padding: 40px;
            width: 100%;
            max-width: 600px;
            text-align: center;
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        h2 {
            color: var(--dark);
            margin-bottom: 30px;
            font-size: 32px;
        }
        
        .flag-container {
            background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
        .flag-container p {
            color: var(--dark);
            font-size: 18px;
            margin-bottom: 15px;
        }
        
        .flag {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            font-size: 24px;
            font-weight: bold;
            color: var(--success);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        a {
            display: inline-block;
            padding: 12px 25px;
            background-color: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        a:hover {
            background-color: #5649c0;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 92, 231, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Admin Panel</h2>
        <div class="flag-container">
            <p>Congratulations! Here's your flag:</p>
            <div class="flag"><?php echo $flag; ?></div>
        </div>
        <a href="logout.php">Logout</a>
    </div>
</body>
</html>