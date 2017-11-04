from django.shortcuts import render
from .models import RealEstate
from django.views import generic

from .forms import PublishHouseForm

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def index(request):
    latitude = -22.912194
    longitude = -43.249910 
    location = (latitude, longitude)
    num_houses = RealEstate.objects.all().count()
    

    return render(
        request,
        'index.html',
        context = {'num_houses':num_houses},
    )

class HouseListView(generic.ListView):
    model = RealEstate
    paginate_by = 10

def publish_house(request):
    
    house = RealEstate()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = PublishHouseForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            house.address = form.cleaned_data['address']
            house.publish()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('houses') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = PublishHouseForm()

    return render(request, 'catalog/house_publish.html', {'form': form, 'house': house})