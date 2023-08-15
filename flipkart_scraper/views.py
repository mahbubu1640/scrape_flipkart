from django.shortcuts import render

# flipkart_scraper/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

class ScrapeAndSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        flipkart_url = request.data.get('flipkart_url')
        if not flipkart_url:
            return Response({"message": "Flipkart URL missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(flipkart_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('span', class_='B_NuCI').get_text()
            price = float(soup.find('div', class_='_30jeq3 _16Jk6d').get_text().replace('₹', '').replace(',', ''))
            description = soup.find('div', class_='_3cpW1u').get_text()
            reviews = int(soup.find('span', class_='_2_R_DZ').get_text().split()[0])
            ratings = float(soup.find('div', class_='hGSR34').get_text())
            media_count = len(soup.find_all('img', class_='_396cs4 _3exPp9'))

            product = Product.objects.create(
                user=request.user,
                title=request.title,
                price=request.price,
                description=request.description,
                reviews=request.reviews,
                ratings=request.ratings,
                media_count=request.media_count
            )

            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": "Error scraping data or saving to database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetrieveProductView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            if product.user != request.user:
                return Response({"message": "Product does not belong to the logged-in user"}, status=status.HTTP_403_FORBIDDEN)

            # Return product data
            data = {
                "title": product.title,
                "price": product.price,
                "description": product.description,
                "reviews": product.reviews,
                "ratings": product.ratings,
                "media_count": product.media_count
            }
            return Response(data, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
