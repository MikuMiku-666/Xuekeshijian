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

// 准备 SQL 语句，用于更新哈希密码
$sql = "UPDATE users SET hashed_password = ? WHERE username = ?";

// 准备语句
$stmt = $conn->prepare($sql);

// 从 users 表中查询所有用户
$result = $conn->query("SELECT username, password FROM users");

// 遍历查询结果
while ($row = $result->fetch_assoc()) {
    $raw_password = $row['password']; // 从结果中获取明文密码
    $hashed_password = password_hash($raw_password, PASSWORD_DEFAULT); // 生成密码哈希

    // 绑定参数到预处理语句
    $stmt->bind_param("ss", $hashed_password, $row['username']);
    
    // 执行预处理语句，更新数据库中的哈希密码
    $stmt->execute();
}

// 关闭预处理语句
$stmt->close();

// 关闭数据库连接
$conn->close();

// 输出成功消息
echo "All passwords have been successfully updated to hashed values in the new column.";
?>