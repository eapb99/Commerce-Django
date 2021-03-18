from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView
from .forms import ListingForm, CommentForm, BidForm
from .models import *


class Index(ListView):
    paginate_by = 12
    model = Listing
    template_name = 'listings/listlisting.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.filter(lis_active=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active Listing'
        context['name_page'] = 'HomePage'
        return context

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        if username == '':
            return render(request, "auctions/register.html", {
                "message": "Username cannot be blank"
            })
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class ListingCreateView(CreateView):
    model = Listing
    template_name = 'listings/create.html'
    form_class = ListingForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def __init__(self):
        super(ListingCreateView, self).__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = 'Create Listing'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.lis_user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        p = super().form_invalid(form)
        return p


class ListingDetailView(DetailView, FormView):
    model = Listing
    template_name = 'listings/listingdetail.html'
    form_class = CommentForm
    success_url = reverse_lazy('view')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        arg = self.object.pk
        return reverse('view', args=(arg,))

    def get_object(self):
        try:
            instance = self.model.objects.get(pk=self.kwargs['pk'])
        except Exception as e:
            raise e
        return instance

    def get_comments(self):
        try:
            instance = Comment.objects.filter(listings=self.kwargs['pk'])
        except Exception as e:
            raise e
        return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['object'] = self.get_object()
        context['comments'] = self.get_comments()
        context['watch'] = self.watchlist()
        context['bid'] = Bid.objects.filter(listings=self.kwargs['pk']).order_by('initial').last()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.get_object().pk
        kwargs['user'] = self.request.user.id
        kwargs['pk'] = pk
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def watchlist(self):
        return True if self.request.user in self.object.watchlist.all() else False


class ListingListView(ListView):
    paginate_by = 12
    model = Listing
    template_name = 'listings/listlisting.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.filter(watchlist=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'WatchList'
        context['name_page'] = 'WatchlistPage'
        return context


class CategoryListView(ListView):
    paginate_by = 3
    model = Category
    template_name = 'category/listcategory.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categories'
        context['name_page'] = 'CategoryPage'
        return context


class CategoryListingContent(ListView):
    paginate_by = 12
    model = Listing
    template_name = 'listings/listlisting.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Listing.objects.filter(category=self.kwargs['pk']).filter(lis_active=True)
        return qs


# class BidCreateView(CreateView):
#     form_class = BidForm
#     template_name = 'bid/bid.html'
#
#     def get_success_url(self):
#         arg = self.kwargs['pk']
#         return reverse('view', args=(arg,))
#
#     def get_listing(self):
#         try:
#             instance = Listing.objects.get(pk=self.kwargs['pk'])
#         except Exception as e:
#             raise e
#         return instance
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['foo'] = self.get_object()
#         context['bid'] = self.bid()
#         return context
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         pk = self.get_object().pk
#         kwargs['user'] = self.request.user.id
#         kwargs['pk'] = pk
#         return kwargs
#
#     def post(self, request, *args, **kwargs):
#         obj = self.get_listing()
#         self.object = self.get_listing()
#         bid = Bid.objects.filter(listings=kwargs['pk'])
#         value = float(request.POST['initial'])
#         if bid.exists():
#             if value > bid.order_by('-initial').first().initial:
#                 obj.lis_price = value
#                 obj.save()
#                 form = self.get_form()
#                 if form.is_valid():
#                     form.save()
#                     return redirect(self.get_success_url())
#             else:
#                 return self.other(request)
#         else:
#             if value >= obj.lis_price:
#                 obj.lis_price = value
#                 obj.save()
#                 form = self.get_form()
#                 if form.is_valid():
#                     form.save()
#                     return redirect(self.get_success_url())
#             else:
#                 return self.other(request)
#
#     def other(self, request):
#         context = self.get_context_data()
#         context['error'] = 'Your bid must be higher than the price'
#         return render(request, self.template_name, context)
#
#     def bid(self):
#         bid = Bid.objects.filter(listings=self.kwargs['pk'])
#         if bid.exists():
#             return bid.order_by('-initial').first()
#         else:
#             return ''
#
#
#
#     def form_valid(self, form):
#         self.object= form.save()
#         return super(BidCreateView, self).form_valid()

def make(request, pk):
    if request.method == "POST":
        value = float(request.POST['initial'])
        listing = Listing.objects.get(pk=pk)
        bid = Bid.objects.filter(listings=listing.pk)
        if bid.exists():
            last = bid.order_by('-initial').first()
            return response_bid(request, value, last.initial, listing)
        else:
            return response_bid(request, value, listing.lis_price, listing)

    else:
        listing = Listing.objects.get(pk=pk)
        return render(request, "bid/bid.html", {
            'foo': listing,
            'last': Bid.objects.filter(listings=listing.pk).order_by('-initial').first(),
            'form': BidForm()
        })


def response_bid(request, value, price, listing):
    if value > price:
        form = Bid(initial=value, user=request.user, listings=listing)
        listing.lis_price = value
        listing.save()
        form.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
            "foo": listing,
            "message": "Your bid is less than the current price",
            'form': BidForm()
        }
        return render(request, "bid/bid.html", context)


def add_watch(request, pk):
    if request.method == "POST":
        listing = Listing.objects.get(pk=pk)
        user = User.objects.get(pk=request.user.pk)
        listing.watchlist.add(user.pk)
        return HttpResponseRedirect(reverse("view", args=(pk,)))


def remove_watch(request, pk):
    if request.method == "POST":
        listing = Listing.objects.get(pk=pk)
        user = User.objects.get(pk=request.user.pk)
        listing.watchlist.remove(user.pk)
        return HttpResponseRedirect(reverse("view", args=(pk,)))


def close(request, pk):
    if request.method == "POST":
        listing = Listing.objects.get(pk=pk)
        listing.lis_active =False
        listing.save()
        return HttpResponseRedirect(reverse("view", args=(pk,)))

