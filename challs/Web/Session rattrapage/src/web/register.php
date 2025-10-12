<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST["username"] ?? '');
    $password = $_POST["password"] ?? '';
    $hashed_password = password_hash($password, PASSWORD_BCRYPT);

    try {
        $db = new PDO('sqlite:db.sqlite');
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $stmt = $db->prepare('INSERT INTO users (username, password) VALUES (:username, :password)');
        $stmt->execute([':username' => $username, ':password' => $hashed_password]);
        $userId = $db->lastInsertId();

        // Generate random low grades
        $courses = [
            "Mathematics I",
            "Data Structures",
            "Operating Systems",
            "Computer Networks",
            "English Composition"
        ];
        $ins = $db->prepare('INSERT INTO grades (user_id, course, grade) VALUES (:uid, :course, :grade)');
        foreach ($courses as $c) {
            $ins->execute([
                ':uid' => $userId,
                ':course' => $c,
                ':grade' => random_int(0, 5)
            ]);
        }

        echo "Registration successful! <a href='login.php'>Login</a>";
        exit();
    } catch (PDOException $e) {
        echo "Error: " . htmlspecialchars($e->getMessage());
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Register</title>
<style>
body{font-family:Inter,system-ui,Arial;background:#f3f4f6;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;}
.card{background:white;padding:20px;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.06);width:360px;}
input{width:100%;padding:10px;margin:6px 0;border:1px solid #ddd;border-radius:8px;}
button{width:100%;padding:10px;background:#10b981;color:white;border:0;border-radius:8px;font-weight:700;}
</style>
</head>
<body>
<div class="card">
    <h2>Create account</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Register</button>
    </form>
</div>
</body>
</html>
