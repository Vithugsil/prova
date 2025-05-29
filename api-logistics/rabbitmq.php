<?php
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

function publishToQueue($host, $messageBody) {
    $connection = new AMQPStreamConnection($host, 5672, 'guest', 'guest');
    $channel = $connection->channel();

    $channel->queue_declare('logistics_queue', false, false, false, false);

    $msg = new AMQPMessage($messageBody);
    $channel->basic_publish($msg, '', 'logistics_queue');

    $channel->close();
    $connection->close();
}
