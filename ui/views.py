from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse

@login_required(login_url="/login/")
def dashboard_view(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def portfolio_view(request):
    context = {'segment': 'portfolio'}

    html_template = loader.get_template('home/portfolio.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def analysis_view(request):
    context = {'segment': 'analysis'}

    html_template = loader.get_template('home/analysis.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def populate_view(request):
    context = {'segment': 'populate'}

    html_template = loader.get_template('home/populate.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def tables_view(request):
    context = {'segment': 'tables'}

    html_template = loader.get_template('home/tables.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def billing_view(request):
    context = {'segment': 'billing'}

    html_template = loader.get_template('home/billing.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def notifications_view(request):
    context = {'segment': 'notifications'}

    html_template = loader.get_template('home/notifications.html')
    return HttpResponse(html_template.render(context, request))
