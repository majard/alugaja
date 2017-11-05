from django.shortcuts import render, redirect
from .models import RealEstate
from django.views import generic

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import PublishHouseForm, SearchNearbyForm, ImageForm

from geopy.geocoders import Nominatim
from geopy import geocoders

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
    distance = 10000
    form = SearchNearbyForm()

    def get_context_data(self, **kwargs):

        geolocator = Nominatim()
        default_address = "Rua Conselheiro Otaviano"
        location = geolocator.geocode(default_address)

        # If this is a POST request then process the Form data
        if self.request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            self.form = SearchNearbyForm(self.request.POST)

            # Check if the form is valid:
            # Also check if a valid geolocation has been found, if not, give a feedback. 
            if self.form.is_valid():
                # Else process the data in form.cleaned_data as required             
                self.distance = self.form.cleaned_data['distance']
                geolocator = Nominatim()
                location = geolocator.geocode(self.form.cleaned_data['address'])

        # If this is a GET (or any other method) create the default form.
        else:
            self.form = SearchNearbyForm()            
         
        # Call the base implementation first to get a context
        context = super(HouseListView, self).get_context_data(**kwargs)
        # Add in more context
        context['distance'] = self.distance
        context['location'] = location
        context['form'] = self.form
        return context
 
    def post(self, request, *args, **kwargs):        
        return self.get(request, *args, **kwargs)


@login_required
def publish_house(request):
    
    house = RealEstate()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = PublishHouseForm(request.POST, request.FILES)

        # Check if the form is valid:
        if form.is_valid():
            # check if a valid geolocation has been found, if not, give a feedback. 
            # Else process the data in form.cleaned_data as required    
            house = form.save(commit=False)
            house.owner = request.user
            house.publish()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('houses') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = PublishHouseForm()

    return render(request, 'catalog/house_publish.html', {'form': form, 'house': house})