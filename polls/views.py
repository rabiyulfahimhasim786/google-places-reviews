from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth import User
# from .serializers import UserSerializers
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Reviews
from .serializers import ReveiwSerializers
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                       IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
import requests
import datetime as dt
#
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
# datetime.date.today()  # Returns 2018-01-15

# datetime.datetime.now() # Returns 2018-01-15 09:00
google_api_key ='yourapikey'
# Create your views here.
def index(request):
    return HttpResponse('Hello world')
def get_place_details(place_id):
    # Set up the Google Places API request
    api_url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={google_api_key}'

    # Make a request to the Google Places API
    response = requests.get(api_url)
    if response.status_code == 200:
        place_details = response.json().get('result')
        # print(place_details)
        # Extract reviews from the place details
        reviews = [
            {
                'author_name': review['author_name'] or None,
                'rating': review['rating'] or None,
                'relative_time_description': review['relative_time_description'] or None,
                'text': review['text'] or None,
            }
            for review in place_details.get('reviews', [])
        ]

        # Send the formatted reviews as JSON
        return ({'reviews': reviews})
    else:
        # Handle errors
        return ({'error': 'Failed to fetch place details'})

class ReviewListCreateView(ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReveiwSerializers
    permission_classes = [IsAuthenticated, IsOwner]
    # permission_classes = (IsAdminUserOrReadOnly,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('keyword',)

    # def getdata(self):
    def get(self, request, *args, **kwargs):
        try:
            # input_url = request.data.get('xmls')
            place_id = self.request.query_params.get('web')
            print(place_id)
            # if not place_id:
            if place_id:
                if not place_id:
                    place_id = self.request.query_params.get('web')
                print(place_id)
                # Access the review data from the request
                # review_data = {
                #     'author_name': request.GET.get('author_name', None),
                #     'rating': request.GET.get('rating', None),
                #     'relative_time_description': request.GET.get('relative_time_description', None),
                #     'text': request.GET.get('text', None),
                # }
                # Set up the Google Places API request
                # place_id ='ChIJO-2Z8A5kUjoRgXokgqGaBEs' # desss
                # # place_id =  'ChIJN1t_tDeuEmsRUsoyG83frY4'
                api_url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={google_api_key}'

                # Make a request to the Google Places API
                response = requests.get(api_url)
                todaysdates = dt.datetime.now().strftime ("%Y-%m-%d")
                if response.status_code == 200:
                    place_details = response.json().get('result')
                    # print(place_details)
                    # Extract reviews from the place details
                    reviews = [
                        {
                            'authorname': review['author_name'] or None,
                            'rating': review['rating'] or None,
                            'relativetimedescription': review['relative_time_description'] or None,
                            'text': review['text'] or None,
                            'date': todaysdates or None,
                        }
                        # for review in place_details.get('reviews', [])
                        for review in place_details.get('reviews', {})
                    ]
                    # print(reviews)
                    # print(type(reviews))
                    # Send the formatted reviews as JSON
                    # return ({'reviews': reviews})
                # else:
                    # Handle errors
                    # return ({'error': 'Failed to fetch place details'})

                # Create a new Reviews instance using the serializer
                    for review_data in reviews:
                        # Check if a similar review already exists in the database
                        if Reviews.objects.filter(authorname=review_data['authorname'], text=review_data['text']).exists():
                            continue  # Skip saving this review as it already exists
                        serializer = self.get_serializer(data=review_data)
                        serializer.is_valid(raise_exception=True)
                        self.perform_create(serializer)

                    # Return a custom response if needed
                    return Response({'message': 'Review created successfully'})
                    # serializer = ReveiwSerializers()
                    # return Response(serializer.data)
            else:
                # Handle errors
                # return ({'error': 'Failed to fetch place details'})
                # serializer = ReveiwSerializers()
                # return Response(serializer.data)
                # queryset = self.get_queryset()
                # serializer = ReveiwSerializers(queryset, many=True)
                # return Response(serializer.data)
                # if place_id or not place_id:
                #     queryset = self.get_queryset()
                #     serializer = ReveiwSerializers(queryset)
                #     return Response(serializer.data)

                queryset = self.get_queryset()
                serializer = ReveiwSerializers(queryset, many=True)
                return Response(serializer.data)
            
                
        except requests.exceptions.HTTPError as http_err:
            # Return an error response with the URL and error message
            error_msg = f"HTTP error occurred: {http_err}"
            error_data = {'url': place_id, 'error': error_msg}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            # Return an error response with the URL and error message
            error_msg = f"An error occurred: {err}"
            error_data = {'url': place_id, 'error': error_msg}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # Override the list method if you want to customize the list behavior
        # For example, you might want to return a custom response after creating a review
        response = super().list(request, *args, **kwargs)
        # Additional custom logic if needed
        return response


class ReviewsRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReveiwSerializers
    permission_classes = [IsAuthenticated, IsOwner]
    # permission_classes = (IsAdminUserOrReadOnly,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('keyword', )