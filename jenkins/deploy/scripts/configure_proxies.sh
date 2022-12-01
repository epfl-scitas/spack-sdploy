#!/usr/bin/env bash
no_proxy="127.0.0.1,localhost,.epfl.ch,"
# fidis
no_proxy="${no_proxy},10.91.10.254,fadmin1,fadmin2,.fidis,localhost,127.0.0.1,fdata1,fdata2"
# helvetios
no_proxy="${no_proxy},10.91.*,hadmin1,hadmin2,helvetios,helvetios.cluster,localhost,127.0.0.1,helvetios.cluster,h???,h???-ib,h???-mgmt"
# izar
no_proxy="${no_proxy},10.91.16.,10.91.17.,10.91.18.,10.91.19.,10.91.24.,iadmin,.izar.local"
# jed
no_proxy="${no_proxy},172.16.4.*,10.91.*,jadmin1,jadmin2,scitas-internal-jsmartproxy,jed,jed.cluster,*.jed.cluster,jst???,jst???-mgmtadm,jst???-mgmt,jbm???,jbm???-mgmtadm,jbm???-mgmt,jhm???,jhm???-mgmtadm,jhm???-mgmt,jstorage-bmc,jswitch-main-spine??,jswitch-main-leaf??,jswitch-mgmt-spine??,jswitch-mgmt-leaf??,localhost,127.0.0.1,jed.cluster,j???,j???-mgmtadm,j???-mgmt"

export no_proxy
export NO_PROXY=${no_proxy}
#
export proxy_host="scitassrv9.epfl.ch"
export proxy_port="80"
#
export ftp_proxy="${proxy_host}:${proxy_port}"
export FTP_PROXY="${proxy_host}:${proxy_port}"
#
export http_proxy="${proxy_host}:${proxy_port}"
export HTTP_PROXY="${proxy_host}:${proxy_port}"
#
export https_proxy="${proxy_host}:${proxy_port}"
export HTTPS_PROXY="${proxy_host}:${proxy_port}"
export ALL_PROXY="${proxy_host}:${proxy_port}"
