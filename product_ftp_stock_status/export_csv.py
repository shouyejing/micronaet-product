# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2001-2014 Micronaet SRL (<http://www.micronaet.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import os
import sys
import logging
import openerp
import xlsxwriter
import openerp.netsvc as netsvc
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, expression, orm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT, 
    DEFAULT_SERVER_DATETIME_FORMAT, 
    DATETIME_FORMATS_MAP, 
    float_compare)


_logger = logging.getLogger(__name__)

class ProductProduct(orm.Model):
    ''' Model name: Product 
    '''    
    _inherit = 'product.product'
    
    # -------------------------------------------------------------------------
    # Scheduled action:
    # -------------------------------------------------------------------------
    def export_csv_stock_status_via_ftp_file(self, cr, uid, context=None):
        ''' Export and launch FTP publish
        '''        
        # ---------------------------------------------------------------------
        # Utility:
        # ---------------------------------------------------------------------
        def clean_ascii(value):
            ''' Clean not ascii char
            '''
            res = ''
            if not value:
                return tes
            for c in value:
                if ord(c) < 127:
                    res += c
                else:
                    res += '#'    
            return res
            
        # ---------------------------------------------------------------------
        # CSV file:
        # ---------------------------------------------------------------------
        csv_file = '/home/administrator/photo/xls/ftp/inventario.txt'
        sh_file = '/home/administrator/photo/xls/ftp/publish.sh'
        supplier_id = '30993'
        lang = 'en_US'
        
        # Setup context in correct lang
        if context is None:
            context = {}
        ctx = context.copy()
        ctx['lang'] = lang
        
        _logger.warning('Start generate CSV stock status: %s [lang: %s]' % (
            csv_file, lang))

        ftp_file = open(csv_file, 'w')
        header = 'Supplier ID,Item Number,Qty On Hand,Qty Backordered,' + \
            'Qty On Order,Item Next Availability Date,Item Discontinued,' + \
            'Item Description\n'
        ftp_file.write(header)
                
        # ---------------------------------------------------------------------
        # Start export product:
        # ---------------------------------------------------------------------
        product_pool = self.pool.get('product.product')
        product_ids = product_pool.search(cr, uid, [
            #('statistic_category', 'in', (
            #    'I01', 'I02', 'I03', 'I04', 'I05', 'I06')),
            ], context=ctx)
        for product in product_pool.browse(
                cr, uid, product_ids, context=ctx):
            if not product.default_code:
                _logger.warning('Error no code: %s' % product.id)
                continue
                
            ftp_file.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (
                supplier_id, # Supplier ID
                product.default_code, # Code
                product.mx_net_qty, # On hand
                '', # Qty backordered
                '', # Qty ordered
                '', # Qty next availability date
                '', # Item discontinued
                clean_ascii(product.name), # Item description
                ))
        ftp_file.close()       
                 
        # ---------------------------------------------------------------------
        # FTP publish
        # ---------------------------------------------------------------------
        _logger.warning('Publish file: %s [script: %s]' % (
            csv_file,
            sh_file,
            ))            

        import pdb; pdb.set_trace()    
        os.system(sh_file)
        _logger.warning('End publish FTP stock status')
        return True
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: