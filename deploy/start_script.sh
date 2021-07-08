#!/bin/bash
# Name    : start_script.py
# Date    : 2016.03.28
# Func    : 启动脚本
# Note    : 注意：当前路径为应用部署文件夹
# cd /usr/local/metrics-server-exporter && /usr/local/python3/python app.py
# --ca_cert=/usr/local/metrics-server-exporter/210_config/ca.crt
# --api_url="https://192.168.100.210:6443"
# --svc_token=/usr/local/metrics-server-exporter/210_config/token
#############################################################
# 初始化环境

# 用户自定义
app_folder="metrics-server-exporter"                 # 项目根目录

install_base="/data/exporter"          # 安装根目录

#############################################################
# 通用前置
# ulimit 设定
ulimit -n 100000
export LD_LIBRARY_PATH=/usr/local/easyops/ens_client/sdk:${LD_LIBRARY_PATH}

# 执行准备
install_path="${install_base}/${app_folder}/"
if [[ ! -d ${install_path} ]]; then
    echo "${install_path} is not exist"
    exit 1
fi

python3_path=${python3_path}
ca_cert=${ca_cert}
api_url=${api_url}
svc_token=${svc_token}
# 需要用户提供 python3路径 连接apiserver认证证书，apiurl以及token文件
# 启动命令
start_cmd="${python3_path} app.py ---ca_cert=${ca_cert} --api_url=${api_url} --svc_token=${svc_token} >/dev/null 2>log/${app_folder}.log &"


# 日志目录
log_path="${install_base}/${app_folder}/log"
mkdir -p ${log_path}


#############################################################

# 启动程序
echo "start by cmd: ${start_cmd}"
cd ${install_path} && eval "${start_cmd}"
if [[ $? -ne 0 ]];then
    echo "start error, exit"
    exit 1
fi
#############################################################