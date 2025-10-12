<?php
session_start();

if (!isset($_SESSION["userId"])) {
    header("Location: login.php");
    exit();
}

if (isset($_POST["settings"]) && is_array($_POST["settings"])) {
    $allowedThemes = ["light", "dark"];
    $allowedSizes = ["small", "large"];

    if (in_array($_POST["settings"]["theme"], $allowedThemes) || in_array($_POST["settings"]["font_size"], $allowedSizes)) {
        $_SESSION = array_merge($_SESSION, $_POST["settings"]);
    }

    $saved = true;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Settings - Grades</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        :root{--bg:#f3f4f6; --card:#fff; --accent:#2b7cff; --muted:#6b7280;}
        body { margin:0; font-family: Inter, system-ui, Arial; background:var(--bg); color:#111827; }
        .wrap { max-width:760px; margin:40px auto; padding:16px; }
        .card { background:var(--card); border-radius:12px; padding:18px; box-shadow: 0 8px 24px rgba(15,23,42,0.06); }
        h2{margin:0 0 10px 0;}
        label{display:block; margin-top:12px; font-size:14px; color:#374151;}
        select{padding:8px; margin-top:6px; border-radius:8px; border:1px solid #e6edf3; width:220px;}
        button{margin-top:14px; padding:10px 14px; border-radius:8px; border:0; background:var(--accent); color:white; font-weight:700;}
        .muted{color:var(--muted); font-size:13px;}
        .ok{color: #059669; font-weight:700; margin-top:10px;}
        header{display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;}
        a {color:var(--accent); text-decoration:none;}

        <?php
        if (isset($_SESSION["theme"]) && $_SESSION["theme"] == "dark") {
            echo "body { background: #0f1724; color: #e6eef8; } .card { background: #071029; }";
        }
        if (isset($_SESSION["font_size"]) && $_SESSION["font_size"] == "large") {
            echo "body { font-size:16px; }";
        } else {
            echo "body { font-size:13px; }";
        }
        ?>
    </style>
</head>
<body>
<div class="wrap">
    <div class="card">
        <header>
            <div>
                <h2>Settings</h2>
                <div class="muted">Change theme and font-size for the demo view (saved to session).</div>
            </div>
            <div style="text-align:right;">
                <div class="muted">Signed in as <strong><?php echo htmlspecialchars($_SESSION["username"]); ?></strong></div>
                <div style="margin-top:6px;"><a href="index.php">Back to Grades</a></div>
            </div>
        </header>

        <?php if (!empty($saved)): ?><div class="ok">Settings saved to session.</div><?php endif; ?>

        <form method="POST" style="margin-top:12px;">
            <label for="theme">Theme</label>
            <select name="settings[theme]" id="theme">
                <option value="light" <?php if (isset($_SESSION["theme"]) && $_SESSION["theme"] == "light") echo "selected"; ?>>Lite</option>
                <option value="dark" <?php if (isset($_SESSION["theme"]) && $_SESSION["theme"] == "dark") echo "selected"; ?>>Dark</option>
            </select>

            <label for="font_size">Font Size</label>
            <select name="settings[font_size]" id="font_size">
                <option value="small" <?php if (isset($_SESSION["font_size"]) && $_SESSION["font_size"] == "small") echo "selected"; ?>>Small</option>
                <option value="large" <?php if (isset($_SESSION["font_size"]) && $_SESSION["font_size"] == "large") echo "selected"; ?>>Large</option>
            </select>

            <div>
                <button type="submit">Save Settings</button>
            </div>
        </form>
    </div>
</div>
</body>
</html>
