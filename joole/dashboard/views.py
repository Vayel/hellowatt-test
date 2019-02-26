import calendar
import statistics

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ClientForm
from .models import Conso_eur, Conso_watt


class ClientFormView(View):
    def get(self, request):
        return render(request, 'dashboard/accueil.html')

    def post(self, request):
        form = ClientForm(request.POST)

        if form.is_valid():
            client_id = form.cleaned_data['client']
            return redirect('dashboard:results', client_id=client_id)


def read_consumption(model, client_id):
    cons = model.objects.filter(
        client_id=client_id
    ).order_by("-year")[:settings.MAX_YEARS_DISPLAYED]
    if not cons:
        raise ValueError(
            f"Aucune donnée de consommation pour le client n°{client_id}"
        )
    return list(reversed(cons))


def compute_heating_conso_rel_delta(conso):
    mean_heating = statistics.mean([
        c for i, c in enumerate(conso) if i in settings.HEATING_MONTHS
    ])
    mean_not_heating = statistics.mean([
        c for i, c in enumerate(conso) if i not in settings.HEATING_MONTHS
    ])
    return (mean_heating - mean_not_heating) / mean_not_heating


def find_dysfunction_month(conso):
    prev, cur = conso
    for i, (cons_prev, cons_cur) in enumerate(zip(prev, cur)):
        delta = abs((cons_cur - cons_prev) / cons_prev)
        if delta > settings.DYSFUNCTION_CONS_REL_DELTA:
            return i
    return -1


def results(request, client_id):
    try:
        client_id = int(client_id)
    except (TypeError, ValueError):
        return HttpResponseBadRequest(
            f"'{client_id}' n'est pas un identifiant valide."
        )

    try:
        conso_euro = read_consumption(Conso_eur, client_id)
    except ValueError as e:
        return HttpResponseNotFound(str(e))

    try:
        conso_watt = read_consumption(Conso_watt, client_id)
    except ValueError as e:
        return HttpResponseNotFound(str(e))
    conso_watt = list(map(list, conso_watt))

    heating_conso_rel_delta = compute_heating_conso_rel_delta(conso_watt[-1])

    dysfunction = None
    if len(conso_watt) > 1:
        dysfunction_month = find_dysfunction_month(conso_watt[-2:])
        if dysfunction_month >= 0:
            dysfunction = calendar.month_name[dysfunction_month + 1]

    context = {
        "years": [conso.year for conso in conso_euro],
        "conso_euro": list(map(list, conso_euro)),
        "conso_watt": conso_watt,
        "heating_conso_rel_delta": int(heating_conso_rel_delta * 100),
        "is_elec_heating": heating_conso_rel_delta > settings.ELEC_HEATING_REL_DELTA,
        "dysfunction": dysfunction,
    }
    return render(request, 'dashboard/results.html', context)
