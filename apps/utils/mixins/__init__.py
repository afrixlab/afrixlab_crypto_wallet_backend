from rest_framework.response import Response
from rest_framework import status
from abc import ABC, abstractmethod


class CustomRequestDataValidationMixin(ABC):
    @abstractmethod
    def get_required_fields(self):
        pass

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)
            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed
                )
            else:
                handler = self.http_method_not_allowed
            if request.method.lower() in ["post", "patch", "put", "delete", "get"]:
                errors = []
                if request.method.lower() == "get":
                    data = request.GET
                else:
                    data = request.data
                required_fields_res = self.get_required_fields()
                assert callable(required_fields_res) or getattr(
                    required_fields_res, "__iter__"
                ), "'get_required_fields' method must return an iterable or callable"
                if callable(required_fields_res):
                    _, msg = required_fields_res(data)
                    if not _:
                        errors.append(msg)
                else:
                    for field in self.get_required_fields():
                        if not data.get(field):
                            errors.append(f"'{field}' is required")
                if errors:
                    response = Response(
                        data={"errors": errors}, status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    response = handler(request, *args, **kwargs)
            else:
                response = handler(request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class CountListResponseMixin:
    def list(self, request, *args, **kwargs):
        if request.GET.get("count", "").lower() == "true":
            return Response(
                status=status.HTTP_200_OK,
                data={"count": self.filter_queryset(self.get_queryset()).count()},
            )
        return super().list(request, *args, **kwargs)
