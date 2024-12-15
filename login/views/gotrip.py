from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from login.models import Trip
from login.serializers import TripSerializer


class TripAPI(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        trips = Trip.objects.filter(created_by=request.user)  # 사용자별 Trip 데이터
        page = request.GET.get('page', 1)  # 요청에서 'page' 값 가져오기
        per_page = 10  # 페이지당 항목 수

        # Paginator로 페이지네이션 처리
        paginator = Paginator(trips, per_page)
        try:
            paginated_trips = paginator.page(page)
        except PageNotAnInteger:
            paginated_trips = paginator.page(1)  # 'page' 값이 유효하지 않으면 첫 번째 페이지
        except EmptyPage:
            paginated_trips = []  # 'page' 값이 범위를 벗어나면 빈 결과 반환

        # 직렬화
        serializer = TripSerializer(paginated_trips, many=True)

        # 응답 데이터 구성
        response_data = {
            "total_count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": paginated_trips.number if paginated_trips else 1,
            "is_next": paginated_trips.has_next() if paginated_trips else False,
            "is_previous": paginated_trips.has_previous() if paginated_trips else False,
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        # 인증된 사용자만 접근 가능
        serializer = TripSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
