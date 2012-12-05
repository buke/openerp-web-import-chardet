openerp-web-import-chardet
==========================
::

  .. _fig_0601:
  .. figure:: http://www.openerp-china.org/templates/image/openerp-logo.png

     插图 6-1 神奇的2


然后,就可以在任意地方使用 :ref:`fig_0601` 来指代,
实际输出的就是 "插图 6-1 神奇的2"


.. _fig_0601:
.. figure:: http://www.openerp-china.org/templates/image/openerp-logo.png

   插图 6-1 神奇的2

   

Use python chardet module to detect import csv file encoding.
And remove BOM header in UTF8 file.

Detects
 - ASCII, UTF-8
 - Big5, GBK, GB2312, HZ-GB, HZ-GB-2312 (Traditional and Simplified Chinese)
 - EUC-JP, SHIFT_JIS, ISO-2022-JP (Japanese)
 - EUC-KR, ISO-2022-KR (Korean)
 - KOI8-R, MacCyrillic, IBM855, IBM866, ISO-8859-5, windows-1251 (Cyrillic)
 - ISO-8859-2, windows-1250 (Hungarian)
 - ISO-8859-5, windows-1251 (Bulgarian)
 - windows-1252 (English)
 - ISO-8859-7, windows-1253 (Greek)
 - ISO-8859-8, windows-1255 (Visual and Logical Hebrew)
 - TIS-620 (Thai)

This module is web addon and only for web.

Depends:
 - python chardet (This module have chartdet-1.1, it would use the newer if you install a newer version.)



功能：
---------
自动检测OpenERP 导入的CSV文件编码 
自动移除UTF8文件的BOM.


支持编码：
---------
 - ASCII, UTF-8
 - Big5, GBK, GB2312, HZ-GB, HZ-GB-2312 (简体/繁体中文)
 - EUC-JP, SHIFT_JIS, ISO-2022-JP (日文)
 - EUC-KR, ISO-2022-KR (韩文)
 - KOI8-R, MacCyrillic, IBM855, IBM866, ISO-8859-5, windows-1251 (斯拉夫文)
 - ISO-8859-2, windows-1250 (匈牙利文)
 - ISO-8859-5, windows-1251 (保加利亚文)
 - windows-1252 (英文)
 - ISO-8859-7, windows-1253 (希腊文)
 - ISO-8859-8, windows-1255 (希伯来文)
 - TIS-620 (泰文)

依赖模块:
---------
 - python chardet (本模块已内含chartdet-1.1。如果系统安装了新版本，则使用您安装的新版本.)


更多说明，请关注 http://my.oschina.net/wangbuke



