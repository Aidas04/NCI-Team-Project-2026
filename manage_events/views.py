from django.shortcuts import render

# Create your views here.
def manage_events(request):
    # Render the home page template
    # return HttpResponse("HOME PAGE OK")
    return render(request, 'home/manage_events_page.html')
 