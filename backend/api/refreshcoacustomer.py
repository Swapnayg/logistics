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

class RefreshCOA_Customer():

    def refresh_COA_Customer(c_id):
        get_client_coa = ChartOfAccount.query.filter(ChartOfAccount.id == int(c_id)).one()
        sum_client_leg = Ledger2.query.filter(and_(Ledger2.ledger_account_no == int(c_id),Ledger2.ledger_type == "client" )).order_by(Ledger2.id.asc()).all()
        get_client = Clients.query.filter(and_(Clients.client_name == str(get_client_coa.accnt_name).strip().lower(),Clients.userid == get_client_coa.userid)).one()
        sum_client_leg_val = 0
        sum_client_cash_val = 0
        legder_balnce = 0
        for client_leg_result in sum_client_leg:
            if(int(client_leg_result.ledger_debit_amount) == 0):
                legder_balnce = (legder_balnce) + int(client_leg_result.ledger_credit_amount)
            elif(int(client_leg_result.ledger_credit_amount) == 0):
                legder_balnce = (legder_balnce) - int(client_leg_result.ledger_debit_amount)
            client_leg_result.ledger_balance = legder_balnce
            db.session.flush()
            db.session.commit() 
            sum_client_leg_val += int(client_leg_result.ledger_debit_amount)
            sum_client_cash_val += int(client_leg_result.ledger_credit_amount)    
        get_client_coa.networth = legder_balnce
        get_client.networth = legder_balnce
        db.session.flush()
        db.session.commit()
        
        
    def refresh_COA_Supplier(s_id):
        get_suppl_coa = ChartOfAccount.query.filter(ChartOfAccount.id == int(s_id)).one()
        sum_suppl_leg = Ledger2.query.filter(and_(Ledger2.ledger_account_no == int(s_id),Ledger2.ledger_type == "supplier" )).order_by(Ledger2.id.asc()).all()
        get_suppl = Supplier.query.filter(and_(Supplier.suppl_name == str(get_suppl_coa.accnt_name).strip().lower(),Supplier.userid == get_suppl_coa.userid)).one()
        sum_suppl_leg_val = 0
        sum_suppl_cash_val = 0
        legder_balnce = 0
        for suppl_leg_result in sum_suppl_leg:
            if(int(suppl_leg_result.ledger_debit_amount) == 0):
                legder_balnce = (legder_balnce) + int(suppl_leg_result.ledger_credit_amount)
            elif(int(suppl_leg_result.ledger_credit_amount) == 0):
                legder_balnce = (legder_balnce) - int(suppl_leg_result.ledger_debit_amount)
            suppl_leg_result.ledger_balance = legder_balnce
            db.session.flush()
            db.session.commit() 
            sum_suppl_leg_val += int(suppl_leg_result.ledger_debit_amount)
            sum_suppl_cash_val += int(suppl_leg_result.ledger_credit_amount)    
        get_suppl_coa.networth = legder_balnce
        get_suppl.networth = legder_balnce
        db.session.flush()
        db.session.commit()
    
    def refresh_COA_Party(p_id):
        get_party_chart = ChartOfAccount.query.filter(ChartOfAccount.id == int(str(p_id))).one()
        sum_party_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == int(str(p_id)),Ledger.ledger_type == "party" )).order_by(Ledger.id.asc()).all()
        get_party = Party.query.filter(and_(Party.english_name == str(get_party_chart.accnt_name).strip().lower(),Party.userid == get_party_chart.userid)).one()
        sum_party_leg_val = 0
        sum_party_cash_val = 0
        legder_balnce = 0
        for party_leg_result in sum_party_leg:
            if(int(party_leg_result.ledger_debit_amount) == 0):
                legder_balnce = (legder_balnce) + int(party_leg_result.ledger_credit_amount)
            elif(int(party_leg_result.ledger_credit_amount) == 0):
                legder_balnce = (legder_balnce) - int(party_leg_result.ledger_debit_amount)
            party_leg_result.ledger_balance = legder_balnce
            db.session.flush()
            db.session.commit() 
            sum_party_leg_val += int(party_leg_result.ledger_debit_amount)
            sum_party_cash_val += int(party_leg_result.ledger_credit_amount)    
        get_party_chart.networth = -(sum_party_leg_val) + sum_party_cash_val
        get_party.net_amount = -(sum_party_leg_val) + sum_party_cash_val
        db.session.flush()
        db.session.commit()
    
    def refresh_COA_Vehicle(v_id):
        get_vehicle_chart = ChartOfAccount.query.filter(ChartOfAccount.id == int(str(v_id))).one()
        sum_veh_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == int(str(v_id)),Ledger.ledger_type == "vehicle",Ledger.userid == get_vehicle_chart.userid)).order_by(Ledger.id.asc()).all()
        get_vehicle = Vehicles.query.filter(and_(Vehicles.vehicle_num == str(get_vehicle_chart.accnt_name).strip().lower(),Vehicles.userid == get_vehicle_chart.userid)).one()
        sum_veh_leg_val = 0
        sum_veh_cash_val = 0
        legder_balnce = 0
        for veh_leg_result in sum_veh_leg:
            if(int(veh_leg_result.ledger_debit_amount) == 0):
                legder_balnce = (legder_balnce) - int(veh_leg_result.ledger_credit_amount)
            elif(int(veh_leg_result.ledger_credit_amount) == 0):
                legder_balnce = (legder_balnce) + int(veh_leg_result.ledger_debit_amount)
            veh_leg_result.ledger_balance = legder_balnce
            db.session.flush()
            db.session.commit() 
            sum_veh_leg_val += int(veh_leg_result.ledger_credit_amount)
            sum_veh_cash_val += int(veh_leg_result.ledger_debit_amount)    
        get_vehicle_chart.networth = (sum_veh_leg_val) - sum_veh_cash_val
        get_vehicle.net_worth = (sum_veh_leg_val) - sum_veh_cash_val
        db.session.commit()
        
    def refresh_COA_Comm(userid):
        accnt_sub_type = AccountSubTypes.query.filter(AccountSubTypes.sub_type_name == "Commission Income").one()
        get_commission = ChartOfAccount.query.filter(and_(ChartOfAccount.accnt_name == str("commission").strip().lower(), ChartOfAccount.accnt_type  ==accnt_sub_type.id, ChartOfAccount.account_mode == 'commission',ChartOfAccount.userid == int(userid))).one()
        sum_comm_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == get_commission.id ,Ledger.ledger_type == "commission")).order_by(Ledger.id.asc()).all()
        sum_comm_leg_val = 0
        sum_comm_cash_val = 0
        legder_balnce = 0
        for comm_leg_result in sum_comm_leg:
            if(int(comm_leg_result.ledger_debit_amount) == 0):
                legder_balnce = (legder_balnce) + int(comm_leg_result.ledger_credit_amount)
            elif(int(comm_leg_result.ledger_credit_amount) == 0):
                legder_balnce = (legder_balnce) - int(comm_leg_result.ledger_debit_amount)
            comm_leg_result.ledger_balance = legder_balnce
            db.session.flush()
            db.session.commit() 
            sum_comm_leg_val += int(comm_leg_result.ledger_debit_amount)
            sum_comm_cash_val += int(comm_leg_result.ledger_credit_amount)     
        get_commission.networth = (sum_comm_cash_val) - sum_comm_leg_val
        db.session.commit()
        
    def refresh_COA_General(g_id):
        get_general_chart = ChartOfAccount.query.filter(ChartOfAccount.id == int(str(g_id))).one()
        sum_gen_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == get_general_chart.id,Ledger.ledger_type == "general")).order_by(Ledger.id.asc()).all()
        sum_gen_leg_val = 0
        sum_gen_cash_val = 0
        legder_balnce = 0
        for gen_leg_result in sum_gen_leg:
            if(int(gen_leg_result.ledger_debit_amount) == 0):
                legder_balnce = (legder_balnce) + int(gen_leg_result.ledger_credit_amount)
            elif(int(gen_leg_result.ledger_credit_amount) == 0):
                legder_balnce = (legder_balnce) - int(gen_leg_result.ledger_debit_amount)
            gen_leg_result.ledger_balance = legder_balnce
            db.session.flush()
            db.session.commit() 
            sum_gen_leg_val += int(gen_leg_result.ledger_debit_amount)
            sum_gen_cash_val += int(gen_leg_result.ledger_credit_amount)    
        get_general_chart.networth = -(sum_gen_leg_val) + sum_gen_cash_val
        db.session.commit()