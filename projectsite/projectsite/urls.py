"""
URL configuration for projectsite project.

Hangarin Task Management System
Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): 2025-10-14 04:03:58
Current User's Login: hizoo5
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hangarin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),
    path("accounts/", include("allauth.urls")), # allauth routes
    path('', views.home, name='home'),
    
    # Task URLs
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task-add'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    
    # SubTask URLs
    path('subtasks/', views.SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/add/', views.SubTaskCreateWithParentView.as_view(), name='subtask-add-with-parent'),
    path('tasks/<int:task_pk>/subtasks/add/', views.SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<int:pk>/update/', views.SubTaskUpdateView.as_view(), name='subtask-update'),
    path('subtasks/<int:pk>/delete/', views.SubTaskDeleteView.as_view(), name='subtask-delete'),
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Priority URLs
    path('priorities/', views.PriorityListView.as_view(), name='priority-list'),
    path('priorities/add/', views.PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<int:pk>/update/', views.PriorityUpdateView.as_view(), name='priority-update'),
    path('priorities/<int:pk>/delete/', views.PriorityDeleteView.as_view(), name='priority-delete'),
    
    # Note URLs
    path('notes/', views.NoteListView.as_view(), name='note-list'),
    path('notes/add/', views.NoteCreateWithTaskView.as_view(), name='note-add-with-task'),
    path('tasks/<int:task_pk>/notes/add/', views.NoteCreateView.as_view(), name='note-add'),
    path('notes/<int:pk>/update/', views.NoteUpdateView.as_view(), name='note-update'),
    path('notes/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note-delete'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)