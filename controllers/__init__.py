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
try:
    from chardet.universaldetector import UniversalDetector
except ImportError:
    import sys,os
    sys.path.append (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'libs', 'chardet-1.1')))
    from chardet.universaldetector import UniversalDetector

import simplejson
import csv
import itertools
import operator
import xmlrpclib

try:
    # embedded
    import openerp.addons.web.common.http as openerpweb
    from openerp.addons.web import common
    from openerp.addons.web.controllers.main import Import
except ImportError:
    # standalone
    from web import common
    import web.common.http as openerpweb
    from web.controllers.main import Import


class ChardetImport(Import):
    _cp_path = "/web/import2"

    @openerpweb.httprequest
    def detect_data(self, req, csvfile, csvsep=',', csvdel='"', csvcode='utf-8', jsonp='callback'):
        #detect encoding
        if csvcode == 'auto':
            u = UniversalDetector()
            for line in csvfile:
                u.feed(line)
            u.close()
            csvcode = u.result['encoding'].lower()
            csvfile.seek(0)

        # gb2312 gbk hz-gb-2312 hz-gb
        if csvcode == 'gb2312': csvcode = 'gbk'
        if 'hz' in csvcode: csvcode = 'hz'

        #remove bom
        if 'utf' in csvcode:
            if 'utf-8' in csvcode:
                contents = csvfile.read().decode('utf-8-sig').encode('utf-8')
                csvcode = 'utf-8'
            #FIXME not support utf-16
            if 'utf-16' in csvcode:
                contents = csvfile.read().decode(csvcode).encode('utf-16')
                csvcode = 'utf-16'
            #FIXME not support utf-32
            if 'utf-32' in csvcode:
                contents = csvfile.read().decode('utf-32be').encode('utf-32')
                csvcode = 'utf-32'
            csvfile.truncate(0)
            csvfile.write(contents)
            csvfile.seek(0)

        try:
            data = list(csv.reader(
                csvfile, quotechar=str(csvdel), delimiter=str(csvsep)))
        except csv.Error, e:
            csvfile.seek(0)
            return '<script>window.top.%s(%s);</script>' % (
                jsonp, simplejson.dumps({'error': {
                    'message': 'Error parsing CSV file: %s' % e,
                    # decodes each byte to a unicode character, which may or
                    # may not be printable, but decoding will succeed.
                    # Otherwise simplejson will try to decode the `str` using
                    # utf-8, which is very likely to blow up on characters out
                    # of the ascii range (in range [128, 256))
                    'preview': csvfile.read(200).decode('iso-8859-1')}}))

        try:
            return '<script>window.top.%s(%s);</script>' % (
                jsonp, simplejson.dumps(
                    #{'records': data[:10]}, encoding=csvcode))
                    {'records': data[:10], 'encoding':csvcode}, encoding=csvcode))
        except UnicodeDecodeError:
            return '<script>window.top.%s(%s);</script>' % (
                jsonp, simplejson.dumps({
                    'message': u"Failed to decode CSV file using encoding %s, "
                               u"try switching to a different encoding" % csvcode
                }))
        except:
            return '<script>window.top.%s(%s);</script>' % (
                jsonp, simplejson.dumps({
                    'message': u"Failed to decode CSV file using encoding %s, "
                               u"try switching to a different encoding" % csvcode
                }))


    @openerpweb.httprequest
    def import_data(self, req, model, csvfile, csvsep, csvdel, csvcode, jsonp,
                    meta):

        #remove bom
        if 'utf' in csvcode:
            if 'utf-8' in csvcode:
                contents = csvfile.read().decode('utf-8-sig').encode('utf-8')
                csvcode = 'utf-8'
            #FIXME not support utf-16
            if 'utf-16' in csvcode:
                contents = csvfile.read().decode(csvcode).encode('utf-16')
                csvcode = 'utf-16'
            #FIXME not support utf-32
            if 'utf-32' in csvcode:
                contents = csvfile.read().decode('utf-32be').encode('utf-32')
                csvcode = 'utf-32'
            csvfile.truncate(0)
            csvfile.write(contents)
            csvfile.seek(0)

        skip, indices, fields, context = \
            operator.itemgetter('skip', 'indices', 'fields', 'context')(
                simplejson.loads(meta, object_hook=common.nonliterals.non_literal_decoder))

        error = None
        if not (csvdel and len(csvdel) == 1):
            error = u"The CSV delimiter must be a single character"

        if not indices and fields:
            error = u"You must select at least one field to import"

        if error:
            return '<script>window.top.%s(%s);</script>' % (
                jsonp, simplejson.dumps({'error': {'message': error}}))

        # skip ignored records (@skip parameter)
        # then skip empty lines (not valid csv)
        # nb: should these operations be reverted?
        rows_to_import = itertools.ifilter(
            None,
            itertools.islice(
                csv.reader(csvfile, quotechar=str(csvdel), delimiter=str(csvsep)),
                skip, None))

        # if only one index, itemgetter will return an atom rather than a tuple
        if len(indices) == 1: mapper = lambda row: [row[indices[0]]]
        else: mapper = operator.itemgetter(*indices)

        data = None
        error = None
        try:
            # decode each data row
            data = [
                [record.decode(csvcode) for record in row]
                for row in itertools.imap(mapper, rows_to_import)
                # don't insert completely empty rows (can happen due to fields
                # filtering in case of e.g. o2m content rows)
                if any(row)
            ]
        except UnicodeDecodeError:
            error = u"Failed to decode CSV file using encoding %s" % csvcode
        except csv.Error, e:
            error = u"Could not process CSV file: %s" % e

        # If the file contains nothing,
        if not data:
            error = u"File to import is empty"
        if error:
            return '<script>window.top.%s(%s);</script>' % (
                jsonp, simplejson.dumps({'error': {'message': error}}))

        try:
            (code, record, message, _nope) = req.session.model(model).import_data(
                fields, data, 'init', '', False,
                req.session.eval_context(context))
        except xmlrpclib.Fault, e:
            error = {"message": u"%s, %s" % (e.faultCode, e.faultString)}
            return '<script>window.top.%s(%s);</script>' % (
                jsonp, simplejson.dumps({'error':error}))

        if code != -1:
            return '<script>window.top.%s(%s);</script>' % (
                jsonp, simplejson.dumps({'success':True}))

        msg = u"Error during import: %s\n\nTrying to import record %r" % (
            message, record)
        return '<script>window.top.%s(%s);</script>' % (
            jsonp, simplejson.dumps({'error': {'message':msg}}))


#def wrap_detect_data(func):
    #def _func(*args, **kwds):
        ##if kwds.get('csvcode', 'utf-8') == 'auto':
            ##u = UniversalDetector()
            ##for line in args[2]:
                ##u.feed(line)
            ##u.close()
            ##result = u.result
            ##print result
        #print args, kwds
        #print 'aaaaaaaaaaaaaaaaaaa'
        #func(*args, **kwds)
    #return _func
##Import.detect_data = openerpweb.httprequest(Import.detect_data)
#Import.detect_data = wrap_detect_data(Import.detect_data)
#Import.detect_data = openerpweb.httprequest(Import.detect_data)

#def wrap_import_data(func):
    #def _func(*args, **kwds):
        #func(*args, **kwds)
    #return _func
#Import.import_data = wrap_detect_data(Import.import_data)






# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
