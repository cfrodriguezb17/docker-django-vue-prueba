from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, ProfileSerializer, RedeemPointsSerializer, GrantPointsSerializer, TransactionSerializer
from .models import User, Transaction
from .permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class ReedemPointsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RedeemPointsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        description = serializer.validated_data.get('description', 'Canje de puntos')
        user = request.user

        if user.points < amount:
            return Response(
                {"error": "No tienes suficientes puntos para realizar este canje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user.points -= amount
                user.save(update_fields=['points'])

                Transaction.objects.create(
                    user=user,
                    amount=amount,
                    transaction_type='redeem',
                    description=description
                )
        except Exception as e:
            return Response({"error": f"Ocurrió un error en la transacción: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"message": "Puntos canjeados exitosamente.", "new_balance": user.points},
            status=status.HTTP_200_OK
        )
    
class GrantPointsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GrantPointsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        amount = serializer.validated_data['amount']
        description = serializer.validated_data.get('description', 'Puntos otorgados por administrador')
        
        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                target_user.points += amount
                target_user.save(update_fields=['points'])

                Transaction.objects.create(
                    user=target_user,
                    amount=amount,
                    transaction_type='grant',
                    description=description
                )
        except Exception as e:
            return Response({"error": f"Ocurrió un error en la transacción: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(
            {"message": f"Se han otorgado {amount} puntos a {target_user.first_name}.", "new_balance": target_user.points},
            status=status.HTTP_200_OK
        )

class TransactionsHistoryAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by('-created_at')