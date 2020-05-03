from django.shortcuts import render

# Create your views here.
def take_turn(self):
  print("Taking turn...")

def index(request):
    context = {"data": "HI"}
    return render(request, 'game/index.html', context)
