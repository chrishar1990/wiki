from django import forms
from django.http import HttpResponse
from django.shortcuts import render
import random
import markdown2

from . import util

#tasks_list  = []

class NewTaskForm(forms.Form):
    task = forms.CharField(label="Title")
    content_text_area = forms.CharField(
        label="Content", 
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 10
        ,'class': 'my-textarea' }),)
    

def index(request):
    #A test, please delete when done.
    print("List below: ")
    print(util.list_entries())
    lengthofList = len(util.list_entries())
    lengthofList = lengthofList - 1
    randomNumber = random.randint(0, lengthofList)
    print(randomNumber)
    fullList = util.list_entries()
    fullListRandomEntry = fullList[randomNumber]
    print(fullListRandomEntry)
    randomEntry = util.get_entry(fullList[randomNumber])
    print(randomEntry)


    #End of test

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

tasks_list = []



def create_page(request):
    print("View function is running!")  # Debugging: Confirm the view is being called
    allEntries = util.list_entries()
    entryExist = False
    for entry in allEntries:
        print(entry.upper())
    


    if request.method == "POST":
        
        print("Form submitted!")  # Debugging: Confirm the form is being submitted
        form = NewTaskForm(request.POST)
        
        #entryExist = False

        if form.is_valid():
            
            print("Form is valid!")  # Debugging: Confirm the form is valid
            task_title = form.cleaned_data["task"]
            task_content = form.cleaned_data["content_text_area"]
            tasks_list.append({"title": task_title, "content": task_content})
            print(f"Task added: {task_title}  \n Content added:  {task_content}")  # Debugging: Confirm the task is added
            # Redirect or perform some other action
            for entry in allEntries:
                if task_title.upper() == entry.upper():
                    entryExist = True
                    
            
            if(entryExist == False):
                util.save_entry(task_title, task_content)
            else:
                print("Entry already EXIST!!!")
            
        else:
            print("Form is invalid!")  # Debugging: Confirm the form is invalid
            return render(request, "encyclopedia/create_page.html", {
                "form": form
            })
    
    return render(request, "encyclopedia/create_page.html", {
        "form": NewTaskForm(),
        "entry": util.list_entries(),
        "entryExist": entryExist
        
    })



def entry_page(request, title):
    print("What I typed: did it changed? " + title) 
    
    entry = util.get_entry(title)
    print(entry)
    if entry == None:
        
        entry = util.get_entry(title.upper())
        if entry == None:
            return error(request, title)
        else:
            print("Rendering entry_page.html1")
            return render(request, "encyclopedia/entry_page.html",{
             "entry": markdown2.markdown(entry),
              "title": title
        })
        
       
    else:
        print("Rendering entry_page.html2")

        return render(request, "encyclopedia/entry_page.html",{
             "entry": markdown2.markdown(entry),
              "title": title
        })
    

def search_entries(request):
    #print(request.method)
    #title = request.POST['searched']
    title = request.POST.get('searched', '').strip()

    entries = util.list_entries()
    query = title
    results = [entry for entry in entries if query.lower() in entry.lower()]
    print("It is below:")
    if results != []:
        print(results)
    else:
        print("empty")
    if request.method == "POST":
        
        #print(searched + "\tThe entry below: ")
        entry = util.get_entry(title)
        if entry is not None:
            return render(request, "encyclopedia/entry_page.html",{
             "entry": markdown2.markdown(entry),
              "title": title
            })

        if entry == None:
            entry = util.get_entry(title.upper())
            if entry is not None:
                return render(request, "encyclopedia/entry_page.html",{
                "entry":markdown2.markdown(entry),
                "title": title
                })
            
        if entry == None:
            entry = util.get_entry(title.capitalize())
            #print(title.capitalize())
            #print(entry)
            if entry is not None:
                return render(request, "encyclopedia/entry_page.html",{
                "entry": markdown2.markdown(entry),
                "title": title,
                "results": results,

                })
        return render(request, "encyclopedia/search_entries.html", {
            "title": title,
            "results" : results
            })
    else:
        
        print("we got there!!!!")
        return render(request, "encyclopedia/search_entries.html", {
            
            
            })
        

        
def edit_page(request,title):

    
    print("View function is running!")  # Debugging: Confirm the view is being called
    entry = util.get_entry(title)
    

    # Form Function Begins
    class NewTaskFormEdit(forms.Form):
        content_text_area = forms.CharField(
            label="Content", 
            widget=forms.Textarea(attrs={'rows': 10, 'cols': 10
            ,'class': 'my-textarea' }),initial=(entry))
    # Form Function Ends

    if request.method == "POST":
        form = NewTaskFormEdit(request.POST)

        print("Test to see if we get here")
        if form.is_valid():
            print("form is valid")
            task_content = form.cleaned_data["content_text_area"]
            print("Content is " + task_content )
            if task_content is None:
                print("Value is null")
            else:
                util.save_entry(title, task_content)
                entry = util.get_entry(title)
                return render(request, "encyclopedia/entry_page.html",{
                    "entry": markdown2.markdown(entry),
                    "title": title
            })



    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "entry": entry,
        "form": NewTaskFormEdit(),
    })
    
    
def random_page(request):
    #A test, please delete when done.
    print("List below: ")
    print(util.list_entries())
    lengthofList = len(util.list_entries())
    lengthofList = lengthofList - 1
    randomNumber = random.randint(0, lengthofList)
    print(randomNumber)
    fullList = util.list_entries()
    fullListRandomEntry = fullList[randomNumber]
    print(fullListRandomEntry)
    randomEntry = util.get_entry(fullList[randomNumber])
    print(randomEntry)

    entry = randomEntry
    title = fullListRandomEntry
    #End of test

    return render(request, "encyclopedia/entry_page.html",{
                    "entry": markdown2.markdown(entry),
                    "title": title
            })



def error(request, title):
    return render(request, "encyclopedia/error.html", {
        "title": title,
        
        
    })
    