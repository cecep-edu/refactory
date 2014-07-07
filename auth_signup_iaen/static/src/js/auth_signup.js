openerp.auth_signup_iaen = function(instance) {
    instance.auth_signup_iaen = instance.auth_signup_iaen || {};
    var _t = instance.web._t;
    
    instance.web.Login.include({
        
        on_token_loaded: function(result) {
            // select the right the database
            this.selected_db = result.db;
            this.on_db_loaded([result.db]);
            
            if (result.token) {
                // switch to signup mode, set user name and login
                if (this.params.type === 'signup'){
                    var params = {
                        dbname : result.db,
                        token: result.token,
                    }
                    this.rpc('/auth_iaen/active_user',params)
                        .done(function(result) {
                            if (result.error) {
                                self.show_error(result.error);
                            }
                        });
                    this.show_error(_t("Se ha activado su cuenta, ahora puede logearse"));
                    this.set('login_mode', 'default');
                }
                if (this.params.type === 'reset'){
                    this.set('login_mode', (this.params.type === 'reset' ? 'reset' : 'signup'));
                    this.$("form input[name=name]").val(result.name).attr("readonly", "readonly");
                    if (result.login) {
                        this.$("form input[name=login]").val(result.login).attr("readonly", "readonly");
                    } else {
                        this.$("form input[name=login]").val(result.email);
                    }
                }
            } else {
                // remain in login mode, set login if present
                delete this.params.token;
                this.set('login_mode', 'default');
                this.$("form input[name=login]").val(result.login || "");
            }
        },



        get_params: function(){
            // signup user (or reset password)
            var db = this.$("form [name=db]").val();
            var name = this.$("form input[name=name]").val();
            var login = this.$("form input[name=login]").val();
            var password = this.$("form input[name=password]").val();
            var confirm_password = this.$("form input[name=confirm_password]").val();
            var email = this.$("form [name=email]").val();
            if (!db) {
                this.do_warn(_t("Login"), _t("No database selected !"));
                return false;
            } else if (!name) {
                this.do_warn(_t("Login"), _t("Please enter a name."));
                return false;
            } else if (!login) {
                this.do_warn(_t("Login"), _t("Please enter a username."));
                return false;
            } else if (!password || !confirm_password) {
                this.do_warn(_t("Login"), _t("Please enter a password and confirm it."));
                return false;
            } else if (password !== confirm_password) {
                this.do_warn(_t("Login"), _t("Passwords do not match; please retype them."));
                return false;
            }
            if (!email) {
                this.do_warn(_t("Login"), _t("No email ingresado !"));
                return false;
            }
            var params = {
                dbname : db,
                token: this.params.token || "",
                name: name,
                login: login,
                password: password,
                email: email,
                active: 'False',
            };
            return params;


        },

        on_submit: function(ev) {
            if (ev) {
                ev.preventDefault();
            }
            var login_mode = this.get('login_mode');
            if (login_mode === 'signup' || login_mode === 'reset') {
                var params = this.get_params();
                if (_.isEmpty(params)){
                    return false;
                }
                //var self = this,
                 //   super_ = this._super;
                this.rpc('/auth_iaen/signup', params)
                    .done(function(result) {
                        if (result.error) {
                            self.show_error(result.error);
                        }
                    });
            } else {
                // regular login
                this._super(ev);
                //return false
            }
            this.set('login_mode', 'default');
        },
    });
};
