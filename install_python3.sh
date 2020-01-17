InstallPy36() {
  # 定义python3安装目录
  install_dir=/usr/local/python36
  echo -e "${ccyan}配置 Python3.6 ${cend}"

  if [ "$(rpm -qa | grep python3-3.6)" == "" ] || [ "$(rpm -qa | grep python3-devel-3.6)" == "" ]; then
      yum -y install python36 python36-devel
  fi
  if [ ! -d "$install_dir" ]; then
      python3.6 -m venv $install_dir
  fi
  if [ ! -f "~/.pydistutils.cfg" ]; then
      echo -e "[easy_install]\nindex_url = https://mirrors.aliyun.com/pypi/simple/" > ~/.pydistutils.cfg
  fi
  if [ ! -f "~/.pip/pip.conf" ]; then
      mkdir -p ~/.pip
      echo -e "[global]\nindex-url = https://mirrors.aliyun.com/pypi/simple/\n\n[install]\ntrusted-host=mirrors.aliyun.com" > ~/.pip/pip.conf
  fi
  pip3 install python-dotenv
}
InstallPy36
