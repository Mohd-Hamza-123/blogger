from django.shortcuts import render
from practice.forms import DemoForm
# Create your views here.
def demo_form_view(request):
    # print(request.method)
    fm = DemoForm()

    context = {
        "form": fm
    }
    return render(request, 'practice/forms.html', context=context)