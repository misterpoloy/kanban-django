import asyncio
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Card, Column, Board

# Define GraphQL types
class CardType(DjangoObjectType):
    class Meta:
        model = Card

class ColumnType(DjangoObjectType):
    class Meta:
        model = Column

class BoardType(DjangoObjectType):
    class Meta:
        model = Board

# Helper function for authentication
def authenticate_user(info):
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

    return user

# Mutation: Create Column
class CreateColumnMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    column = graphene.Field(ColumnType)

    def mutate(self, info, title):
        user = authenticate_user(info)  # Ensure the user is authenticated
        column = Column.objects.create(title=title)  # Create the column
        return CreateColumnMutation(column=column)

class DeleteColumnMutation(graphene.Mutation):
    class Arguments:
        column_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, column_id):
        user = authenticate_user(info)  # Ensure the user is authenticated

        try:
            # Get the column by ID
            column = Column.objects.get(id=column_id)
            print(f"Deleting column: {column.title}")

            # Delete all associated cards (if desired)
            column.cards.all().delete()
            print(f"Deleted all cards from column {column.title}")

            # Delete the column itself
            column.delete()

            return DeleteColumnMutation(success=True)

        except Column.DoesNotExist:
            raise Exception(f"Column with ID {column_id} does not exist")
        except Exception as e:
            print(f"Error deleting column: {e}")
            raise Exception("Failed to delete column")


# Mutation: Create Card
class CreateCardMutation(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        column_id = graphene.ID(required=True)

    card = graphene.Field(CardType)

    def mutate(self, info, content, column_id):
        print(f"Creating card with content: '{content}' in column: {column_id}")

        # Authenticate the user
        user = authenticate_user(info)

        # Ensure the column exists
        try:
            column = Column.objects.get(id=column_id)
            print(f"Found column: {column.title}")
        except Column.DoesNotExist:
            raise Exception(f"Column with id {column_id} does not exist")

        # Create the new card
        try:
            card = Card.objects.create(content=content)
            print(f"Card created with ID: {card.id}")
        except Exception as e:
            print(f"Error creating card: {e}")
            raise Exception("Failed to create card")

        # Add the card to the column's many-to-many field
        try:
            column.cards.add(card)
            column.save()
            print(f"Card '{card.content}' added to column '{column.title}'")
        except Exception as e:
            print(f"Error adding card to column: {e}")
            raise Exception("Failed to add card to column")

        # Return the created card
        return CreateCardMutation(card=card)


# Mutation: Update Card
class UpdateCardMutation(graphene.Mutation):
    class Arguments:
        card_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    card = graphene.Field(CardType)

    def mutate(self, info, card_id, content):
        user = authenticate_user(info)
        card = Card.objects.get(id=card_id)
        card.content = content
        card.save()
        return UpdateCardMutation(card=card)

# Mutation: Delete Card
class DeleteCardMutation(graphene.Mutation):
    class Arguments:
        card_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, card_id):
        user = authenticate_user(info)
        card = Card.objects.get(id=card_id)
        card.delete()
        return DeleteCardMutation(success=True)

# Define Query and Mutation classes
class Query(graphene.ObjectType):
    boards = graphene.List(BoardType)

    def resolve_boards(self, info):
        # Ensure an event loop is available in the current thread
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        user = authenticate_user(info)
        return Board.objects.filter(user=user)

class Mutation(graphene.ObjectType):
    create_card = CreateCardMutation.Field()
    update_card = UpdateCardMutation.Field()
    delete_card = DeleteCardMutation.Field()
    create_column = CreateColumnMutation.Field()
    delete_column = DeleteColumnMutation.Field()

# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
