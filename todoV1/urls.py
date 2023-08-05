from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('todos', views.TodoItemViewSet)

todosRouter = routers.NestedDefaultRouter(router, 'todos', lookup='todos')
todosRouter.register('reviews', views.ReviewViewSet, 'todos-reviews')

# urlpatterns = router.urls + productsRouter.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(todosRouter.urls))
]
