from django.shortcuts import redirect

def auth_middlware(get_response):

    def middleware(request):
        if not request.session.get('customer_id'):
            return redirect('login')

        response = get_response(request)
        return response

    return middleware