from django.shortcuts import render, redirect

def Error403(request, origen):
	return render(request, 'PermisoDenegado.html', {
			'origen': origen 
		})

def Licencias(request):
	return render(request, 'creditos.html')