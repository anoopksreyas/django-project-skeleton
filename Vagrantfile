# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'yaml'
require 'readline'

def input(prompt="", newline=false)
  prompt += "\n" if newline
  Readline.readline(prompt, true).squeeze(" ").strip
end

#Interactive script: START
=begin 
Below script is for getting host dir path, project name etc from user.
Default: Parent directory of setup/ folder.
=end
if ARGV[0] == 'up' #Run script only on 'vagrant up'
    $DEFAULT_PROJECT_DIR = File.expand_path(File.dirname(File.dirname(__FILE__))) #parent dir of setup folder.
    dir_path_exists = false
    prompt_text = "\n"+'     '*10+'*'*8+"Django BaseBox setup"+'*'*8+"\n\nWhere you want to create your "+
                  "project?(Full directory path)\n"+' '*2+"Press ENTER if path is '"+$DEFAULT_PROJECT_DIR+"': "
    while dir_path_exists == false do
        $PROJECT_DIR = input(prompt=prompt_text)
        if $PROJECT_DIR == ''
            $PROJECT_DIR = $DEFAULT_PROJECT_DIR
            break
        end
        if File.directory?($PROJECT_DIR) #Check if its a valid directory
            dir_path_exists = true
        end
        prompt_text = "Please give a valid directory path: "
    end
    $PROJECT_DIR = $PROJECT_DIR.sub(/(\/)+$/, '') #Replace trailing backslashes if any with empty string from the dir path.
    
    prompt_text = "\nPlease provide your django project name: "
    $PROJECT_NAME = ''
    while $PROJECT_NAME == '' do
      $PROJECT_NAME = input(prompt=prompt_text)
      prompt_text = "Please provide a valid project name:"
    end
    
    prompt_text = "\nPlease provide site name(Eg: basebox)\n"+' '*2+"Press ENTER if you want to use project name as your site name: "
    $HOST_NAME = input(prompt=prompt_text)
    if $HOST_NAME == ''
      $HOST_NAME = $PROJECT_NAME
    end
    
    print "\nYour site name will be '\e[34m"+$HOST_NAME+"-local.com\e[0m'\n"
    
    print "\nSetup database.\n"+"-"*15
    prompt_text = "\nDatabase name: "
    $DB_NAME = input(prompt=prompt_text)
    prompt_text = "Database username: "
    $DB_USERNAME = input(prompt=prompt_text)
    prompt_text = "Database password: "
    $DB_PASSWORD = input(prompt=prompt_text)
    
    print "\nSetup admin site.\n"+"-"*17
    prompt_text = "\nSite username: "
    $ADMIN_SITE_USERNAME = input(prompt=prompt_text)
    prompt_text = "Site password: "
    $ADMIN_SITE_PASSWORD = input(prompt=prompt_text)
        
    print "\nConfiguring...\n"
    file_name = "configs/project_settings.yml"
    text = File.read(file_name)
    new_contents = text.sub(/HOST_NAME/, $HOST_NAME).sub(/HOST_ROOT/, $PROJECT_DIR).sub(/PROJECT_NAME/, $PROJECT_NAME).
                        sub(/DB_NAME/, $DB_NAME).sub(/DB_USERNAME/, $DB_USERNAME).sub(/DB_PASSWORD/, $DB_PASSWORD).
                        sub(/ADMIN_SITE_USERNAME/, $ADMIN_SITE_USERNAME).sub(/ADMIN_SITE_PASSWORD/, $ADMIN_SITE_PASSWORD)#gsub(): For global replacement.
    File.open(file_name, "w") {|file| file.puts new_contents }
end
#Interactive script: END

#custom settings: START
settings = YAML.load_file 'configs/project_settings.yml'
HOST_DJANGO_PROJECT_ROOT = settings['DJANGO_PROJECT']['host']['root']
GUEST_DJANGO_PROJECT_ROOT = settings['DJANGO_PROJECT']['guest']['root']
SITE_NAME = settings['MYSITE_NAME'] + '-'+ 'local.com'
#custom settings: END

#Script for dynamic /etc/hosts entry: START
#Add only if hostname entry not found in /etc/hosts.
if File.readlines("/etc/hosts").grep(/#{SITE_NAME}/).size == 0
  system "sudo sed -i -e '1i127.0.0.1       '"+SITE_NAME+" /etc/hosts"
end
#Script for dynamic /etc/hosts entry: END

=begin
Add host to ansible/inventory/ file dynamically based on 'development host'.
file modes: {'r':'read', 'w':'write', 'a': 'append-to-end'}
Eg:...[localhost (or) staging (or) production]
......basebox-production.com   ansible_ssh_port=2222
=end
File.open('ansible/inventory/'+settings['DEPLOYMENT_HOST'], 'w') do |f|
    f.write "#This file content is created dynamically by Vagarant file.\n"
    f.write "["+settings['DEPLOYMENT_HOST']+"]\n"
    f.write SITE_NAME + "   " + "ansible_ssh_port=2222"
end

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "amd-64"
  
  # Configure VM Ram usage
  config.vm.provider "virtualbox" do |v|
      v.name = 'Django Project Skeleton'
      v.memory = 1024 # 1024 MB= 1 GB
      #v.cpus = 2
  end

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.network :private_network, ip: "192.168.33.15"
  config.vm.network "forwarded_port", guest: 80, host: 8090
  config.vm.synced_folder ".", "/home/vagrant/setup"
  
=begin
  Below command will create specified folder in the host machine if !exists. 
  config.vm.synced_folder "dir in host machine", "corresponding link in guest machine"
=end
  config.vm.synced_folder HOST_DJANGO_PROJECT_ROOT, GUEST_DJANGO_PROJECT_ROOT, create:true

  #Provisioner: Ansible
  config.vm.provision :ansible do |ansible|
    ansible.playbook = "ansible/playbook.yml"
    ansible.inventory_path = "ansible/inventory/" + settings['DEPLOYMENT_HOST']
    ansible.host_key_checking = false
    ansible.verbose = "vv" #min-value:'v' (less details.), max-value:'vvvv' (more detials.)
    ansible.limit=SITE_NAME
  end

end
