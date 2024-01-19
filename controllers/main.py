import odoo
from odoo.addons.web.controllers import main
from odoo.exceptions import Warning
import odoo.modules.registry
from odoo.tools.translate import _
from odoo import http
from odoo.http import request
import socket
import logging


# _logger = logging.getLogger(__name__)

class UserStatusLongpolling(http.Controller):
    @http.route('/web/user_status', type='json', auth='user')
    def update_status(self, message=None, db=None):
        user_id = request.env['res.users'].sudo().browse(request.env.user.id)
        if not user_id:
            return {'message': 'Please login', 'user_id': False}
        else:
            user_ip = request.httprequest.environ['HTTP_X_REAL_IP']
            ip_list = []
            if user_id.allowed_ips:    
                for rec in user_id.allowed_ips:
                    domain_ip = socket.gethostbyname(rec.ip_address)
                    ip_list.append(domain_ip)  
                if user_ip not in ip_list:
                    request.session.logout(keep_db=True)
                    logging.info("User IP changed. User %r - Session Terminated", user_id.name)
                    return {'status': 'session_closed', 'user_ids': user_id.login}    
        return {'status': 'ok', 'user_id': user_id.login}

class Home(main.Home):

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        main.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            #ip_address = request.httprequest.environ['REMOTE_ADDR']
            ip_address = False
            try:
                ip_address = request.httprequest.environ['HTTP_X_REAL_IP']
            except:
                pass
            #print(ip_address)
            if request.params['login']:
                user_rec = request.env['res.users'].sudo().search(
                    [('login', '=', request.params['login'])])
                if user_rec.allowed_ips:
                    ip_list = []
                    for rec in user_rec.allowed_ips:
                        domain_ip = socket.gethostbyname(rec.ip_address)
                        ip_list.append(domain_ip)
                    if ip_address and ip_address in ip_list:
                        try:
                            uid = request.session.authenticate(
                                request.session.db,
                                request.params[
                                    'login'],
                                request.params[
                                    'password'])
                            request.params['login_success'] = True
                            return request.redirect(
                                self._login_redirect(uid, redirect=redirect))
                        except odoo.exceptions.AccessDenied as e:
                            request.uid = old_uid
                            if e.args == odoo.exceptions.AccessDenied().args:
                                values['error'] = _("Wrong login/password")
                    else:
                        request.uid = old_uid
                        values['error'] = _("Not allowed to login from this IP")
                else:
                    try:
                        uid = request.session.authenticate(request.session.db,
                                                           request.params[
                                                               'login'],
                                                           request.params[
                                                               'password'])
                        request.params['login_success'] = True
                        return request.redirect(
                            self._login_redirect(uid, redirect=redirect))
                    except odoo.exceptions.AccessDenied as e:
                        request.uid = old_uid
                        if e.args == odoo.exceptions.AccessDenied().args:
                            values['error'] = _("Wrong login/password")

        return request.render('web.login', values)
