"""Определяет схемы URL для learning_logs."""
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from . import views


app_name = 'learning_logs'

urlpatterns = [
    # Домашняя страница
    path('', views.index, name='index'),
    # Страница со списком всех тем.
    path('topics/', views.Topics.as_view(), name='topics'),
    # Страница с подробной информацией по отдельной теме
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Страница для добавления новой темы
    path('new_topic/', views.new_topic, name='new_topic'),
    # Страница для добавления новой записи
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Страница для редактирования записи
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # Страница для чтения записи
    path('read_entry/<int:entry_id>/', views.read_entry, name='read_entry'),
    # Страница для удаления записи
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # Страница для редактирования темы
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    # Страница для удаления темы
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    # Страница для поиска темы по названию
    path('search_entries/', views.SearchEntries.as_view(), name='search_entries'),
    path('search_topics/', views.SearchTopics.as_view(), name='search_topics'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
