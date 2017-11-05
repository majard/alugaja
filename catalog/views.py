from django.shortcuts import render
from .models import RealEstate
from django.views import generic

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import PublishHouseForm


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
    latitude = -22.912194
    longitude = -43.249910 
    location = (latitude, longitude)
    model = RealEstate
    paginate_by = 10

    distance = 50

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HouseListView, self).get_context_data(**kwargs)
        # Add in more context
        context['distance'] = self.distance
        context['location'] = self.location
        return context

def publish_house(request):
    
    house = RealEstate()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = PublishHouseForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # check if a valid geolocation has been found, if not, give a feedback. 
            # Else process the data in form.cleaned_data as required             
            house.address = form.cleaned_data['address']
            house.owner = request.user
            house.zip_code = form.cleaned_data['zip_code']
            house.publish()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('houses') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = PublishHouseForm()

    return render(request, 'catalog/house_publish.html', {'form': form, 'house': house})