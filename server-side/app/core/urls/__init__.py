from django.urls import path, include
from ._tour_urls import urlpatterns as tour_urls
from ._user_urls import urlpatterns as user_urls
from ._advisor_urls import urlpatterns as advisor_urls
from ._guide_urls import urlpatterns as guide_urls
from ._visitor_urls import urlpatterns as visitor_urls 
from ._review_urls import urlpatterns as review_urls
from ._tour_request_urls import urlpatterns as tour_request_urls
from ._tour_request_batch_urls import urlpatterns as tour_request_batch_urls
from ._tour_report_urls import urlpatterns as tour_report_urls

urlpatterns = [
    path('tour/', include(tour_urls)),
    path('user/', include(user_urls)),
    path('advisor/', include(advisor_urls)),
    path('guide/', include(guide_urls)),
    path('visitor/', include(visitor_urls)),
    path('review/', include(review_urls)),
    path('tour_request/', include(tour_request_urls)),
    path('tour_request_batch/', include(tour_request_batch_urls)),
    path('tour_report/', include(tour_report_urls)),
    ]