"""Custom module for django tests"""
import re
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View


def home(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page with a greeting, mission statement, and list of services.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered home page with context data.
    """
    if request.method == "GET":
        greeting = "Welcome to Our Web Development Hub!"
        mission = """We specialize in creating high-performance web applications and intelligent automation solutions. 
        Whether you need a full-cycle web application or a powerful Telegram bot, we’ve got you covered."""
        services = ["Django, FastAPI, and Flask-based web application development",
                    "Scalable and efficient backend solutions",
                    "Custom Telegram bot development for automation and engagement"]
        return render(request, "main/home.html", {"greeting": greeting, "mission": mission, "services": services})


def about(request: HttpRequest) -> HttpResponse:
    """
    Renders the about page with information about the company, its mission, and history.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered about page with context data.
    """
    if request.method == "GET":
        about_us = """Welcome to our platform, where we specialize in building powerful and efficient web solutions. 
        Our expertise spans across multiple modern frameworks, ensuring high-performance applications tailored to your needs."""
        mission = """Our mission is to empower businesses with cutting-edge web technologies that streamline operations, 
        enhance user experiences, and drive growth. We believe in building efficient, scalable, and secure applications that stand the test of time."""
        history = """Founded by passionate developers, our journey began with a simple goal—to create powerful and 
        reliable digital solutions using the best web technologies available. Over the years,we have successfully delivered 
        projects across various industries, gaining expertise in full-cycle web development and automation. 
        Today, we continue to innovate, helping businesses and individuals bring their ideas to life with tailored digital solutions."""
        return render(request, 'main/about.html', {"about_us": about_us, "mission": mission,
                                                   "history": history, "about_date": datetime.utcnow()})


class ContactView(View):
    """
    A view class to handle the contact page. Displays contact information such as phone numbers, address, and email.

    Methods:
        get: Handles GET requests and renders the contact page.
    """

    def get(self, request):
        """
        Renders the contact page with contact information.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Rendered contact page with context data.
        """
        phone_list = [380111111111, 380222222222, 380333333333]
        address = "Dreamshire, Web str, apt 404."
        email = ""
        return render(request, 'main/contacts.html', {"phone_list": phone_list, "address": address,
                                                      "email": email})


class ServiceView(View):
    """
    A view class to handle the services page. Displays a list of services offered by the company.

    Methods:
        get: Handles GET requests and renders the services page.
    """

    def get(self, request):
        """
        Renders the services page with a list of services.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Rendered services page with context data.
        """
        return render(request, 'main/services.html', {"service_list": service_list})


def search(request: HttpRequest) -> HttpResponse:
    """
    Renders the page with search results.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered home page with context data.
    """
    if request.method == "GET":
        query = request.GET.get("query")
        search_res = [service for service in service_list if str(query).lower() in service[0].lower()]
        return render(request, "main/search.html", {"search_res": search_res})


service_list = [
    ("Full-cycle Django-based web-application development",
     "We build secure, scalable, and feature-rich web applications using Django, ensuring a robust backend and smooth user experience."),
    ("Full-cycle FastAPI-based web-application development",
     "Leverage the power of FastAPI for high-performance, async-driven web applications with fast response times and modern API standards."),
    ("Full-cycle Flask-based web-application development",
     "Develop lightweight, flexible, and efficient web applications with Flask, perfect for projects that need customization and simplicity."),
    ("Telegram bot development",
     "Automate workflows, engage users, and enhance communication with custom Telegram bots tailored to your business needs")
]
