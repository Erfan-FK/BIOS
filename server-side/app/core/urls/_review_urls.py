from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views._review_view import ReviewViewSet
from core.views._review_view import GuideReviewsView

router = DefaultRouter()
router.register('review', ReviewViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('reviews/guide/<int:guide_id>/', GuideReviewsView.as_view(), name='guide-reviews'),
]
