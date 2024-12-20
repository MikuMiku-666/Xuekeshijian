<?php
// 数据库配置信息
$servername = "localhost";
$username = "root";
$password = "123456";
$dbname = "anime_db";

// 创建数据库连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 从 users 表中查询所有用户
$result = $conn->query("SELECT username, password FROM users");

// 遍历查询结果
while ($row = $result->fetch_assoc()) {
    // 去除password字段两侧的空格
    $trimmedPassword = trim($row['password']);

    // 检查是否需要更新密码
    if ($row['password'] !== $trimmedPassword) {
        echo "密码两侧有空格，正在更新。<br>";
        
        // 准备更新语句
        $sql = "UPDATE users SET password = ? WHERE username = ?";
        $stmt = $conn->prepare($sql);

        // 检查语句是否准备成功
        if ($stmt === false) {
            die("Prepare failed: " . $conn->error);
        }

        // 绑定参数
        $stmt->bind_param("ss", $trimmedPassword, $row['username']);

        // 执行语句
        if (!$stmt->execute()) {
            die("Execute failed: " . $stmt->error);
        }

        // 关闭预处理语句
        $stmt->close();
    } else {
        echo "密码两侧没有空格。<br>";
    }
}

// 关闭数据库连接
$conn->close();

// 输出成功消息
echo "All passwords have been successfully updated to trimmed values.";
?>