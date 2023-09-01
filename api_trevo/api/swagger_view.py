from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Api Trevo",
        default_version='v1',
        description="API que Cadastra clientes que compram rifas, além de criar pagamentos ver os números comprados e "
                    "e numeros pendentes",
        terms_of_service='https://www.apache.org/licenses/LICENSE-2.0',
        contact=openapi.Contact(url='https://github.com/samuelfilho-dev'),
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[],
)
