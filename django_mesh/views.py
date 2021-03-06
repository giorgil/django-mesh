# -*- coding: utf-8 -*-
#Copyright (C) 2011 Seán Hayes
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Python imports
import logging

# Django imports
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

# App imports
from .models import Channel, Post, Tag

logger = logging.getLogger(__name__)

class IndexView(ListView):
    model = Post
    template_name = 'django_mesh/index.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        ret = super(IndexView, self).get_queryset(*args, **kwargs)
        return ret.get_for_user(user=self.request.user).active()

class ChannelIndexView(ListView):
    model = Channel
    template_name = 'django_mesh/channel_index.html'
    context_object_name = 'channel_list'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        qs = super(ChannelIndexView, self).get_queryset(*args, **kwargs)
        return qs.get_for_user(self.request.user)

class ChannelDetailView(ListView):
    model = Post
    template_name = 'django_mesh/channel_view.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel.objects.get_for_user(user=self.request.user), slug=self.kwargs['slug'])
        response = super(ChannelDetailView, self).dispatch(request, *args, **kwargs)
        return response

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        ret = super(ChannelDetailView, self).get_queryset(*args, **kwargs)

        if ((self.channel.public) or (user in self.channel.followers.all())):
            return ret.filter(channel=self.channel).active()
        else:
            return ret.none()

    def get_context_data(self, **kwargs):
        context = super(ChannelDetailView, self).get_context_data(**kwargs)
        context['channel'] = self.channel
        return context

class PostIndexView(ListView):
    model = Post
    template_name = 'django_mesh/post_index.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        ret = super(PostIndexView, self).get_queryset(*args, **kwargs)
        return ret.get_for_user(user=self.request.user).active()

class PostDetailView(DetailView):
    model = Post
    template_name = 'django_mesh/post_view.html'
    context_object_name = 'post'

    def get_queryset(self, *args, **kwargs):
        ret = super(PostDetailView, self).get_queryset(*args, **kwargs)
        return ret.get_for_user(user=self.request.user).active()

def self_enrollment(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        channel = get_object_or_404(Channel.objects.get_for_user(user), slug=kwargs['slug'])
        channel.followers.add(user)
        return HttpResponseRedirect(reverse('mesh_channel_index'))
    else:
        return HttpResponseRedirect(reverse('mesh_channel_index'))

class TagDetailView(ListView):
    model = Post
    template_name = 'django_mesh/tag_view.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):

        self.tag = get_object_or_404(Tag.objects.all(), slug=kwargs['slug'])
        response = super(TagDetailView, self).dispatch(request, *args, **kwargs)
        return response

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        ret = super(TagDetailView, self).get_queryset(*args, **kwargs).get_for_user(user).filter(tags=self.tag).distinct()

        if len(ret) == 0:
            raise Http404
        return ret

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class TagIndexView(ListView):
    model = Tag
    template_name = 'django_mesh/tag_index.html'
    context_object_name = 'tag_list'

    def get_queryset(self, *args, **kwargs):
        qs = super(TagIndexView, self).get_queryset(*args, **kwargs)
        return qs.get_for_user(self.request.user)