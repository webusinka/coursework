"""
URL configuration for journal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home, submit_test, results, update_performance, edit_testing
from .views import save_testing_changes, get_question_category, add_group, delete_group
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('django_prometheus.urls')),
    path('', home, name='home'),

    path('submit_test/', submit_test, name='submit_test'),
    path('results/', results, name='results'),

    path('update-performance/', update_performance, name='update_performance'),

    path('edit_testing/', edit_testing, name='edit_testing'),
    path('save_testing_changes/', save_testing_changes, name='save_testing_changes'),
    path('get-question-category/<int:question_id>/', get_question_category, name='get_question_category'),

    path('add_group/', add_group, name='add_group'),
    path('delete_group/<int:group_id>/', delete_group, name='delete_group'),
]