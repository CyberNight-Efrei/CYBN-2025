<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"] ?? '';
    $password = $_POST["password"] ?? '';

    try {
        $db = new PDO('sqlite:db.sqlite');
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $stmt = $db->prepare('SELECT * FROM users WHERE username = :username');
        $stmt->bindParam(':username', $username);
        $stmt->execute();

        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        // Verify password
        if ($user && password_verify($password, $user["password"])) {
            $_SESSION["userId"] = $user["id"];
            $_SESSION["username"] = $user["username"];
            header("Location: index.php");
            exit();
        } else {
            $error = "Invalid credentials!";
        }
    } catch (PDOException $e) {
        $error = "Error: " . $e->getMessage();
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login - Grades</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        body{font-family: Inter, system-ui, Arial; background:#f3f4f6; margin:0; display:flex; align-items:center; justify-content:center; min-height:100vh;}
        .wrap{width:420px; padding:20px;}
        .card{background:white; padding:20px; border-radius:12px; box-shadow: 0 8px 24px rgba(15,23,42,0.06);}
        h2{margin:0 0 10px 0;}
        label{display:block; margin-top:12px; font-size:13px; color:#374151;}
        input[type="text"], input[type="password"]{width:calc(100% - 20px); padding:10px; margin-top:6px; border-radius:8px; border:1px solid #e6edf3;}
        button{margin-top:14px; width:100%; padding:10px; border-radius:8px; border:0; background:#2b7cff; color:white; font-weight:700;}
        .muted{color:#6b7280; font-size:13px;}
        .error{color:#ef4444; margin-top:8px; font-weight:600;}
        .small{margin-top:10px; text-align:center;}
        a {color:#2b7cff; text-decoration:none;}
    </style>
</head>
<body>
<div class="wrap">
    <div class="card">
        <h2>Login</h2>
        <div class="muted">Sign in to view and manage your grades.</div>
        <?php if (!empty($error)): ?><div class="error"><?php echo htmlspecialchars($error); ?></div><?php endif; ?>
        <form method="POST" style="margin-top:12px;">
            <label>Username
                <input type="text" name="username" required autocomplete="username">
            </label>
            <label>Password
                <input type="password" name="password" required autocomplete="current-password">
            </label>
            <button type="submit">Login</button>
        </form>

        <div class="small muted">
            New here? <a href="register.php">Create an account</a>
        </div>
    </div>
</div>
</body>
</html>
