from django.contrib.auth.mixins import AccessMixin

from tasks.models import Task


class TaskCreatorRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs.get('pk'))
        if task.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
