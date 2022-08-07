from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator


class SwaggerSchemaView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        """
        Retrieve the API documents.
        """
        generator = SchemaGenerator(title='Infoweaver API')
        schema = generator.get_schema(request=request)
        return Response(schema)
