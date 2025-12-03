
from jjsystem.common.subsystem import router


class Router(router.Router):

    def init(self, routes=[]):
        super().init('integracao', routes)

    @property
    def routes(self):
        return [
            {
                'action': 'Inicia uma sub-rotina para as integrações',
                'method': 'POST',
                'url': '/integracoes/inicia_subrotina',
                'callback': 'queue_subroutine'
            }
        ]
