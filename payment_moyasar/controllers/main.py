# -*- coding: utf-8 -*-

import json
import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

import requests
from ast import literal_eval
import webbrowser
import json
import werkzeug.utils
_logger = logging.getLogger(__name__)


class MoyasarController(http.Controller):
    _return_url = '/payment/moyasar/return/'

    @http.route('/payment/txt_action', type="http", auth="public", csrf=False, website=True)
    def Moyasar_action(self, **kw):

        print("hi action", kw)
        return http.request.render("https://api.moyasar.com/v1/payments.html?u=sk_test_GwH7M35mPJW7X5tyiVYDXpZR6ycuhkNafKXUMKyy:", kw)

    @http.route([
        '/payment/moyasar/return',
    ], type='http', auth='public', csrf=False)
    def moyasar_return(self, **post):
        _logger.info('Beginning Moyasar form_feedback with post data %s', pprint.pformat(post))  # debug
        if post.get('authResult') not in ['CANCELLED']:
            request.env['payment.transaction'].sudo().form_feedback(post, 'moyasar')
        return werkzeug.utils.redirect('/payment/process')

    # @http.route([
    #     '/payment/moyasar',
    # ], type='http', auth='public', csrf=False)
    # def moyasar_return(self, **post):
    #     _logger.info('Beginning Moyasar form_feedback with post data %s', pprint.pformat(post))  # debug
    #     if post.get('authResult') not in ['CANCELLED']:
    #         request.env['payment.transaction'].sudo().form_feedback(post, 'moyasar')
    #     return werkzeug.utils.redirect('/payment/process')

    # @http.route('/payment/moyasar', type='http', auth='public',  csrf=False)
    # def sale_details(self, **kwargs):
    #     return request.render('payment_moyasar1.moyasar_merchant_page_pay')



    @http.route('/payment/moyasar', type="http", auth="public", csrf=False,website=True)
    def Moyasar_webform(self, **kw):
        print("Execution Here.........................")
        # # print(self.paymentAmount)
        # print(kw)
        # request_params = json.loads(kw.text)
        # print("hi..",request_params)
        # print("Execution Here.........................2")
        # paymentAmount=kw.get("paymentAmount")
        # description="Purchase From Al Rumaih Company"

        # doctor_rec = request.env['res.partner'].sudo().search([])
        # print("doctor_rec...", doctor_rec)

        kw['txt_action'] ="https://api.moyasar.com/v1/payments.html"
        kw['callback_url'] ="https://alrumaih.co/moyasar/feedback"
        kw['publishable_api_key'] ="pk_test_PFqgvNEjjZADru96KZSmUF1u4UGUMw8d5Tr1MRsB"
        # kw['source[type]'] ="https://api.moyasar.com/v1/payments.html?u=sk_test_GwH7M35mPJW7X5tyiVYDXpZR6ycuhkNafKXUMKyy:"
        kw['Currency'] ="SAR"
        print("hi Moyasar", kw)
        return http.request.render('payment_moyasar.payment_purchase', kw)

    @http.route([
        '/payment/moyasar/notification',
    ], type='http', auth='public', methods=['POST'], csrf=False)
    def moyasar_notification(self, **post):
        tx = post.get('description') and request.env['payment.transaction'].sudo().search([('reference', 'in', [post.get('description')])], limit=1)
        if post.get('eventCode') in ['AUTHORISATION'] and tx:
            states = (post.get('merchantReference'), post.get('success'), tx.state)
            if (post.get('success') == 'true' and tx.state == 'done') or (post.get('success') == 'false' and tx.state in ['cancel', 'error']):
                _logger.info('Notification from Moyasar for the reference %s: received %s, state is %s', states)
            else:
                _logger.warning('Notification from Moyasar for the reference %s: received %s but state is %s', states)
        return '[accepted]'

    def myrequest(self,http_verb, url, data=None):
        moyasar_key = 'sk_test_GwH7M35mPJW7X5tyiVYDXpZR6ycuhkNafKXUMKyy'

        if moyasar_key is None:
            raise Exception('API key must be provided')

        request = {
            'method': 'GET',
            'url': url,
            'auth': (moyasar_key, ''),
            'params':data,
            'headers': {
                'Content-Type': 'application/json'
            }
        }

        # request['params'] = data

        res = requests.request(**request)
        if 400 <= res.status_code <= 404:
            json_string = res.text
            json_dict = json.loads(json_string)
            json_dict["http_code"] = res.status_code
            raise Exception(f'{json.dumps(json_dict)}')
        if 500 <= res.status_code <= 504:
            raise Exception(f'API Error with status code: {res.status_code}')
        return res


    @http.route(['/moyasar/feedback'], type='http', auth='public', website=True, csrf=False)
    def paytabs_feedback(self, **post):
        merchant_detail = request.env["payment.acquirer"].sudo().search([("provider", "=", "moyasar")])
        try:
            # params = {
            #     'merchant_email': merchant_detail.detail_payment_acquire().get('paytabs_merchant_email'),
            #     'secret_key': merchant_detail.detail_payment_acquire().get('paytabs_client_secret'),
            #     'payment_reference': post.get('payment_reference')
            # }

            print(post)
            print("Hello Moyasar ....")


            status = post.get('status')
            print(status)
            amount = post.get('amount')
            print(amount)
            message = post.get('message')
            print(message)
            request_params = post

            id = post.get('id')
            print(id)
            mydata={'id': id}
            try:
                result= self.myrequest('get', 'https://api.moyasar.com/v1/payments/',
                          data=mydata)
            except Exception as e2:
                print(e2)
                print("hi liyah ya shalabi")




            json_dict = json.loads(result.content)
            print(json_dict)
            desc = json_dict['payments'][0]['description']
            # result = requests.get("https://api.moyasar.com/v1/payments/?id=%s&u=sk_test_GwH7M35mPJW7X5tyiVYDXpZR6ycuhkNafKXUMKyy:"%(id),json=mydata, headers=headers).content
            # print("https://api.moyasar.com/v1/payments/?id=%s&u=sk_test_GwH7M35mPJW7X5tyiVYDXpZR6ycuhkNafKXUMKyy:"%(id))
            print("Hi shalbiy ...??")
            print(desc)

            request_params = json_dict['payments'][0]
            request_params['merchantReference'] = desc
            request_params['pspReference'] = id
            print(request_params)

        except Exception as e:
            request_params = {
                'status': 'cancel',
                "reference_no": request.session.get('so_id'),
                'result': 'The payment is cancelled successfully!',
                'response_code': '403'
            }
        # request.session.pop('so_id', None)
        request.env['payment.transaction'].form_feedback(request_params, 'moyasar')
        return werkzeug.utils.redirect('/payment/process')
