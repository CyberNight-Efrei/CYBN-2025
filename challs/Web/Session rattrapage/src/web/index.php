<?php
session_start();

if (!isset($_SESSION["userId"])) {
    header("Location: login.php");
    exit();
}

try {
    $db = new PDO('sqlite:db.sqlite');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $db->prepare("SELECT course, grade FROM grades WHERE user_id = :id");
    $stmt->execute([':id' => $_SESSION["userId"]]);
    $grades = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    die("Database error: " . htmlspecialchars($e->getMessage()));
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>My Grades</title>
<style>
    body{font-family:Inter,system-ui,Arial;background:#f3f4f6;margin:0;}
    header{background:#2b7cff;color:white;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;}
    a.btn{background:#fff;color:#2b7cff;text-decoration:none;padding:6px 10px;border-radius:6px;font-weight:600;}
    .container{max-width:900px;margin:20px auto;background:#fff;padding:20px;border-radius:12px;box-shadow:0 4px 10px rgba(0,0,0,.05);}
    table{width:100%;border-collapse:collapse;}
    th,td{padding:10px;text-align:left;border-bottom:1px solid #e5e7eb;}
    th{color:#6b7280;}
</style>
</head>
<body>
<header>
    <div>👋 Hello, <?php echo htmlspecialchars($_SESSION["username"]); ?></div>
    <div>
        <a href="settings.php" class="btn">Settings</a>
        <a href="logout.php" class="btn" style="background:#ef4444;color:white;">Logout</a>
    </div>
</header>

<div class="container">
    <h2>Your Grades</h2>
    <?php if (empty($grades)): ?>
        <p>No grades found yet.</p>
    <?php else: ?>
    <table>
        <tr><th>Course</th><th>Grade</th></tr>
        <?php foreach ($grades as $g): ?>
            <tr>
                <td><?= htmlspecialchars($g["course"]) ?></td>
                <td><?= htmlspecialchars($g["grade"]) ?>/20</td>
            </tr>
        <?php endforeach; ?>
    </table>
    <?php endif; ?>
</div>
</body>
</html>
