from django.shortcuts import redirect

def unauth_middleware(get_response):

    def middleware(request):
        if request.session.get('customer_id'):
            return redirect('home')
        
        response = get_response(request)
        return response

    return middleware