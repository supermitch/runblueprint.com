from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import PlanForm


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlanForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/plans/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlanForm()

    return render(request, 'plans/plan_form.html', {'form': form})


def thanks(request):
    return render(request, 'plans/thanks.html', {})
