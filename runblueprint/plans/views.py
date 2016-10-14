from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import PlanForm
from . import planner, persister, renderer
from .formdata import FormData
from .models import Plan


def index(request):
    if request.method == 'POST':  # if this is a POST request we need to process the form data
        form = PlanForm(request.POST)  # create a form instance and populate it with data from the request
        if form.is_valid():  # check whether it's valid
            form_data = FormData(form.cleaned_data)
            plan = planner.generate_plan(form_data)

            request.session['plan_id'] = plan.id  # Save plan ID to session

            persister.persist(plan)  # Save plan to disk

            return redirect('download')

    else:  # if a GET (or any other method) we'll create a blank form
        form = PlanForm()

    return render(request, 'plans/plan_form.html', {'form': form})


def download(request):
    if 'plan_id' in request.session:
        context = {'plan_id': request.session['plan_id']}
    else:
        context = {}
    return render(request, 'plans/download.html', context)
