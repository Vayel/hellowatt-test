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

def results(request, client_id):
    # TODO
    conso_watt = []
    is_elec_heating = True
    dysfunction_detected = False

    try:
        client_id = int(client_id)
    except (TypeError, ValueError):
        return HttpResponseBadRequest(
            f"'{client_id}' n'est pas un identifiant valide."
        )

    conso_euro = Conso_eur.objects.filter(
        client_id=client_id
    ).order_by("-year")[:settings.MAX_YEARS_DISPLAYED]
    if not conso_euro:
        return HttpResponseNotFound(
            f"Aucune donnée de dépense pour le client n°{client_id}"
        )
    conso_euro = list(reversed(conso_euro))

    context = {
        "years": [conso.year for conso in conso_euro],
        "conso_euro": list(map(list, conso_euro)),
        # TODO
        "conso_watt": conso_watt,
        "is_elec_heating": is_elec_heating,
        "dysfunction_detected": dysfunction_detected
    }
    return render(request, 'dashboard/results.html', context)
