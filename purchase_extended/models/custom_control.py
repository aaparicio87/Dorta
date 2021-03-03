from odoo import api, fields, models, _
from datetime import datetime

class custom_control(models.Model):
    _name = 'custom.control'
    _rec_name = 'partner_id'

    state = fields.Selection(
        [('borrardor', 'Borrador'),
         ('abierto', 'Abierto'),
         ('pagado', 'Pagado'),
         ('cerrado', 'Cerrado'),
         ], string='Estatus', default='borrardor')
    name = fields.Char("")
    purchase_id = fields.Many2one('purchase.order')
    purchase_order_id = fields.Many2one('purchase.order', "Orden de Compra")
    partner_id = fields.Many2one('res.partner', string="Proveedor")
    issue_date = fields.Datetime(string="Fecha del Problema")
    status_order = fields.Char(string="Estatus del Orden", readonly=True)
    document_count = fields.Integer("Documentos", compute='_compute_published_document')
    doc_uploaded = fields.Boolean("Documentos Cargados")
    date_shipment = fields.Date("Fecha de Envio")
    supplier_receipt_date = fields.Date("Fecha de recepcion de proveedora")
    confirmation_date = fields.Date("Fecha de Confirmacion")
    proforma_date = fields.Date("fecha de Pro-forma")
    departure_date = fields.Date("Fecha de Salida")
    arrival_date = fields.Date("Fecha de Arribo")
    output_port_id = fields.Many2one('output.port',"Puerto de Salida")
    arrival_port_id = fields.Many2one('arrival.port',"Puerto de Arribo")
    payment_condition = fields.Many2one('account.payment.term', "Condicion de Pago")
    shipping_name = fields.Char("Nombre del envio")
    steam_name = fields.Char("Nombre del Equipo")
    conform_date = fields.Date("Fecha de confirmacion")
    final_date = fields.Date("Fecha final")
    date_arrival = fields.Date("Fecha de Arribo")
    courier_number = fields.Char("Numero del Mensajero")
    invoice_n = fields.Char("Factura N°")
    invoice_currency_id = fields.Many2one('res.currency',"Moneda de La Factura")
    exchange_rate = fields.Float("Tipo de Cambio")
    customs_dollar = fields.Float("Dolar Personalizado")
    invoice_date = fields.Date("Fecha de La Factura")
    due_date = fields.Date("Fecha de Vencimiento")
    fob_value_currency = fields.Float("FOB Moneda de Valor")
    fob_bs_currency = fields.Float("FOB Bs Valor")
    currency_insurance = fields.Float("Seguro de Moneda")
    bs_insurance = fields.Float("Bs Seguro")
    freight_currency = fields.Float("Modena de Flete")
    freight_bs = fields.Float("Carga Bs")
    cif_currency = fields.Float("CIF Moneda", compute='compute_cif_currency')
    cif_bs = fields.Float("CIF Bs", compute='compute_cif_bs')
    invoice = fields.Boolean("Factura")
    Bill_lading = fields.Boolean("Guia de Carga(BL)")
    free_sale = fields.Boolean("Venta Libre")
    analysis = fields.Boolean("Analisis")
    age = fields.Boolean("Edad")
    origin = fields.Boolean("Origen")
    health = fields.Boolean("Salud")
    date_sending_document = fields.Date("Fecha de Envio de Documentos")
    doc_arrival_date = fields.Date("Fecha de Arribo")
    doc_courier_number = fields.Char(size=(10))
    numbering_bLs = fields.Char(size=(10))
    container_type = fields.Selection(
        [('con_20_feet', 'CONTENERDOR 20 PIES'),
         ('con_40_feet', 'CONTENEDOR 40 PIES'),
         ('consolidated', 'CONSOLIDADO'),
         ], string='Tipo de contenedor')
    qty_container = fields.Char(size=(10))
    number_container = fields.Char("Numero de Contenedores")
    certificate_number = fields.Char(size=(10))
    merchandise_arrival_date = fields.Date("Fecha de Arribo de la Mercancia al Puerto")
    transfer_date_warehouse = fields.Date("Fecha de Transferencia al Almacen")
    store_id = fields.Many2one('store.store',"Tienda")

    # def action_document(self):
    #     action = self.env.ref('purchase_extended.view_document_document_tree').read()[0]
    #     return action

    # @api.onchange('purchase_order_id', 'partner_id', 'status_order')
    # def onchange_purchase_order(self):
    #     # for rec in self:
    #     #     for res in rec.purchase_order_id:
    #     #         print("2222222222222", res.state)
    #     #         rec.status_order = res.state
    #     #         rec.issue_date = res.date_order
    #     #         if res.state == 'purchase':
    #     #             rec.state = 'paid'
    #     purchase_order = self.purchase_order_id
    #     self.status_order = purchase_order.state
    #     self.issue_date = purchase_order.date_order
    #     if purchase_order.state == 'purchase':
    #         self.state = 'paid'
    #     else:
    #         self.state = 'draft'

    def _compute_published_document(self):
        for rec in self:
            document = self.env['document.document'].search([])
            rec.document_count = len(document)

    def action_cerrar(self):
        for order in self:
            order.state = 'closed'

    def action_validate(self):
        for order in self:
            order.state = 'open'

    @api.onchange('fob_value_currency')
    def onchange_fob_value_currency(self):
        if self.fob_value_currency and self.exchange_rate:
            self.fob_bs_currency = self.exchange_rate / self.fob_value_currency

    @api.onchange('fob_bs_currency')
    def onchange_fob_bs_currency(self):
        if self.fob_bs_currency and self.exchange_rate:
            self.fob_value_currency = self.exchange_rate / self.fob_bs_currency

    @api.onchange('bs_insurance')
    def onchange_bs_insurance(self):
        if self.bs_insurance and self.exchange_rate:
            self.currency_insurance = self.exchange_rate / self.bs_insurance

    @api.onchange('currency_insurance')
    def onchange_currency_insurance(self):
        if self.currency_insurance and self.exchange_rate:
            self.bs_insurance = self.exchange_rate / self.currency_insurance

    @api.onchange('freight_currency')
    def onchange_freight_currency(self):
        if self.freight_currency and self.exchange_rate:
            self.freight_bs = self.exchange_rate / self.freight_currency

    @api.onchange('freight_bs')
    def onchange_freight_bs(self):
        if self.freight_bs and self.exchange_rate:
            self.freight_currency = self.exchange_rate / self.freight_bs

    @api.depends('fob_bs_currency', 'freight_bs', 'bs_insurance')
    def compute_cif_bs(self):
        self.cif_bs = self.fob_bs_currency + self.freight_bs + self.bs_insurance

    @api.depends('freight_currency', 'currency_insurance', 'fob_value_currency')
    def compute_cif_currency(self):
        self.cif_currency = self.freight_currency + self.currency_insurance + self.fob_value_currency


class output_port(models.Model):
    _name = 'output.port'

    name = fields.Char("Name")


class output_port(models.Model):
    _name = 'arrival.port'

    name = fields.Char("Name")


class store_store(models.Model):
    _name = 'store.store'
    _rec_name = 'warehouse'

    code = fields.Char("Code")
    warehouse = fields.Char("Warehouse")
