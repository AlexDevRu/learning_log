from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404


# Create your views here.


def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'learning_logs/index.html')


class Topics(LoginRequiredMixin, ListView):
    template_name = 'learning_logs/topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.filter(owner=self.request.user).order_by('date_added')


@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:read_entry', entry_id=entry_id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def read_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    context = {'entry': entry}
    return render(request, 'learning_logs/entry.html', context)


def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    check_topic_owner(request, entry.topic)
    entry.delete()
    return redirect('learning_logs:topic', topic_id=entry.topic.id)


@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    topic.delete()
    return redirect('learning_logs:topics')


@login_required
def edit_topic(request, topic_id):
    """Редактирует существующую тему."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = TopicForm(instance=topic)
    else:
        # Отправка данных POST; обработать данные.
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)


class Search(LoginRequiredMixin, ListView):

    def get_queryset(self):
        if self.request.GET.get('obj') == 'topic':
            self.template_name = 'learning_logs/topics.html'
            self.context_object_name = 'topics'
            return Topic.objects.filter(Q(text__icontains=self.request.GET.get("q")) & Q(owner=self.request.user))
        elif self.request.GET.get('obj') == 'entry':
            self.template_name = 'learning_logs/topic.html'
            self.context_object_name = 'entries'
            return Entry.objects.filter(Q(text__icontains=self.request.GET.get("q")) &
                                        Q(topic__id=self.request.GET.get("topic_id")))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        if self.request.GET.get('obj') == 'entry':
            context["topic"] = get_object_or_404(Topic, pk=self.request.GET.get("topic_id"))
        return context


class SearchTopics(LoginRequiredMixin, ListView):
    template_name = 'learning_logs/topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.filter(Q(text__icontains=self.request.GET.get("q")) & Q(owner=self.request.user))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context


class SearchEntries(LoginRequiredMixin, ListView):
    template_name = 'learning_logs/topic.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Entry.objects.filter(Q(text__icontains=self.request.GET.get("q")) &
                                    Q(topic__id=self.request.GET.get("topic_id")))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context
