from django.contrib.auth import get_user_model
from rest_framework import response, status

from apps.utils.exceptions import QuerySetException


class Utils:
    @staticmethod
    def get_user_or_404(user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            return Utils.error_response(
                status.HTTP_404_NOT_FOUND, message="User %s does not exist" % user_id
            )

    @staticmethod
    def error_response(http_status: int, *, message: str = "", errors: list = []):
        return response.Response(
            status=http_status,
            data={
                "errors": errors,
                "message": message,
            },
        )

    @staticmethod
    def success_response(http_status, *, data: dict = {}):
        return response.Response(status=http_status, data=data)

    @staticmethod
    def get_object_or_raise_error(
        klass,
        custom_error_title: str = "Queryset error",
        custom_error: str = None,
        *args,
        **kwargs
    ):
        queryset = Utils._get_queryset(klass)
        if not hasattr(queryset, "get"):
            klass__name = (
                klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
            )
            raise ValueError(
                "First argument to Utils.get_object_or_raise_error() must be a Model, Manager, "
                "or QuerySet, not '%s'." % klass__name
            )

        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            raise QuerySetException(
                [custom_error_title],
                custom_error
                if custom_error
                else "No %s matches the given query."
                % queryset.model._meta.object_name,
            )

    @staticmethod
    def get_object_or_none_if_not_existing(klass, *args, **kwargs):
        queryset = Utils._get_queryset(klass)
        if not hasattr(queryset, "get"):
            klass__name = (
                klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
            )
            raise ValueError(
                "First argument to Utils.get_object_or_raise_error() must be a Model, Manager, "
                "or QuerySet, not '%s'." % klass__name
            )

        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            return None

    @staticmethod
    def _get_queryset(klass):
        """
        Return a QuerySet or a Manager.
        Duck typing in action: any class with a `get()` method (for
        Utils.get_object_or_raise_error) or a `filter()` method (for get_list_or_404) might do
        the job.
        """
        # If it is a model class or anything else with ._default_manager
        if hasattr(klass, "_default_manager"):
            return klass._default_manager.all()
        return klass

    @staticmethod
    def get_strategy_from_request_data(request):
        return (
            {"strategy_type": request.data.get("strategy")}
            if request.data.get("strategy")
            else {}
        )

    @staticmethod
    def get_strategy_from_query_argument(request):
        return (
            {"strategy_type": request.GET.get("strategy")}
            if request.GET.get("strategy")
            else {}
        )
