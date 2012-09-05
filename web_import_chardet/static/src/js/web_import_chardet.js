/*############################################################################
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
############################################################################*/

openerp.web_import_chardet = function(openerp) {

    function jsonp(form, attributes, callback) {
        attributes = attributes || {};
        var options = {jsonp: _.uniqueId('import_callback_')};
        window[options.jsonp] = function () {
            delete window[options.jsonp];
            callback.apply(null, arguments);
        };
        if ('data' in attributes) {
            _.extend(attributes.data, options);
        } else {
            _.extend(attributes, {data: options});
        }
        $(form).ajaxSubmit(attributes);
    }

    openerp.web.DataImport = openerp.web.DataImport.extend({
        start: function() {
            var self = this;
            this._super();

            var csv_encoding = this.$element.find('#csv_encoding')
            csv_encoding.empty();
            csv_encoding.append('<option value="auto">Auto Detect</option>');

            csv_encoding.append('<option value="utf-8">UTF-8</option>');
            csv_encoding.append('<option value="ascii">Ascii</option>');
            //csv_encoding.append('<option value="utf-16">UTF-16</option>');
            //csv_encoding.append('<option value="utf-32">UTF-32</option>');

            csv_encoding.append('<option value="big5">Big5 (Chinese)</option>');
            csv_encoding.append('<option value="gbk">GBK (Chinese)</option>');
            //csv_encoding.append('<option value="euc-tw">EUC-TW(Chinese)</option>');
            csv_encoding.append('<option value="hz">HZ (Chinese)</option>');
            //csv_encoding.append('<option value="iso-2022-cn">ISO-2022-CN(Chinese)</option>');

            csv_encoding.append('<option value="euc-jp">EUC-JP (Japanese)</option>');
            csv_encoding.append('<option value="shift-jis">SHIFT_JIS (Japanese)</option>');
            csv_encoding.append('<option value="iso-2022-jp">ISO-2022-JP (Japanese)</option>');

            csv_encoding.append('<option value="euc-kr">EUC-KR (Korean)</option>');
            csv_encoding.append('<option value="iso-2022-kr">ISO-2022-KR (Korean)</option>');

            csv_encoding.append('<option value="koi8-r">KOI8-R (Cyrillic)</option>');
            csv_encoding.append('<option value="maccyrillic">MacCyrillic (Cyrillic)</option>');
            csv_encoding.append('<option value="ibm855">IBM855 (Cyrillic)</option>');
            csv_encoding.append('<option value="ibm866">IBM866 (Cyrillic)</option>');
            csv_encoding.append('<option value="iso-8859-5">ISO-8859-5 (Cyrillic)</option>');
            csv_encoding.append('<option value="windows-1251">windows-1251 (Cyrillic)</option>');

            csv_encoding.append('<option value="iso-8859-2">ISO-8859-2 (Hungarian)</option>');
            csv_encoding.append('<option value="windows-1250">windows-1250 (Hungarian)</option>');

            csv_encoding.append('<option value="iso-8859-5">ISO-8859-5 (Bulgarian)</option>');
            csv_encoding.append('<option value="windows-1251">windows-1251 (Bulgarian)</option>');

            csv_encoding.append('<option value="windows-1252">windows-1252 (English)</option>');

            csv_encoding.append('<option value="iso-8859-7">ISO-8859-7 (Greek)</option>');
            csv_encoding.append('<option value="windows-1253">windows-1253 (Greek)</option>');

            csv_encoding.append('<option value="iso-8859-8">ISO-8859-8 (Hebrew)</option>');
            csv_encoding.append('<option value="windows-1255">windows-1255 (Hebrew)</option>');

            csv_encoding.append('<option value="tis-620">TIS-620 (Thai)</option>');

            $('#csvfile').change(function() {
                $('#csv_encoding option').removeAttr('selected');
                $('#csv_encoding option[value=auto]').attr('selected', 'selected');
            });


        },

        do_import: function() {
            if(!this.$element.find('#csvfile').val()) { return; }
            var lines_to_skip = parseInt(this.$element.find('#csv_skip').val(), 10);
            var with_headers = this.$element.find('#file_has_headers').prop('checked');
            if (!lines_to_skip && with_headers) {
                lines_to_skip = 1;
            }
            var indices = [], fields = [];
            this.$element.find(".sel_fields").each(function(index, element) {
                var val = element.value;
                if (!val) {
                    return;
                }
                indices.push(index);
                fields.push(val);
            });

            jsonp(this.$element.find('#import_data'), {
                url: '/web/import2/import_data',
                data: {
                    model: this.model,
                    meta: JSON.stringify({
                        skip: lines_to_skip,
                        indices: indices,
                        fields: fields,
                        context: this.context
                    })
                }
            }, this.on_import_results);
        },

        on_autodetect_data: function() {
            //this.$element.find('#csv_encoding option').removeAttr('selected');
            if(!this.$element.find('#csvfile').val()) { return; }
            jsonp(this.$element.find('#import_data'), {
                url: '/web/import2/detect_data'
            }, this.on_import_results);
        },

        on_import_results: function(results) {
            if (results['encoding']) {
                this.$element.find('#csv_encoding option').removeAttr('selected');
                this.$element.find('#csv_encoding option[value=' + results['encoding'] + ']').attr('selected', 'selected');
            }
            else{
                this.$element.find('#csv_encoding option').removeAttr('selected');
            }
            this._super(results);
        },

    });


};


