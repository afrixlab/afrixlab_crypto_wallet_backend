from kombu import Queue


class CeleryQueue:
    class Definitions:
        EMAIL_NOTIFICATION = "email-notification"
        BEATS = "beats"

    @staticmethod
    def queues():
        return tuple(
            (Queue(getattr(CeleryQueue.Definitions, item)))
            for item in filter(
                lambda ref: not ref.startswith("_"), dir(CeleryQueue.Definitions)
            )
        )
