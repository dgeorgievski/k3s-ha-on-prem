Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/bionic64"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
  end

  config.vm.synced_folder ".", "/vagrant", disabled: true
 
 
  config.vm.define "etcd1" do |etcd1|
  	etcd1.vm.hostname = "etcd1"
  	etcd1.vm.network "private_network", ip: "10.0.0.101"
        etcd1.vm.provider "virtualbox" do |vb|
		vb.name = "etcd1"
	end
  end

  config.vm.define "etcd2" do |etcd2|
  	etcd2.vm.hostname = "etcd2"
  	etcd2.vm.network "private_network", ip: "10.0.0.102"
        etcd2.vm.provider "virtualbox" do |vb|
		vb.name = "etcd2"
	end
  end

  config.vm.define "etcd3" do |etcd3|
  	etcd3.vm.hostname = "etcd3"
  	etcd3.vm.network "private_network", ip: "10.0.0.103"
        etcd3.vm.provider "virtualbox" do |vb|
		vb.name = "etcd3"
	end
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ssh.yaml"
  end

end
