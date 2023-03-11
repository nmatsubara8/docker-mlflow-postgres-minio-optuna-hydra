from django.views.generic.base import TemplateView

# Create your views here.
class EmailVerificationSentView(TemplateView):
    template_name = "account/verification_sent.html"
