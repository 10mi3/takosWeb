from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, DeleteView
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
import os
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
from takos.settings import EMAIL_HOST_USER
from website.forms import MessageForm, RegisterForm
from website.models import Gallery, Pro, Actualites, Aboutus, Criteria, Service, Homeimg, Item, OrderItem, Order, Category, Contact, Message, CartItems
# Create your views here.
import random
import string

def file_response_download(request, file_path):
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404




def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def contactus(request):
    contacts = Contact.objects.all()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            name = request.POST.get("nom")
            subject = request.POST.get("sujet")
            email = request.POST.get("email")
            message = request.POST.get("message")
            recepient = "dimitridarius75@gmail.com"
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                [recepient],
                fail_silently=False,
            )
            # Message.objects.create(name=name, subject=subject, email=email, body=message)
            return render(request, 'contactus.html', context={'contacts': contacts, 'form': form})
    else:
        form = MessageForm()

    return render(request, 'contactus.html', context={'contacts': contacts, 'form': form})

@login_required
def adjust_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    quantity=int(request.POST.get('quantity'))
    get_cartitems = CartItems.objects.filter(item__slug=item.slug, user=request.user).exists()
    if get_cartitems:
        get_cartitems.quantity = quantity
        get_cartitems.save()
    return redirect(reverse('cart'))

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    get_cartitems = CartItems.objects.filter(item__slug=item.slug, user_id=request.user, ordered=False).last()
    if get_cartitems:
        messages.info(request, "Items already exists!!")
    else:
        CartItems.objects.create(item=item, user=request.user, ordered=False)
    return redirect("shop")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    print(item)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            return redirect("order-summary")
        else:
            # add a message saying the user dosent have an order
            return redirect("product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        return redirect("product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            return redirect("order-summary")
        else:
            # add a message saying the user dosent have an order
            return redirect("product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        return redirect("product", slug=slug)
    return redirect("product", slug=slug)



# class HomeView(ListView):
#     template_name = "index.html"
#     queryset = Item.objects.filter(is_active=True)
#     context_object_name = 'items'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            return redirect("/")


class ShopView(ListView):
    model = Item
    paginate_by = 6
    template_name = "solarex/shop.html"

# def ShopView(request):
#     return render(request, "shop.html", {'category': Category.objects.all(), 'item': Item.objects.all()[:6]})


def menuDetail(request, slug):
    item = Item.objects.filter(slug=slug).first()
    criteria = Criteria.objects.filter(item_id=item)
    # criteria = Criteria.objects.filter()
    context = {

        'item': item,
        'criteria': criteria
    }
    return render(request, 'product-detail.html', context)

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(category=category, is_active=True)
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "solarex/category.html", context)


def homeimg(request):
    list = Homeimg.objects.filter(is_visibles=True)
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        homeimg = paginator.page(page)
    except PageNotAnInteger:
        homeimg = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        homeimg = paginator.page(
            paginator.num_pages)  # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, template_name='index.html', context={'homeimg': list})


def actualite(request):
    list = Actualites.objects.filter(is_visibles=True).order_by('-pub_dates')
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        actualite = paginator.page(page)
    except PageNotAnInteger:
        actualite = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        actualite = paginator.page(
            paginator.num_pages)  # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, template_name='events.html', context={'events': list})


def index(request):
    list = Service.objects.filter(is_visibles=True)[:2]
    events = Actualites.objects.all()[:3]
    service = Service.objects.all()[:2]
    homeimg = Homeimg.objects.all()[:1]
    pro = Pro.objects.all()[:2]
    return render(request, template_name='solarex/index.html',
                  context={'service': service, 'events': events, 'homeimg': homeimg, 'pro': pro[:4], 'services': list })


def service(request):
    list = Service.objects.filter(is_visibles=True)

    return render(request, template_name='services.html', context={'services': list})


def mentor(request):
    mentors = Mentor.objects.all()
    return render(request, template_name='mentor.html', context={'mentors': mentors})


def event(request):
    events = Actualites.objects.all()
    return render(request, template_name='events.html', context={'events': events})


def gallery(request):
    gallery = Gallery.objects.all()
    return render(request, template_name='gallery.html', context={'gallery': gallery})


def project(request):
    pro = Pro.objects.all()
    return render(request, template_name='projects.html', context={'pro': pro})


def aboutus(request):
    aboutus = Aboutus.objects.all()
    return render(request, template_name='aboutus.html', context={'aboutus': aboutus})

# other stuff



def view_404(request, exception):
    return redirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'index.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'login.html',
                          {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login.html')


def signup_view(request):
    # if this is a POST request we need to process the form data
    template = 'signup.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            print("ici")
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()

                # Login the user
                login(request, user)

                # redirect to accounts page:
                return render(request, 'index.html', {'form': form})

    # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user, ordered=False)
    bill = cart_items.aggregate(Sum('item__price'))
    number = cart_items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    context = {
        'cart_items': cart_items,
        'total': total,
        'count': count,
    }
    return render(request, 'cart.html', context)


class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = 'cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.user:
            cart.delete()
            return redirect("cart")
        return redirect("cart")


@login_required
def order_item(request):
    cart_items = CartItems.objects.filter(user=request.user, ordered=False)
    ordered_date = timezone.now()
    cart_items.update(ordered=True, ordered_date=ordered_date)
    return redirect("order_details")


@login_required
def order_details(request):
    items = CartItems.objects.filter(user=request.user, ordered=True, status="Active").order_by('-ordered_date')
    cart_items = CartItems.objects.filter(user=request.user, ordered=True, status="Delivered").order_by('-ordered_date')
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    pieces = items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    total_pieces = pieces.get("item__pieces__sum")
    context = {
        'items': items,
        'cart_items': cart_items,
        'total': total,
        'count': count,
        'total_pieces': total_pieces
    }
    return render(request, 'order_details.html', context)