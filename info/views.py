from django.http import HttpResponse
from django.shortcuts import render
import csv



def index(request):
    if request.method == "POST":
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', '안녕', 'B', 'C', '"Testing"', "Here's a quote"])

        return response
    return render(request, 'index.html')
