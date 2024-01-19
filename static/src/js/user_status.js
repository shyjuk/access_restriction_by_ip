/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import rpc from 'web.rpc';

const { onMounted } = owl.hooks;

patch(WebClient.prototype,'access_restriction_by_ip', {
  setup() {
    this._super.apply(this, arguments);

    onMounted(() => {
      this.loopCheck();
    });
  },

  //Check the user status every 5 minutes
  loopCheck(){
    var self = this;
    setInterval(function() { 
      self.UserStatusCheck();
    }, 300000);
  },

  async UserStatusCheck(){
    var self = this;
    await rpc.query({
      route: "/web/user_status",
    }).then(function (result) {
      console.log("User Status: ", result.status);
        if (result.status == 'session_closed')
        {
          window.location.replace('/web/session/logout?redirect=/web');
        }
      
    });
  }

});
