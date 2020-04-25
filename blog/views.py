from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic.detail import SingleObjectMixin

from .emails import send_new_comment_email
from .models import Post, Comment
from .forms import WysiwygForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = WysiwygForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=context.get('post'))
        context['comment_form'] = CommentForm()
        return context


class CommentCreateView(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.object
        if form.is_valid():
            form.save()
            send_new_comment_email.delay(comment=form.cleaned_data,
                                         receiver=self.object.author.email)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_view', kwargs={'pk': self.object.pk})


class PostComment(View):

    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreateView.as_view()
        return view(request, *args, **kwargs)
