import django
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string
import io
import os
from rich import print
from rich.console import Console
console = Console()
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
    }
]
#Set django template backend
settings.configure(TEMPLATES=TEMPLATES)
django.setup()


def render(context,dir,output):
    """Render template with given values"""
    console.rule(f"[bold cyan]Rendering html[/bold cyan]",style="cyan")
    if context == {}:
        print("Rendering html | [bold red]KO, There is nothing inside the database")
    else:
        try:
            content = render_to_string('template.html', context) 
            if not os.path.exists(dir):
                os.makedirs(dir)  
            with io.open(dir+output, 'w', encoding="utf-8") as f:
                f.write(content)   
            print("Rendering html | [bold green]OK")
            print(f"Saved in [bold cyan]{dir}{output}")
        except Exception as e:   
            print("Rendering html | [bold red]KO")
            print(e)
