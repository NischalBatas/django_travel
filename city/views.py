from email import message
from multiprocessing import context
from pickle import NONE
from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpResponseRedirect
from calendar import HTMLCalendar
import calendar
from datetime import datetime
from .models import *
from .forms import *
import csv
from django.http import FileResponse
import io
from django.core.paginator import Paginator

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Generate Pdf file
# install pip install reportlab
def venue_pdf(request):
    buf=io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",12)

    venues=Venue.objects.all()
    lines=[]

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.phone)
        lines.append(venue.zip_code)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

        

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf,as_attachment=True,filename='venue.pdf')

def venue_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachmnet; filename=venues.csv'

    writer=csv.writer(response)

    venues=Venue.objects.all()

    writer.writerow(['Venue Name','Address','Zip Code','Phone','Web address','Email'])
    
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_address])

    return response

# download to .txt
def venue_text(request):
    response=HttpResponse(content_type='text/plain')
    response['Content-Disposition']='attachmnet; filename=venues.txt'

    # line=["hello 1\n",
    #         "hello 2"]
    venues=Venue.objects.all()
    
    line=[]
    
    for venue in venues:
        line.append(f'{venue.name}\n{venue.address}\n\n')
    response.writelines(line)
    return response

def index(request,year=datetime.now().year,month=datetime.now().strftime("%B")):
    month=month.capitalize()  # or title, make the month first letter Capital june=June
    # convert month from name to numbers
    month_number=list(calendar.month_name).index(month)
    month_number=int(month_number)

    #create a calendar
    cal=HTMLCalendar().formatmonth(year,month_number)
    dates=datetime.now()
    years=dates.year
    context={
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "dates":dates,
        "years":years
    }
    return render(request,'index.html',context)

def calendars(request,year=datetime.now().year,month=datetime.now().strftime("%B")):
    month=month.capitalize()  # or title, make the month first letter Capital june=June
    # convert month from name to numbers
    month_number=list(calendar.month_name).index(month)
    month_number=int(month_number)

    #create a calendar
    cal=HTMLCalendar().formatmonth(year,month_number)
    dates=datetime.now()
    years=dates.year
    context={
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "dates":dates,
        "years":years
    }
    return render(request,'calendars.html',context)


def events(request):
    events=Event.objects.all()
    paginator=Paginator(events,2)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    event="a"*page_obj.paginator.num_pages
    context={
        # "city":city,
        "page_obj":page_obj,
        "event":event
    }
    return render(request,'events.html',context)

def clickEvent(request,event_id):
    events=Event.objects.get(pk=event_id)
    context={
        "events":events
    }
    return render(request,'show_events.html',context)

def venues(request):
    venues=Venue.objects.all().order_by('name')
    context={
        "venues":venues
    }
    return render(request,'all_venues.html',context)

def show_venues(request,venue_id):
    venues=Venue.objects.get(pk=venue_id)
    context={
        "venues":venues
    }
    return render(request,'show_venues.html',context)
    
def addvenue(request):
    submitted=False
    if request.method=="POST":
        forms=VenueForm(request.POST)
        if forms.is_valid():
            forms.save()
            return HttpResponseRedirect('/addvenue?submitted=True')
    else:
        forms=VenueForm
        if 'submitted' in request.GET:
            submitted =True
        context={
            "forms":forms,
            "submitted":submitted
        }
        return render(request,'Venue_CRUD/addvenue.html',context)

def update_venue(request,venue_id):
    venues=Venue.objects.get(pk=venue_id)
    form=VenueForm(request.POST or None, instance=venues)
    if form.is_valid():
        form.save()
        
        return redirect('venues')
    context={
        "venues":venues,
        "form":form
    }
    return render(request,"Venue_CRUD/update_venue.html",context)

def delete_venue(request,venue_id):
    venues=Venue.objects.get(pk=venue_id)
    venues.delete()
    return redirect('venues')

def addevent(request):
    if request.method=="POST":
        form=eventForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    else:
        form=eventForm
        context={
            "form":form
        }
        return render(request,'Venue_CRUD/addevent.html',context)

def update_event(request,event_id):
    events=Event.objects.get(pk=event_id)
    form=eventForm(request.POST or None,instance=events)
    if form.is_valid():
        form.save()
        return redirect('events')
    context={
        "events":events,
        "form":form
    }
    return render(request,'Venue_CRUD/update_event.html',context)

def delete_event(request,event_id):
    event=Event.objects.get(pk=event_id)
    event.delete()
    return redirect('events')
    
def searchs(request):
    if request.method=='POST':
        searched=request.POST['searchs']
        venues=Venue.objects.filter(address__contains=searched)
        context={
            "searched":searched,
            "venues":venues
        }  
        return render(request,'searchbar.html',context)
    else:
        return render(request,'searchbar.html')
