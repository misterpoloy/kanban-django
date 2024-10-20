import asyncio
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Card, Column, Board

class CardType(DjangoObjectType):
    class Meta:
        model = Card

class ColumnType(DjangoObjectType):
    class Meta:
        model = Column

class BoardType(DjangoObjectType):
    class Meta:
        model = Board

class Query(graphene.ObjectType):
    boards = graphene.List(BoardType)

    def resolve_boards(self, info):
        # Ensure an event loop is available in the current thread
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Access the request object directly from `info.context`
        request = info.context
        user = AnonymousUser()  # Default to AnonymousUser
        auth = JWTAuthentication()

        try:
            # Extract and validate the JWT token from the Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise Exception("No Authorization header provided")

            # Split 'Bearer <token>' and get the token part
            token = auth_header.split(' ')[1]
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)

        except Exception as e:
            print(f"Authentication error: {e}")
            raise Exception("Authentication required")

        # Ensure the user is authenticated
        if user.is_anonymous:
            raise Exception("Authentication required")

        # Query the boards for the authenticated user
        return Board.objects.filter(user=user)

# Define the schema
schema = graphene.Schema(query=Query)
