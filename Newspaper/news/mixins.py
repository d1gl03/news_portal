from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import Post


class DailyPostLimitMixin:
    post_type = None
    daily_limit = 3

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        today_start = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        user_posts_today = Post.objects.filter(
            author=request.user.author,
            date_posted__gte=today_start,
            post_type=self.post_type
        ).count()

        if user_posts_today >= self.daily_limit:
            raise PermissionDenied(
                f"Достигнут дневной лимит ({self.daily_limit}) публикаций "
                f"для данного типа контента"
            )

        return super().dispatch(request, *args, **kwargs)