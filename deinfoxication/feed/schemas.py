"""Application schemas."""
from flask_restless import ProcessingException
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError


class BaseSchema(Schema):
    """Base schema for all other classes."""

    id = fields.UUID()


def validation_for(model_class, schema_class: BaseSchema.__class__):
    """Prepare validation for a schema, creating a serializer and a deserializer.

    This function should be used with :meth:`create_api`.

    :param model_class: SQLAlchemy model class
    :param schema_class: Marshmallow schema class.
    :return: A dict with serializer and deserializer functions, plus validation exceptions that should be handled.
    """
    schema_instance = schema_class()

    def restless_serializer(model_instance):
        """Serialize a SQLAlchemy model instance."""
        return schema_instance.dump(model_instance).data

    def restless_deserializer(data):
        """Create a model instance from JSON data."""
        result = schema_instance.load(data)
        if not result.errors:
            # No errors, return the converted data.
            return model_class(**result.data)

        err = ValidationError(result.errors)

        # Flak-Restless expects attributes called "errors" or "message" (singular), not "messages" (plural).
        err.errors = err.messages

        raise err

    def validate_put_single(instance_id=None, data=None, **kw):
        """Validate data on a PUT request of a single object.

        The current stable version of Flask-Restless (0.17.0) does not deal with this situation.
        All posted data is not validated at all.

        The current dev version (1.0.0b2) is still in beta.
        """
        model_instance = model_class.query.get(instance_id)
        schema_instance.dump(model_instance)
        result = schema_instance.load(data)
        if result.errors:
            raise ProcessingException(result.errors)

    return dict(serializer=restless_serializer,
                deserializer=restless_deserializer,
                validation_exceptions=[ValidationError],
                preprocessors={'PUT_SINGLE': [validate_put_single]})


class FeedSchema(BaseSchema):
    """Feed serialisation schema."""

    name = fields.String()
    url = fields.Url(required=True)
