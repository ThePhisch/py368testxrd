"""
xrootd Request-Codes
"""
from typing import Tuple

kXR_auth = 3000
kXR_query = 3001
kXR_chmod = 3002
kXR_close = 3003
kXR_dirlist = 3004
kXR_getfile = 3005
kXR_protocol = 3006
kXR_login = 3007
kXR_mkdir = 3008
kXR_mv = 3009
kXR_open = 3010
kXR_ping = 3011
kXR_chkpoint = 3012
kXR_read = 3013
kXR_rm = 3014
kXR_rmdir = 3015
kXR_sync = 3016
kXR_stat = 3017
kXR_set = 3018
kXR_write = 3019
kXR_admin = 3020
kXR_prepare = 3021
kXR_statx = 3022
kXR_endsess = 3023
kXR_bind = 3024
kXR_readv = 3025
kXR_verifyw = 3026
kXR_locate = 3027
kXR_truncate = 3028
kXR_writev = 3031
kXR_fattr = 3032

kXR_ok = 0
kXR_oksofar = 4000
kXR_attn = 4001
kXR_authmore = 4002
kXR_error = 4003
kXR_redirect = 4004
kXR_wait = 4005
kXR_waitresp = 4006

kXR_asyncab = 5000
kXR_asyncdi = 5001
kXR_asyncms = 5002
kXR_asyncrd = 5003
kXR_asyncwt = 5004
kXR_asyncav = 5005
kXR_asynunav = 5006
kXR_asyncgo = 5007
kXR_asynrsp = 5008

kXR_fullurl = 1
kXR_multipr = 3
kXR_readrdok = 4

Ability = 0

kXR_asyncap = 128

kXR_vfs = 1

kXR_QStats = 1
kXR_QPrep = 2
kXR_Qcksum = 3
kXR_Qxattr = 4
kXR_Qspace = 5
kXR_Qckscan = 6
kXR_Qconf = 7
kXR_Qvisa = 8


kXR_mkdirp = 1
kXR_online = 1
kXR_dstat = 2
kXR_dcksm = 4

kXR_compress = 1
kXR_delete = 2
kXR_force = 4
kXR_new = 8
kXR_open_read = 16
kXR_open_updt = 32

kXR_async = 64
kXR_refresh = 128
kXR_mkpath = 256
kXR_prefname = 256
kXR_addpeers = 512
kXR_retstat = 1024
kXR_replica = 2048
kXR_posc = 4096
kXR_nowait = 8192

kXR_cancel = 1
kXR_notify = 2
kXR_noerrs = 4
kXR_stage = 8
kXR_wmode = 16
kXR_coloc = 32
kXR_fresh = 64
kXR_usetcp = 128

kXR_doSync = 1

KXR_file = 0
KXR_xset = 1
KXR_isDir = 2
KXR_other = 4
KXR_offline = 8

KXR_secreqs = 1

# kXR_ur = b"\x01\x00"
# kXR_uw = b"\x00\x80"
# kXR_ux = b"\x00\x40"
# kXR_gr = b"\x00\x20"
# kXR_gw = b"\x00\x10"
# kXR_gx = b"\x00\x08"
# kXR_or = b"\x00\x04"
# kXR_ow = b"\x00\x02"
# kXR_ox = b"\x00\x01"

kXR_ur = 256
kXR_uw = 128
kXR_ux = 64
kXR_gr = 32
kXR_gw = 16
kXR_gx = 8
kXR_or = 4
kXR_ow = 2
kXR_ox = 1

kXR_mode: Tuple[int, ...] = (
    256,
    128,
    64,
    32,
    16,
    8,
    4,
    2,
    1,
)  # 0 -> 9
