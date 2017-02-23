#!/usr/bin/env python3
import sys, yaml, ast

def get_plugins_settings(argv):
    '''
    Returns comma seperated string of items that needs to be
    added to settings.INSTALLED_APP and urlpatterns to root urls.py for
    the list of plugins in 'argv[2]'.
    
    @params: argv[2] = List of included plugins.
    @params: argv[3] = settings need to read. (installed_app OR url_patterns)
    '''
    plugins_list = ast.literal_eval(argv[2]) #converts string to correponding python literal.
    
    with open('/home/vagrant/setup/configs/plugins/vars.yml', 'r') as f:
        doc = yaml.load(f)
        all_plugins_settings_list = []
        plugin_settings = ''
        
        #make a list with all plugin's settigs 
        for each_plugin in plugins_list:
            try:
                all_plugins_settings_list.extend(list(set(doc[each_plugin][str(argv[3])])))
            except KeyError:
                pass
        #Iterate over unique list and form a comma seperated string.    
        for each in list(set(all_plugins_settings_list)):
            if argv[3] == 'URL_PATTERNS':
                plugin_settings = plugin_settings+("%s,\n    " %each) #without quotes
            else:    
                plugin_settings = plugin_settings+("'%s',\n    " %each) #with quotes    
            
        print(plugin_settings)
        
        
class extra_settings_vars:
    def __init__ (self,settings_var_name,settings_var_value,settings_var_type):
        self.var_name = settings_var_name
        self.var_value = settings_var_value
        self.var_type = settings_var_type
    
    
def get_plugins_extra_settings(argv):
    '''
    Returns a string in the form of {settings variable = value} items that needs to be added
    to settings.py as extra settings for the list of plugins in 'argv[2]'.
    
    @params: argv[2] = List of included plugins.
    '''
    plugins_list = ast.literal_eval(argv[2]) #converts string to correponding python literal.      
    with open('/home/vagrant/setup/configs/plugins/vars.yml', 'r') as f:
        doc = yaml.load(f)
        plugin_extra_settings = ''       # final string to replace the placeholder in settings file
        extra_settings_dict ={}
        try:
            for each_plugin in plugins_list:
                    extra_settings = doc[each_plugin]['EXTRA_SETTINGS']                
                    for key, value in extra_settings.items():
                        try:
                            value = ast.literal_eval(str(value))
                            var_type = type(value)
                        except (SyntaxError, ValueError): #To handle string values in var.yml
                            var_type = type('string')
                        if key in extra_settings_dict:
                            # if the setting var is already present, append to it
                            extra_settings_dict[key].var_value += value
                            extra_settings_dict[key].var_value = var_type(set(extra_settings_dict[key].var_value))
                        else:
                            settings_obj = extra_settings_vars(key,value,var_type)   
                            extra_settings_dict[key] = settings_obj
            
            for key, settings_obj in extra_settings_dict.items():            
                if settings_obj.var_type == int:
                    settings_obj.var_value = str(settings_obj.var_value)
                    plugin_extra_settings += key +' = '+ settings_obj.var_value +' \n\n'
                elif settings_obj.var_type == str:
                    settings_obj.var_value = str(settings_obj.var_value)
                    plugin_extra_settings += key +' = '+ "'"+settings_obj.var_value +"'"+' \n\n'    
                else:
                    settings_obj.var_value = str(settings_obj.var_type(settings_obj.var_value)) 
                    plugin_extra_settings += key +' = '+ settings_obj.var_value +' \n\n'
        except Exception as e:
            pass
        
        print(plugin_extra_settings)
        
def get_user_defined_apps(argv):
    '''
    Returns comma seperated string of items that needs to be
    added to settings.py {own_app} placeholder for the list
    of user defined apps in 'argv[2]'.
    '''
    all_apps = ''
    try:
        user_apps = ast.literal_eval(argv[2]) #converts string to correponding python literal.
        user_apps.append('system') #default app for custom management commands.
        for app in user_apps:
            all_apps += ("'%s', \n    " %app)
    except:
        all_apps = "'system', \n" #default app for custom management commands.
        
    print(all_apps)    
        
    
                  
if __name__ == '__main__':
    '''
    Method name will be passed from the calling function.
    args = (filename, method name, plugins, required settings_name)
    '''
    eval(sys.argv[1])(sys.argv)
