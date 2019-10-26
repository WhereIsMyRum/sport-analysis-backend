#!/usr/bin/env python
import pika, json, re
from abc import ABC, abstractmethod

class c_rabbitWrapper(ABC) :
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbit.docker"))
        self.channel = self.connection.channel()

        self.queues_dict = {}
        self.exchanges_dict = {}

    def publish(self, routing_key, body, exchange='') :
        self.channel.basic_publish(exchange, routing_key=routing_key, body=body)

    def getChannel(self) :
        return self.connection.channel()

    def declare_exchange(self, exchange, exchange_type) :
            self.exchanges_dict[exchange] = self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

    def declare_queue(self, queue_name, exclusive=False) :
        self.queues_dict[queue_name] = self.channel.queue_declare(queue=queue_name, exclusive=exclusive)

    def bind_queue(self, exchange, queue_name) :
        self.channel.queue_bind(exchange=exchange, queue=self.queues_dict[queue_name].method.queue)

    def bind_consume(self, callback, queue_name, auto_ack=True) :
        self.channel.basic_consume(on_message_callback=callback, queue=self.queues_dict[queue_name].method.queue, auto_ack=auto_ack)

    def consume(self) :
        self.channel.start_consuming()

    def closeChannels(self) :
        self.channel.close()

    def close(self) :
        self.closeChannels()
        self.connection.close()

    @abstractmethod
    def callback(self, ch, method, properties, body):
        pass