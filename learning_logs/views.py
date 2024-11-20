from django.shortcuts import render, redirect
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
#This was updated
from django.urls import reverse

from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """Home page for learning log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic (request, topic_id):
    """Show single topic and all entries"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic.owner, request.user)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, "entries": entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Adding a new topic"""
    if request.method != 'POST':
        # No data submitted create blank form
        form = TopicForm()

    else:
        #Post submitted process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
        
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adding a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #no data create blank form
        form = EntryForm()
    else:
        #post data submitted process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
        
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    #restricting topics to thier owners
    check_topic_owner(topic.owner, request.user)

    if request.method != 'POST':
        #prefill form with the current entry
        form = EntryForm(instance=entry)
    
    else: 
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            check_topic_owner(topic.owner, request.user)
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(owner, current_user):
    """Check if topic is the users"""
    if owner != current_user:
        raise Http404
    else:
        pass