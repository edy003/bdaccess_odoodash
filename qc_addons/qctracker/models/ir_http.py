from werkzeug.exceptions import BadRequest
from odoo import models
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class IrHttp(models.AbstractModel):
    _inherit = "ir.http"
    
    @classmethod
    def _auth_method_custom_auth(cls):
        _logger.info("Custom Auth method called")

        # Récupération du header Authorization
        acces_token = request.httprequest.headers.get('Authorization')
        if not acces_token:
            _logger.warning("Aucun token fourni dans le header Authorization")
            raise BadRequest('pas de token')
        
        if acces_token.startswith('Bearer '):
            acces_token = acces_token[7:]

        # Vérification du token avec le scope
        user_id = request.env['res.users.apikeys']._check_credentials(
            scope='odoo.restapi',
            key=acces_token
        )

        if not user_id:
            _logger.warning("Token invalide ou non autorisé pour le scope odoo.restapi")
            raise BadRequest('token invalide')

        # Réaffectation de l'environnement avec l'utilisateur authentifié
        request._env = request.env(user=user_id)

        _logger.info(f"Authentifié avec succès : user_id={user_id}")
