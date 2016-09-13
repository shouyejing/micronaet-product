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

class StructureStructure(orm.Model):
    """ Model name: StructureStructure
    """
    
    _name = 'structure.structure'
    _description = 'Product code structure'
    
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'note': fields.text('Note'),
        }

class StructureBlock(orm.Model):
    """ Model name: StructureBlock
    """
    
    _name = 'structure.block'
    _description = 'Structure block'
    _order = 'from'
    
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'structure_id': fields.many2one(
            'structure.structure', 'Code structure'), 
        'from': fields.integer('From char', required=True), 
        'to': fields.integer('To char', required=True),
        'mandatory': fields.boolean('Mandatory'),        
        'note': fields.text('Note'),
        }

class StructureBlockValore(orm.Model):
    """ Model name: StructureBlockValue
    """
    
    _name = 'structure.block.value'
    _description = 'Block value'
    _order = 'code'
    
    _columns = {
        'code': fields.char('Code', size=10, required=True),
        'name': fields.char('Name', size=64, required=True, translate=True),        
        'block_id': fields.many2one('structure.block', 'Block'), 
        'note': fields.text('Note'),
        }

class StructureBlock(orm.Model):
    """ Model name: StructureBlock inherited for add 2many relation fields
    """
    
    _inherit = 'structure.block'
    
    _columns = {
        'value_ids': fields.one2many(
            'structure.block.value', 'block_id', 'Value'), 
        }

class StructureStructure(orm.Model):
    """ Model name: StructureStructure inherited for add 2many relation fields
    """
    
    _inherit = 'structure.structure'

    _columns = {
        'block_ids': fields.one2many(
            'structure.block', 'structure_id', 'Block'), 
        }

class ProductProduct(orm.Model):
    """ Model name: Add extra fields to product
    """
    
    _inherit = 'product.product'
    
    def generate_name_from_code(self, cr, uid, ids, context=None):
        ''' Generate product name depend on structure and code insert
        '''
        product_proxy = self.browse(cr, uid, ids, context=context)[0]
        if not product_proxy.default_code or not product_proxy.structure_id:
            raise osv.except_osv(
                _('Error'), 
                _('Insert manadatory fields: code and structure'),
                )
        name = '...'
        
        # TODO create proceduro to generate name of product:
        
        return self.write(cr, uid, ids, {
            'name': name, 
            }, context=context)
        
    _columns = {
        'structure_id': fields.many2one(
            'structure.structure', 'Code structure'), 
        }
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
