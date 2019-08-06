"""Application schemas."""
from typing import Type

from flask_restless import ProcessingException, simple_serialize
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError


class BaseSchema(Schema):
    """Base schema for all other classes."""

    id = fields.UUID()


def validation_for(model_class, schema_class: Type[BaseSchema]):
    """Prepare validation for a schema, creating a serializer and a deserializer.

    This function should be used with :meth:`create_api`.

    :param model_class: SQLAlchemy model class
    :param schema_class: Marshmallow schema class.
    :return: A dict with serializer and deserializer functions, plus validation exceptions that should be handled.
    """
    schema_instance = schema_class()

    def restless_serializer(model_instance, only=None):
        """Serialize a SQLAlchemy model instance."""
        result = simple_serialize(model_instance, only=only)
        attributes = schema_instance.dump(model_instance).data
        """:type: dict"""
        attributes.pop("id")
        result["attributes"] = attributes
        return result

    def restless_deserializer(document):
        """Create a model instance from JSON data."""
        result = schema_instance.load(document)
        if not result.errors:
            # No errors, return the converted data.
            return model_class(**result.data)

        err = ValidationError(result.errors)

        # Flak-Restless expects attributes called "errors" or "message" (singular), not "messages" (plural).
        # http://flask-restless.readthedocs.io/en/1.0.0b1/customizing.html#capturing-validation-errors
        err.errors = err.messages

        raise err

    def validate_put_single(resource_id=None, data=None, **kw):
        """Validate data on a PUT request of a single object.

        The current stable version of Flask-Restless (0.17.0) does not deal with this situation.
        All posted data is not validated at all.

        The current dev version (1.0.0b2) is still in beta, and also doesn't seem to handle this.
        """
        model_instance = model_class.query.get(resource_id)
        schema_instance.dump(model_instance)
        result = schema_instance.load(data["data"]["attributes"], partial=True)
        if result.errors:
            raise ProcessingException(result.errors)

    return {
        "serializer": restless_serializer,
        "deserializer": restless_deserializer,
        "validation_exceptions": [ValidationError],
        "preprocessors": {"PATCH_RESOURCE": [validate_put_single]},
    }


class FeedSchema(BaseSchema):
    """Feed serialisation schema."""

    name = fields.String()
    url = fields.Url(required=True)
