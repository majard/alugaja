from django.shortcuts import render, redirect, get_object_or_404
from .models import RealEstate, Profile
from django.views import generic

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ugettext as _

from .forms import PublishHouseForm, SearchNearbyForm, UserForm, ProfileForm

from geopy.geocoders import Nominatim
from geopy import geocoders
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D  # D for distance

from alugaja.settings import DEFAULT_ADDRESS, DISTANCE, LATITUDE, LONGITUDE

def index(request):
    location = (LATITUDE, LONGITUDE)
    num_houses = RealEstate.objects.all().count()
    

    return render(
        request,
        'index.html',
        context = {'num_houses':num_houses},
    )

def view_houses(request):
    distance = DISTANCE
    form = SearchNearbyForm()
    queryset = RealEstate.objects.all()
    
    geolocator = Nominatim()
    location = geolocator.geocode(DEFAULT_ADDRESS)
    number_of_bedrooms = 0
    area = 0
    rent_price = 0
    
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchNearbyForm(request.POST)

        # Check if the form is valid:
        # Also check if a valid geolocation has been found, if not, give a feedback. 
        if form.is_valid():
            # Else process the data in form.cleaned_data as required             
            distance = form.cleaned_data['distance']
            location = geolocator.geocode(form.cleaned_data['address'])
            
            number_of_bedrooms = form.cleaned_data['number_of_bedrooms']            
            area = form.cleaned_data['area']
            rent_price = form.cleaned_data['rent_price']     
    
            queryset = queryset.filter(location__distance_lte=(
                Point(location.longitude, location.latitude), 
                D(km=distance)))

            if 'number_of_bedrooms' in form.changed_data:
                queryset = queryset.filter(number_of_bedrooms__gte=number_of_bedrooms)
                print("bed")

            if 'area' in form.changed_data:
                queryset = queryset.filter(area__gte=area)        
                print("area")

            if 'rent_price' in form.changed_data:
                queryset = queryset.filter(rent_price__lte=rent_price)        
                print("rent_price")
        
    return render(request, 'catalog/realestate_list.html', {'form': form, 'queryset': queryset, 'location': location})
 


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

    return render(request, 'catalog/publish_house.html', {'form': form, 'house': house})

class HouseDetailView(generic.DetailView):
    model = RealEstate
    context_object_name = 'house'

@login_required
def update_house(request, id):

    house = get_object_or_404(RealEstate, pk = id)

    if (request.user.id != house.owner.id):
        return HttpResponseRedirect(reverse('houses') )

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = PublishHouseForm(request.POST, request.FILES or None, None, instance = house)

        if 'delete' in request.POST:
            house.delete()
            return HttpResponseRedirect(reverse('houses') )

        # Check if the form is valid:
        if form.is_valid():

            house = form.save()

            # redirect to a new URL:
            return HttpResponseRedirect(house.get_absolute_url())

    # If this is a GET (or any other method) create the default form and fill with
    # the house parameters
    else:
        form = PublishHouseForm(request.POST or None, instance = house)

    return render(request, 'update_house.html', {'form': form, 'house': house})

@login_required
def update_profile(request, pk):

    print(request.user.pk)
    print(User.objects.get(pk = pk).pk)
    

    if (request.user.pk != User.objects.get(pk = pk).pk):
        return HttpResponseRedirect(reverse('houses') )

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect(request.user.profile.get_update_url())
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def profile(request, pk):
    user_profile, created = Profile.objects.get_or_create(pk = pk)
    
    print("inside the profile view")
    print(user_profile)
    return render(request, 'profiles/profile.html', {'user_profile' : user_profile,})