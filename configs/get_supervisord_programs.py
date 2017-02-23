#!/usr/bin/env python3
import sys, ast, yaml

def get_plugins_supervisord(plugins):
    plugins = ast.literal_eval(plugins) #converts string to correponding python literal.
    all_settings = ''
    with open('/home/vagrant/setup/configs/project_settings.yml', 'r') as f:
        project_settings = yaml.load(f)
        supervisord_content = {"django-celery":
            "[program:"+project_settings['MYSITE_NAME']+"-celery]\n"+
            "command=/usr/local/bin/celery -A "+project_settings['DJANGO_PROJECT']['guest']['name']+" worker -l info\n"+
            "directory="+project_settings['DJANGO_PROJECT']['guest']['root']+"/"+project_settings['DJANGO_PROJECT']['guest']['name']+"\n"+
            "user=vagrant\n"+
            "numprocs=1\n"+
            "autostart=true\n"+
            "autorestart=true\n"+
            "stdout_logfile=/tmp/celeryd.log\n"
            "redirect_stderr=true\n"+
            "killasgroup=true\n"+
            "stopasgroup=true\n"+
            "environment=deploymenthost='%s'" %(project_settings['DEPLOYMENT_HOST'])
            }
    
        for each in plugins:
            if supervisord_content.get(each):
                all_settings += supervisord_content.get(each) + "\n"
        print(all_settings)
    

if __name__ == '__main__':
    get_plugins_supervisord(sys.argv[1])