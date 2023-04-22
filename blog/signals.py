from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile


# вот и сам декоратор

# def receiver(signal, **kwargs):
#     """
#     A decorator for connecting receivers to signals. Used by passing in the
#     signal (or list of signals) and keyword arguments to connect::
#
#         @receiver(post_save, sender=MyModel)
#         def signal_receiver(sender, **kwargs):
#             ...
#
#         @receiver([post_save, post_delete], sender=MyModel)
#         def signals_receiver(sender, **kwargs):
#             ...
#     """
#
#     def _decorator(func):                                     func = create_profile
#         if isinstance(signal, (list, tuple)):
#             for s in signal:
#                 s.connect(func, **kwargs)
#         else:
#             signal.connect(func, **kwargs)                # сигнал связывается с функцией, которую он вызывает
#         return func                                       # **kwards - передаём дальше во внутреннюю функцию
#
#     return _decorator

@receiver(post_save, sender=User)
# post_save - is a signal, which says, that USER has been saved
# sender - Specifies a particular sender to receive signals from.
def create_profile(sender, instance, created, **kwargs):
    if created:  # (отправитель, экземпляр, флаг(создано), доп арг)
        Profile.objects.create(user=instance)

# виды сигналов и как они работают

# from functools import partial
#
# from django.db.models.utils import make_model_tuple
# from django.dispatch import Signal
#
# class_prepared = Signal()
#
#
# class ModelSignal(Signal):
#     """
#     Signal subclass that allows the sender to be lazily specified as a string
#     of the `app_label.ModelName` form.
#     """
#
#     def _lazy_method(self, method, apps, receiver, sender, **kwargs):
#         from django.db.models.options import Options
#
#         # This partial takes a single optional argument named "sender".
#         partial_method = partial(method, receiver, **kwargs)
#         if isinstance(sender, str):
#             apps = apps or Options.default_apps
#             apps.lazy_model_operation(partial_method, make_model_tuple(sender))
#         else:
#             return partial_method(sender)
#
#     def connect(self, receiver, sender=None, weak=True, dispatch_uid=None, apps=None):
#         self._lazy_method(
#             super().connect,
#             apps,
#             receiver,
#             sender,
#             weak=weak,
#             dispatch_uid=dispatch_uid,
#         )
#
#     def disconnect(self, receiver=None, sender=None, dispatch_uid=None, apps=None):
#         return self._lazy_method(
#             super().disconnect, apps, receiver, sender, dispatch_uid=dispatch_uid
#         )
#
#
# pre_init = ModelSignal(use_caching=True)
# post_init = ModelSignal(use_caching=True)
#
# pre_save = ModelSignal(use_caching=True)
# post_save = ModelSignal(use_caching=True)
#
# pre_delete = ModelSignal(use_caching=True)
# post_delete = ModelSignal(use_caching=True)
#
# m2m_changed = ModelSignal(use_caching=True)
#
# pre_migrate = Signal()
# post_migrate = Signal()


# сам сигнал из документации


# class Signal:
#     """
#     Base class for all signals
#
#     Internal attributes:
#
#         receivers
#             { receiverkey (id) : weakref(receiver) }
#     """
#
#     def __init__(self, use_caching=False):
#         """
#         Create a new signal.
#         """
#         self.receivers = []
#         self.lock = threading.Lock()
#         self.use_caching = use_caching
#         # For convenience we create empty caches even if they are not used.
#         # A note about caching: if use_caching is defined, then for each
#         # distinct sender we cache the receivers that sender has in
#         # 'sender_receivers_cache'. The cache is cleaned when .connect() or
#         # .disconnect() is called and populated on send().
#         self.sender_receivers_cache = weakref.WeakKeyDictionary() if use_caching else {}
#         self._dead_receivers = False
#
#     def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
#         """
#         Connect receiver to sender for signal.
#
#         Arguments:
#
#             receiver
#                 A function or an instance method which is to receive signals.
#                 Receivers must be hashable objects.
#
#                 If weak is True, then receiver must be weak referenceable.
#
#                 Receivers must be able to accept keyword arguments.
#
#                 If a receiver is connected with a dispatch_uid argument, it
#                 will not be added if another receiver was already connected
#                 with that dispatch_uid.
#
#             sender
#                 The sender to which the receiver should respond. Must either be
#                 a Python object, or None to receive events from any sender.
#
#             weak
#                 Whether to use weak references to the receiver. By default, the
#                 module will attempt to use weak references to the receiver
#                 objects. If this parameter is false, then strong references will
#                 be used.
#
#             dispatch_uid
#                 An identifier used to uniquely identify a particular instance of
#                 a receiver. This will usually be a string, though it may be
#                 anything hashable.
#         """
#         from django.conf import settings
#
#         # If DEBUG is on, check that we got a good receiver
#         if settings.configured and settings.DEBUG:
#             if not callable(receiver):
#                 raise TypeError("Signal receivers must be callable.")
#             # Check for **kwargs
#             if not func_accepts_kwargs(receiver):
#                 raise ValueError(
#                     "Signal receivers must accept keyword arguments (**kwargs)."
#                 )
#
#         if dispatch_uid:
#             lookup_key = (dispatch_uid, _make_id(sender))
#         else:
#             lookup_key = (_make_id(receiver), _make_id(sender))
#
#         if weak:
#             ref = weakref.ref
#             receiver_object = receiver
#             # Check for bound methods
#             if hasattr(receiver, "__self__") and hasattr(receiver, "__func__"):
#                 ref = weakref.WeakMethod
#                 receiver_object = receiver.__self__
#             receiver = ref(receiver)
#             weakref.finalize(receiver_object, self._remove_receiver)
#
#         with self.lock:
#             self._clear_dead_receivers()
#             if not any(r_key == lookup_key for r_key, _ in self.receivers):
#                 self.receivers.append((lookup_key, receiver))
#             self.sender_receivers_cache.clear()
