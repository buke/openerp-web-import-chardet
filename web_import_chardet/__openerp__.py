# -*- coding: utf-8 -*-
##############################################################################
#    web_import_chardet
#    Auto Detect Import File Encoding & Remove BOM Header In UTF8 File.
#    Copyright 2012 wangbuke <wangbuke@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For Commercial or OEM, you need to contact the author and/or licensor
#    and ask for their permission.
##############################################################################

{
    "name": "Auto Detect Import File Encoding & Delete BOM Header",
    'version': '1.0',
    'category': 'Web',
    'description': """
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


    """,
    'author': 'wangbuke@gmail.com',
    'website': 'http://my.oschina.net/wangbuke',
    'license': 'AGPL-3',
    'depends': ['web'],
    'data': [],
    'auto_install': False,
    'web_preload': True,
    'js': ['static/src/js/web_import_chardet.js'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
