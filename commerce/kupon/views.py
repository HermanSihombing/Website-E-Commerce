from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Kupon
from .forms import KuponApplyForm

@require_POST
def kupon_disk(request):
    now = timezone.now()
    form = KuponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            kupon = Kupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['kupon_id'] = kupon.id
        except Kupon.DoesNotExist:
            request.session['kupon_id'] = None
    return redirect('cart:cart_detail')