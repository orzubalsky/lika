import logging
from django.contrib.sites.models import Site
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from oscar.apps.checkout import views
from oscar.apps.payment import forms, exceptions, models
from shipping.repository import Repository
from paypal.payflow import facade
from oscar.core.loading import get_class
from django.db.models import get_model

Dispatcher = get_class('customer.utils', 'Dispatcher')
CommunicationEvent = get_model('order', 'CommunicationEvent')
CommunicationEventType = get_model('customer', 'CommunicationEventType')

logger = logging.getLogger('oscar.checkout')


class PaymentDetailsView(views.PaymentDetailsView):

    def get_context_data(self, **kwargs):
        # Override method so the bankcard and billing address forms can be added
        # to the context.
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)

        ctx['bankcard_form'] = kwargs.get('bankcard_form', forms.BankcardForm())
        
        ctx['billing_address_form'] = kwargs.get('billing_address_form', forms.BillingAddressForm())

        if self.get_default_billing_address() is not None and kwargs.get('billing_address_form') is None:
            
            # initialize billing address form with user's address
            default_billing_address_form = forms.BillingAddressForm(initial=self.get_default_billing_address().__dict__)            
            
            # pass the updated form to the context
            ctx['billing_address_form'] = default_billing_address_form

        return ctx

    def post(self, request, *args, **kwargs):
        # Override so we can validate the bankcard/billingaddress submission. If
        # it is valid, we render the preview screen with the forms hidden within
        # it.  When the preview is submitted, we pick up the 'action' parameters
        # and actually place the order.
        if request.POST.get('action', '') == 'place_order':
            return self.do_place_order(request)

        bankcard_form = forms.BankcardForm(request.POST)
        billing_address_form = forms.BillingAddressForm(request.POST)

        if not all([bankcard_form.is_valid(), billing_address_form.is_valid()]):
            # Form validation failed, render page again with errors
            self.preview = False
            ctx = self.get_context_data(bankcard_form=bankcard_form,
                                        billing_address_form=billing_address_form)
            return self.render_to_response(ctx)

        # Render preview with bankcard and billing address details hidden
        return self.render_preview(request,
                                   bankcard_form=bankcard_form,
                                   billing_address_form=billing_address_form)

    def do_place_order(self, request):
        # Helper method to check that the hidden forms wasn't tinkered
        # with.
        bankcard_form = forms.BankcardForm(request.POST)
        billing_address_form = forms.BillingAddressForm(request.POST)
        if not all([bankcard_form.is_valid(), billing_address_form.is_valid()]):
            messages.error(request, "Invalid submission")
            return HttpResponseRedirect(reverse('checkout:payment-details'))
        bankcard = bankcard_form.get_bankcard_obj()

        # Attempt to submit the order, passing the bankcard object so that it
        # gets passed back to the 'handle_payment' method below.
        return self.submit(
            request.basket,
            payment_kwargs={'bankcard': bankcard,
                            'billing_address': billing_address_form.cleaned_data})

    def handle_payment(self, order_number, total_incl_tax, **kwargs):
        # Make submission to PayPal.
        try:
            # Using authorization here (two-stage model).  You could use sale to
            # perform the auth and capture in one step.  The choice is dependent
            # on your business model.
            facade.sale(order_number,
                             total_incl_tax,
                             kwargs['bankcard'],
                             kwargs['billing_address'])
        except facade.NotApproved, e:
            # Submission failed
            raise exceptions.UnableToTakePayment(e.message)

        # Record payment source and event
        source_type, is_created = models.SourceType.objects.get_or_create(name='PayPal')
        source = models.Source(source_type=source_type,
                               currency='USD',
                               amount_allocated=total_incl_tax)
        self.add_payment_source(source)
        self.add_payment_event('Authorised', total_incl_tax)

    def send_confirmation_message(self, order, **kwargs):
        code = self.communication_type_code
        site = Site.objects.get_current()

        download_link_url = 'http://%s%s' % (
            site.domain,
            reverse(
                'customer:anon-order-download',
                kwargs={
                    'order_number': order.number,
                    'hashcode': order.verification_hash(),
                },
            )
        )

        ctx = {'order': order,
               'lines': order.lines.all(),
               'download_link_url': download_link_url}

        if not self.request.user.is_authenticated():
            path = reverse('customer:anon-order',
                           kwargs={'order_number': order.number,
                                   'hash': order.verification_hash()})
            ctx['status_url'] = 'http://%s%s' % (site.domain, path)

        try:
            event_type = CommunicationEventType.objects.get(code=code)
        except CommunicationEventType.DoesNotExist:
            # No event-type in database, attempt to find templates for this
            # type and render them immediately to get the messages.  Since we
            # have not CommunicationEventType to link to, we can't create a
            # CommunicationEvent instance.
            messages = CommunicationEventType.objects.get_and_render(code, ctx)
            event_type = None
        else:
            # Create CommunicationEvent
            CommunicationEvent._default_manager.create(
                order=order, event_type=event_type)
            messages = event_type.get_messages(ctx)

        if messages and messages['body']:
            logger.info("Order #%s - sending %s messages", order.number, code)
            dispatcher = Dispatcher(logger)
            dispatcher.dispatch_order_messages(order, messages,
                                               event_type, **kwargs)
        else:
            logger.warning("Order #%s - no %s communication event type",
                           order.number, code)



class ShippingMethodView(views.ShippingMethodView):
    def get_available_shipping_methods(self):
        return Repository().get_shipping_methods(self.request.user, self.request.basket,
                                                 self.get_shipping_address())
