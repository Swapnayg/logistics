import random
from flask import Blueprint
from flask import Flask, render_template, request, Response, send_file , redirect, session, url_for, jsonify
from extensions import db
from sqlalchemy import and_, insert
from ledger import Ledger
from ledger2 import Ledger2
from party import Party
from vehicles import Vehicles
from clients import Clients
from supplier import Supplier
from ledger import Ledger
from bookingPerson import BookingPerson
from catgeory import Categories
from citysetup import CitySetup
from container import Container
from dailyexpenses import DailyExpenses
from designation import Designation
from modeofpayment import ModeOfPayment
from province import Province
from units import Units
from accountTypes import AccountTypes
from accountSubTypes import AccountSubTypes
from receivingPoints import ReceivingPoints
from warehouse import Warehouse
from products import Products
from employee import Exmployee
from vehiclebroker import VehicleBroker
from shippingLine import ShippingLine
from stockin import Stockin
from tripeexpense import TripExpense
from partybill import PartyBill
from oilpso import OilPso
from goodsnlc import GoodsNlc
from clientgroup import ClientGroup
from productctegory import ProductCategory
from tblProduct import TblProduct
from stocktransfer import StockTrasfer
from tblQuote import TblQuote
from quoteitems import QuoteItems
from tblInvoice import TblInvoice
from invoiceItems import InvoiceItems
from reccIncoice import TblReccInvoice
from reccItems import ReccItems
from tblOrder import TblOrder
from purchItems import PurchItems
from stkRtn import TblStockRtn
from returnItems import ReturnItems
from clnstkrtn import TblClnStockRtn
from clnStkRtnItems import ClientReturnItems
from chartofAccount import ChartOfAccount
from inwarehouse import InvWarehouses
from users import Users
from api.refreshcoacustomer import RefreshCOA_Customer

class RefreshTables():

    def refresh_goods_oils_manifest(manifest_id, mani_type):
        manifest_values = ''
        if(mani_type == 'goods'):
            manifest_values = GoodsNlc.query.filter(GoodsNlc.id == int(manifest_id)).first()
        elif(mani_type == 'oil'): 
            manifest_values = OilPso.query.filter(OilPso.id == int(manifest_id)).first()
        party_id = int(manifest_values.parties)
        get_party = Party.query.get(party_id)
        parrty_bills = PartyBill.query.filter(PartyBill.party_id == party_id).all()
        for bill in parrty_bills:
            bill_bilties = str(bill.invoice_bilties).strip()
            bill_bilties_li = bill_bilties.split(",")
            if str(manifest_id) in bill_bilties_li:
                party_bill_num  = str(bill.invoice_no).strip()
                party_bill_date  = str(bill.invoice_date).strip()
                party_balance = 0
                if(str(bill.invoice_type).strip() == "goods"):
                    for li in bill_bilties_li:
                        manifest_gd_values = GoodsNlc.query.filter(GoodsNlc.id == int(li)).first()
                        party_balance = party_balance + int(manifest_gd_values.freight)
                elif(str(bill.invoice_type).strip() == "oil"):
                    for li in bill_bilties_li:
                        manifest_oil_values = OilPso.query.filter(OilPso.id == int(li)).first()
                        party_balance = party_balance + int(manifest_oil_values.freight)
                ledger_values = Ledger.query.filter(and_(Ledger.ledger_account_no == int(str(get_party.chart_accnt)),Ledger.ledger_gen_date == party_bill_date,Ledger.ledger_bill == party_bill_num,Ledger.ledger_type == "party" )).one()
                ledger_values.ledger_debit_amount = str(party_balance)
                ledger_values.ledger_balance = str(party_balance)
                bill.invoice_balance = str(party_balance)
                db.session.flush()
                db.session.commit()
                RefreshCOA_Customer.refresh_COA_Party(str(get_party.chart_accnt))
                break
        
    def deleteGoods_ledger(id):
        del_manif_goods_set = GoodsNlc.query.get(int(id))
        del_ledger_data = Ledger.__table__.delete().where(Ledger.ledger_bill == str(del_manif_goods_set.bilty_no).strip())
        db.session.execute(del_ledger_data)
        db.session.commit()

    def deleteOils_ledger(id):
        del_manif_oils_set = OilPso.query.get(int(id))
        del_oil_ledger_data = Ledger.__table__.delete().where(Ledger.ledger_bill == str(del_manif_oils_set.bilty_no).strip())
        db.session.execute(del_oil_ledger_data)
        db.session.commit()
        
        
    def delete_Goods_Bill(id,userid):
        del_manif_goods_set = GoodsNlc.query.get(int(id))
        if(del_manif_goods_set.bill_status != "pending"):
            party_bills = PartyBill.query.filter(PartyBill.party_id == int(del_manif_goods_set.parties)).all()
            for p_bilty in party_bills:
                get_party = Party.query.get(int(str(p_bilty.party_id)))
                prev_bilties = str(p_bilty.invoice_bilties).strip()
                prev_biltiesli = prev_bilties.split(",")
                if str(del_manif_goods_set.id) in prev_biltiesli:
                    new_bill_sub_total = 0
                    prev_biltiesli.remove(str(del_manif_goods_set.id))
                    for p_bilty_n in prev_biltiesli:
                        vah_goods_new = GoodsNlc.query.filter(GoodsNlc.id == int(p_bilty_n)).one()
                        new_bill_sub_total = new_bill_sub_total + int(str(vah_goods_new.freight).strip())
                    ledger_values = Ledger.query.filter(and_(Ledger.ledger_account_no == int(str(get_party.chart_accnt)),Ledger.ledger_gen_date == p_bilty.invoice_date,Ledger.ledger_bill == p_bilty.invoice_no,Ledger.ledger_type == "party" )).one()
                    ledger_values.ledger_debit_amount = str(new_bill_sub_total)
                    ledger_values.ledger_balance = str(new_bill_sub_total)
                    p_bilty.invoice_balance = str(new_bill_sub_total)
                    p_bilty.invoice_bilties = str(','.join(prev_biltiesli))
                    db.session.flush()
                    db.session.commit()
                    RefreshCOA_Customer.refresh_COA_Comm(userid)
                    RefreshCOA_Customer.refresh_COA_Party(str(get_party.chart_accnt))
        del_ledger_data = Ledger.__table__.delete().where(Ledger.ledger_bill == str(del_manif_goods_set.bilty_no).strip())
        db.session.execute(del_ledger_data)
        db.session.delete(del_manif_goods_set)
        db.session.commit()
        
    def delete_Oils_Bill(id):
        del_manif_oils_set = OilPso.query.get(int(id))
        if(del_manif_oils_set != "pending"):
            party_bills = PartyBill.query.filter(PartyBill.party_id == int(del_manif_oils_set.parties)).all()
            for p_bilty in party_bills:
                get_party = Party.query.get(int(str(p_bilty.party_id)))
                prev_bilties = str(p_bilty.invoice_bilties).strip()
                prev_biltiesli = prev_bilties.split(",")
                if str(del_manif_oils_set.id) in prev_biltiesli:
                    new_bill_sub_total = 0
                    prev_biltiesli.remove(str(del_manif_oils_set.id))
                    for p_bilty_n in prev_biltiesli:
                        vah_oils_new = OilPso.query.filter(OilPso.id == int(p_bilty_n)).one()
                        new_bill_sub_total = new_bill_sub_total + int(str(vah_oils_new.freight).strip())
                    ledger_values = Ledger.query.filter(and_(Ledger.ledger_account_no == int(str(get_party.chart_accnt)),Ledger.ledger_gen_date == p_bilty.invoice_date,Ledger.ledger_bill == p_bilty.invoice_no,Ledger.ledger_type == "party" )).one()
                    ledger_values.ledger_debit_amount = str(new_bill_sub_total)
                    ledger_values.ledger_balance = str(new_bill_sub_total)
                    p_bilty.invoice_balance = str(new_bill_sub_total)
                    p_bilty.invoice_bilties = str(','.join(prev_biltiesli))
                    db.session.flush()
                    db.session.commit()
        del_oil_ledger_data = Ledger.__table__.delete().where(Ledger.ledger_bill == str(del_manif_oils_set.bilty_no).strip())
        db.session.execute(del_oil_ledger_data)
        db.session.delete(del_manif_oils_set)
        db.session.commit()

