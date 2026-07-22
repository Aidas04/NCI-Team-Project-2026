from django.shortcuts import render

# Create your views here.
def view_accounts(request):
    # Render the home page template
    # return HttpResponse("HOME PAGE OK")
    return render(request, 'home/view_accounts_page.html')