from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData
from .serializers import SensorDataSerializer, UserSerializer
from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg
import json
from django.utils.dateparse import parse_datetime
import csv
from io import StringIO
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

class SensorDataView(APIView):
    def post(self, request):
        """
        Manipula requisições POST para criar uma nova entrada de SensorData.
        - Analisa dados JSON do corpo da requisição.
        - Transforma os dados no formato esperado.
        - Valida e salva os dados usando o SensorDataSerializer.
        - Retorna uma resposta de sucesso ou erro.
        """
        try:
            json_data = json.loads(request.body)
            
            # Transforma os dados
            transformed_data = {
                'equipment_id': json_data.get('equipmentId'),
                'timestamp': parse_datetime(json_data.get('timestamp')),
                'value': json_data.get('value')
            }
            
            serializer = SensorDataSerializer(data=transformed_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except json.JSONDecodeError:
            return Response({"error": "Dados JSON inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({"error": f"Campo obrigatório faltando: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SensorDataCSVUploadView(APIView):
    def post(self, request):
        """
        Manipula requisições POST para fazer upload de um arquivo CSV contendo SensorData.
        - Verifica se existe o arquivo CSV.
        - Lê e analisa o arquivo CSV.
        - Valida cada linha e salva os dados válidos.
        - Retorna um resumo das linhas processadas e quaisquer erros encontrados.
        """
        print(request.FILES)
        if 'file' not in request.FILES:
            return Response({"error": "Nenhum arquivo fornecido"}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "O arquivo não é um CSV"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Lê o arquivo CSV
            csv_data = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(StringIO(csv_data))

            valid_data = []
            errors = []

            for row in csv_reader:
                try:
                    transformed_data = {
                        'equipment_id': row.get('equipmentId'),
                        'timestamp': parse_datetime(row.get('timestamp')),
                        'value': float(row.get('value'))
                    }

                    serializer = SensorDataSerializer(data=transformed_data)
                    if serializer.is_valid():
                        valid_data.append(serializer.validated_data)
                    else:
                        errors.append(f"Linha {csv_reader.line_num}: {serializer.errors}")
                except Exception as e:
                    errors.append(f"Linha {csv_reader.line_num}: {str(e)}")

            print(valid_data)
            # Cria em massa os dados válidos
            with transaction.atomic():
                SensorData.objects.bulk_create([SensorData(**data) for data in valid_data])

            response_data = {
                "success": f"Processadas com sucesso {len(valid_data)} linhas",
                "errors": errors if errors else None
            }

            return Response(response_data, status=status.HTTP_201_CREATED if valid_data else status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AggregatedDataView(APIView):
    def get(self, request):
        """
        Manipula requisições GET para recuperar dados agregados de sensor.
        - Calcula os valores médios para cada ID de equipamento ao longo de um período especificado.
        - O período pode ser '24h', '48h', '1w' (1 semana) ou '1m' (1 mês).
        - Retorna os dados agregados ou um erro se o período for inválido.
        """
        period = request.query_params.get('period', '24h')
        end_date = timezone.now()

        if period == '24h':
            start_date = end_date - timedelta(hours=24)
        elif period == '48h':
            start_date = end_date - timedelta(hours=48)
        elif period == '1w':
            start_date = end_date - timedelta(weeks=1)
        elif period == '1m':
            start_date = end_date - timedelta(days=30)
        else:
            return Response({"error": "Período inválido"}, status=status.HTTP_400_BAD_REQUEST)

        data = SensorData.objects.filter(timestamp__range=(start_date, end_date)).values('equipment_id').annotate(avg_value=Avg('value'))
        return Response(data)
        
class RegisterView(APIView):
    def post(self, request):
        """
        Manipula requisições POST para registrar um novo usuário.
        - Usa o nome de usuário como endereço de e-mail do usuário.
        - Serializa e salva os dados do usuário.
        - Retorna tokens JWT para autenticação após o registro bem-sucedido.
        """
        # Cria uma cópia mutável dos dados da requisição
        mutable_data = request.data.copy()
        
        # Usa o username como e-mail
        username = mutable_data.get('username')
        mutable_data['email'] = username

        serializer = UserSerializer(data=mutable_data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
