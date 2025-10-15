"""
Hangarin Task Management System - Views
Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): 2025-10-14 04:03:58
Current User's Login: hizoo5
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Task, Category, Priority, SubTask, Note
from .forms import TaskForm, SubTaskForm, SubTaskWithParentForm, CategoryForm, PriorityForm, NoteForm


def home(request):
    """Dashboard home view"""
    all_tasks = Task.objects.all()
    
    # Get all categories and priorities for stats
    categories = Category.objects.all()
    priorities = Priority.objects.all()
    
    # Build category stats
    category_stats = []
    for category in categories:
        category_tasks = all_tasks.filter(category=category)
        category_stats.append({
            'name': category.name,
            'total': category_tasks.count(),
            'pending': category_tasks.filter(status='Pending').count(),
            'in_progress': category_tasks.filter(status='In Progress').count(),
            'completed': category_tasks.filter(status='Completed').count(),
        })
    
    # Build priority stats
    priority_stats = []
    for priority in priorities:
        priority_tasks = all_tasks.filter(priority=priority)
        priority_stats.append({
            'name': priority.name,
            'total': priority_tasks.count(),
            'pending': priority_tasks.filter(status='Pending').count(),
            'in_progress': priority_tasks.filter(status='In Progress').count(),
            'completed': priority_tasks.filter(status='Completed').count(),
        })
    
    context = {
        'total_tasks': all_tasks.count(),
        'pending_tasks': all_tasks.filter(status='Pending').count(),
        'in_progress_tasks': all_tasks.filter(status='In Progress').count(),
        'completed_tasks': all_tasks.filter(status='Completed').count(),
        'recent_tasks': all_tasks.select_related('category', 'priority').order_by('-created_at')[:5],
        'categories': categories,
        'priorities': priorities,
        'category_stats': category_stats,
        'priority_stats': priority_stats,
    }
    return render(request, 'home.html', context)


class TaskListView(ListView):
    """Display list of all tasks"""
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get_queryset(self):
        qs = super().get_queryset().select_related('category', 'priority')
        
        # Apply search filter
        query = self.request.GET.get('q')
        if query:
            # Search in text fields and convert deadline to string for searching
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(priority__name__icontains=query) |
                Q(status__icontains=query) |
                Q(deadline__icontains=query)  # Searches deadline as string (YYYY-MM-DD format)
            )
        
        # Apply ordering
        order_by = self.request.GET.get('order_by', '-created_at')
        if order_by:
            qs = qs.order_by(order_by)
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '-created_at')
        return context

class TaskCreateView(CreateView):
    """Create a new task"""
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

class TaskUpdateView(UpdateView):
    """Update an existing task"""
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)


class TaskDeleteView(DeleteView):
    """Delete a task"""
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)



# SubTask Views
class SubTaskListView(ListView):
    """Display list of all subtasks"""
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'subtasks'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get_queryset(self):
        qs = super().get_queryset().select_related('parent_task')
        
        # Apply search filter
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(parent_task__title__icontains=query) |
                Q(status__icontains=query)
            )
        
        # Apply ordering
        order_by = self.request.GET.get('order_by', '-created_at')
        if order_by:
            qs = qs.order_by(order_by)
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '-created_at')
        return context

class SubTaskCreateView(CreateView):
    """Create a new subtask from task detail page"""
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get parent task from URL parameter
        task_pk = self.kwargs.get('task_pk')
        if task_pk:
            context['parent_task'] = get_object_or_404(Task, pk=task_pk)
        context['page_title'] = 'Add SubTask'
        return context
    
    def form_valid(self, form):
        # Get parent task from URL parameter
        task_pk = self.kwargs.get('task_pk')
        if task_pk:
            form.instance.parent_task = get_object_or_404(Task, pk=task_pk)
        messages.success(self.request, 'SubTask created successfully!')
        return super().form_valid(form)


class SubTaskCreateWithParentView(CreateView):
    """Create a new subtask with parent task selection"""
    model = SubTask
    form_class = SubTaskWithParentForm
    template_name = 'subtask_form_with_parent.html'
    success_url = reverse_lazy('subtask-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'SubTask created successfully!')
        return super().form_valid(form)


class SubTaskUpdateView(UpdateView):
    """Update an existing subtask"""
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_task'] = self.object.parent_task
        context['page_title'] = 'Edit SubTask'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'SubTask updated successfully!')
        return super().form_valid(form)


class SubTaskDeleteView(DeleteView):
    """Delete a subtask"""
    model = SubTask
    template_name = 'subtask_del.html'
    success_url = reverse_lazy('subtask-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_task'] = self.object.parent_task
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'SubTask deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Category Views
class CategoryListView(ListView):
    """Display list of all categories"""
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories_list'
    paginate_by = 10
    ordering = ['name']
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Apply search filter
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(name__icontains=query))
        
        # Apply ordering
        order_by = self.request.GET.get('order_by', 'name')
        if order_by:
            qs = qs.order_by(order_by)
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'name')
        return context

class CategoryCreateView(CreateView):
    """Create a new category"""
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    """Update an existing category"""
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    """Delete a category"""
    model = Category
    template_name = 'category_del.html'
    success_url = reverse_lazy('category-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Priority deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Note Views
class NoteListView(ListView):
    """Display list of all notes"""
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get_queryset(self):
        qs = super().get_queryset().select_related('task')
        
        # Apply search filter
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(task__title__icontains=query) |
                Q(task__deadline__icontains=query) |  # Search by task's deadline
                Q(created_at__icontains=query)  # Search by note's creation date
            )
        
        # Apply ordering
        order_by = self.request.GET.get('order_by', '-created_at')
        if order_by:
            qs = qs.order_by(order_by)
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '-created_at')
        return context


class NoteCreateView(CreateView):
    """Create a new note"""
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')
    
    def dispatch(self, request, *args, **kwargs):
        self.parent_task = get_object_or_404(Task, pk=kwargs.get('task_pk'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add Note'
        context['parent_task'] = self.parent_task
        return context
    
    def form_valid(self, form):
        form.instance.task = self.parent_task
        messages.success(self.request, 'Note created successfully!')
        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    """Update an existing note"""
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Note'
        context['parent_task'] = self.object.task
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Note updated successfully!')
        return super().form_valid(form)


class NoteDeleteView(DeleteView):
    """Delete a note"""
    model = Note
    template_name = 'note_del.html'
    success_url = reverse_lazy('note-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_task'] = self.object.task
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Note deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Priority Views
class PriorityListView(ListView):
    """Display list of all priorities"""
    model = Priority
    template_name = 'priority_list.html'
    context_object_name = 'priorities_list'
    paginate_by = 10
    ordering = ['name']
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Apply search filter
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(name__icontains=query))
        
        # Apply ordering
        order_by = self.request.GET.get('order_by', 'name')
        if order_by:
            qs = qs.order_by(order_by)
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'name')
        return context

class PriorityCreateView(CreateView):
    """Create a new priority"""
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Priority created successfully!')
        return super().form_valid(form)


class PriorityUpdateView(UpdateView):
    """Update an existing priority"""
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Priority updated successfully!')
        return super().form_valid(form)


class PriorityDeleteView(DeleteView):
    """Delete a priority"""
    model = Priority
    template_name = 'priority_del.html'
    success_url = reverse_lazy('priority-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Priority deleted successfully!')
        return super().delete(request, *args, **kwargs)