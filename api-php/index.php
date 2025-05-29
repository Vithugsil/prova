<?php
require_once __DIR__ . '/vendor/autoload.php';
require_once __DIR__ . '/rabbitmq.php';

$method = $_SERVER['REQUEST_METHOD'];
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

$uri = rtrim($uri, '/');

header('Content-Type: application/json');

if ($method === 'GET' && $uri === '/equipments') {
    echo json_encode([
        ["id" => 1, "name" => "Excavator Arm"],
        ["id" => 2, "name" => "Bulldozer Blade"],
        ["id" => 3, "name" => "Crane Hook"],
        ["id" => 4, "name" => "Forklift Forks"],
        ["id" => 5, "name" => "Dump Truck Bed"],
    ]);
} elseif ($method === 'POST' && $uri === '/dispatch') {
    $body = file_get_contents('php://input');
    $host = getenv('RABBITMQ_HOST') ?: 'rabbitmq';
    publishToQueue($host, $body);
    echo json_encode(["status" => "dispatched"]);
} else {
    http_response_code(404);
    echo json_encode(["error" => "Endpoint not found"]);
}
