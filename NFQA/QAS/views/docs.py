import coreapi
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class SwaggerSchemaView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    renderer_classes = [renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer]

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        """
        Retrieve the API documents.
        """
        description = 'Infoweaver Application Program Interface Documents'
        generator = SchemaGenerator(title='Infoweaver API', description=description)
        schema = generator.get_schema(request=request)
        keys = schema.data.get('api').data.keys()
        values = schema.data.get('api')
        schema = coreapi.Document(
            url=schema.url,
            title=schema.title,
            description=schema.description,
            content={key: values.get(key) for key in keys}
        )
        return Response(schema)
