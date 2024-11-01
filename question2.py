"""
    Ans: is Yes, django signals runs in the same thread
    like below example;
    output look like :
        Sender thread: MainThread
        Receiver thread: MainThread
"""

import threading
from django.dispatch import Signal, receiver

# Define a custom signal
my_signal = Signal()

# Define a receiver function to log the current thread
@receiver(my_signal)
def my_receiver(sender, **kwargs):
    print(f"Receiver thread: {threading.current_thread().name}")

# Trigger the signal and log the thread in the sender
print(f"Sender thread: {threading.current_thread().name}")
my_signal.send(sender=None)
