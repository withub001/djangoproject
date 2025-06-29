from django.shortcuts import render, redirect
from .models import Category, Product, Cart
from .forms import RegForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View
import telebot

# Создаем объект бота
bot = telebot.TeleBot('TOKEN')


# Create your views here.
def home_page(request):
    # Достаем данные из БД
    categories = Category.objects.all()
    products = Product.objects.all()

    # Отправляем данные на фронт
    context = {
        'categories': categories,
        'products': products
        }

    return render(request, 'home.html', context)


def category_page(request, pk):
    # Достаем данные из БД
    chosen_category = Category.objects.get(id=pk)
    current_products = Product.objects.filter(product_category=chosen_category)

    # Отправляем данные на фронт
    context = {
        'category': chosen_category,
        'products': current_products
    }

    return render(request, 'category.html', context)


def product_page(request, pk):
    # Достаем данные из БД
    chosen_product = Product.objects.get(id=pk)

    # Отправляем данные на фронт
    context = {
        'product': chosen_product
    }

    return render(request, 'product.html', context)


# Регистрация
class Register(View):
    template_name = 'registration/register.html'

    # Этап 1 - получение формы
    def get(self, request):
        context = {'form': RegForm}
        return render(request, self.template_name, context)


    # Этап 2 - отправка формы
    def post(self, request):
        form = RegForm(request.POST)

        if form.is_valid():
            # Достали данные, которые ввел пользователь
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')

            # Создаем нового пользователя в БД
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Аутентифицируем пользователя
            login(request, user)

            # Переводим пользователя на главную страницу
            return redirect('/')


# Поиск продукта
def search_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        product = Product.objects.filter(product_name__iregex=get_product)

        if product:
            context = {'prompt': get_product,
                       'products': product}
            return render(request, 'result.html', context)
        else:
            return redirect('/')


# Выход из аккаунта
def logout_view(request):
    logout(request)
    return redirect('/')


# Добавление товара в корзину
def add_to_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        if 1 <= int(request.POST.get('pr_amount')) <= product.product_count:
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_pr_amount=int(request.POST.get('pr_amount'))).save()
            return redirect('/')
        return redirect(f'/product/{product.id}')


# Удаление товара из корзины
def del_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    Cart.objects.filter(user_product=product).delete()

    return redirect('/cart')


# Отображение корзины
def cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)
    totals = [round(t.user_product.product_price * t.user_pr_amount, 2) for t in user_cart]

    context = {'cart': user_cart, 'total': round(sum(totals), 2)}

    if request.method == 'POST':
        text = (f'Новый заказ!\n'
                f'Клиент: {User.objects.get(id=request.user.id).email}\n\n')
        for i in user_cart:
            product = Product.objects.get(id=i.user_product.id) # Достали сам товар
            product.product_count = product.product_count - i.user_pr_amount # Посчитали разницу
            product.save(update_fields=['product_count'])
            text += (f'Товар: {i.user_product}\n'
                     f'Количество: {i.user_pr_amount}\n'
                     f'Цена за товары: ${round(i.user_product.product_price * i.user_pr_amount, 2)}\n'
                     f'-----------------------------------------------\n')
        text += f'Итого: ${round(sum(totals), 2)}'
        bot.send_message(6775701667, text)
        user_cart.delete()
        return redirect('/')

    return render(request, 'cart.html', context)