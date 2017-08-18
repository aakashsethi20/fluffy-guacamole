from conduit.apps.core.renderers import ConduitJSONRenderer

class UserJSONRenderer(ConduitJSONRenderer):
    object_label = 'user'

    def render(self, data, media_type=None, renderer_context=None):
        # checking if the token is part of the response as a byte object. If yes, decoding it into utf-8
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode(charset)

        return super(UserJSONRenderer, self).render(data)