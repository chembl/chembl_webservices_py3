from django.conf import settings
from django.http import HttpResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import traceback

@csrf_exempt
def target_predictions_proxy(request):
    if request.method == 'GET':
        return HttpResponse('INVALID USAGE! PLEASE USE POST!\n', status=400)
    elif request.method == 'POST':
        smiles = request.POST.get('smiles', None)
        if smiles is None:
            # noinspection PyBroadException
            try:
                smiles = json.loads(request.body.decode())['smiles']
            except:
                traceback.print_exc()
                return HttpResponse('ERROR: Can not obtain a smiles parameter to be used.\n', status=400)

        proxy_res = requests.get(settings.TARGET_PREDICTION_PROXY_URL,
                                  json={"smiles": smiles})
        if proxy_res.status_code != 200:
            return HttpResponse('ERROR ON PROXY REQUEST.\n{0}\n'.format(proxy_res.content), status=proxy_res.status_code)
        return HttpResponse(proxy_res.content)
