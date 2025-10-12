<?php session_start(); ?>

<!doctype html>
<html>
    <head>
        <meta charset='utf-8'>
        <title>Admin</title>
        <style>
            body {
                font-family: Inter, Arial;
                background: #f3f4f6;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(15,23,42,.06);
                max-width:720px;
            }
            .flag {
                font-family: monospace;
                background: #0f1724;
                color: #d1fae5;
                padding: 10px 12px;
                display: inline-block;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class='card'>
            <h2>Admin</h2>
            <p>Flag / secret:</p>
            <div class='flag'>
                <?php
                if (isset($_SESSION["userId"]) && $_SESSION["userId"] == 1) {
                    echo htmlspecialchars($_ENV["FLAG"] ?: "CYBN{flag}");
                } else {
                    echo "Nope...";
                }
                ?>
            </div>
            <p style='margin-top:12px'>
                <a href='index.php'>Back</a>
            </p>
        </div>
    </body>
</html>
