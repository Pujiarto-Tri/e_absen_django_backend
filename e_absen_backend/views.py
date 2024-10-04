from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime

#Rest Framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.views import APIView

#Local
from .serializers import EmployeeSerializer, AttendanceSerializer
from .models.Employee import Employee
from .models.Shift import Shift
from .models.Attendance import Attendance

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return JsonResponse({
                'user': {
                    'email': employee.user_id.email,
                },
                'message': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'email': user.email,
                'name': user.user_id.name if hasattr(user, 'user_id') else None,
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

class EmployeeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employee = Employee.objects.get(user_id=request.user)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            employee = Employee.objects.get(user_id=request.user)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee = Employee.objects.get(user_id=request.user)
        shift_id = request.data.get('shift_id')

        try:
            shift = Shift.objects.get(pk=shift_id)
        except Shift.DoesNotExist:
            return Response({"error": "Shift not found"}, status=status.HTTP_404_NOT_FOUND)
        
        attendance, created = Attendance.objects.get_or_create(
            user=employee,
            attendance_date=datetime.today().date(),
            defaults={'shift': shift, 'check_in_time': datetime.now().time()}
        )

        if not created:
            return Response({"error": "Already check in today"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee = Employee.objects.get(user_id=request.user)

        try:
            attendance = Attendance.objects.get(
                user=employee,
                attendance_date=datetime.today().date()
            )
        except Attendance.DoesNotExist:
            return Response({"error": "Check-in not found for today"}, status=status.HTTP_404_NOT_FOUND)
        
        if attendance.check_out_time:
            return Response({"error" : "Already checked out today"}, status=status.HTTP_400_BAD_REQUEST)

        attendance.check_out_time = datetime.now().time()
        attendance.save()

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_200_OK)
