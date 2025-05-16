import datetime
from io import BytesIO
import textwrap
from flask import Blueprint
from flask import Flask, render_template, request, Response, send_file , redirect, session, url_for, jsonify
from chartofAccount import ChartOfAccount
from clients import Clients
from clnStkRtnItems import ClientReturnItems
from invoiceItems import InvoiceItems
from ledger import Ledger
from party import Party
from purchItems import PurchItems
from returnItems import ReturnItems
from supplier import Supplier
from tblProduct import TblProduct
from vehicles import Vehicles
from extensions import db
from sqlalchemy import and_, insert, text
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch, A4
from reportlab.lib import colors
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.colors import Color
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

api25 = Blueprint('api25', __name__)

@api25.route('/get_stk_details_data', methods=['POST']) 
def get_stk_dtls_report_index(): 
    data = request.get_json()
    start_date = (data['t_date_from'])
    end_date = (data['t_date_to'])
    userid = int(data['userid'])
    prd_data = []
    prod_list = TblProduct.query.filter(and_(TblProduct.userid == userid,TblProduct.datetime >= start_date, TblProduct.datetime <= end_date)).order_by(TblProduct.id.asc()).all()
    for prd in prod_list:
        big_qty = 0
        stk_out = 0
        inv_qty = 0
        ord_qty = 0
        stk_rtn = 0
        cl_stk_rtn = 0
        inv_items = InvoiceItems.query.filter(InvoiceItems.item_product == prd.id).all()
        for itm in inv_items:
            inv_qty = inv_qty + int(itm.item_qnty)
        ord_items = PurchItems.query.filter(PurchItems.item_product == prd.id).all()
        for o_itm in ord_items:
            ord_qty = ord_qty + int(o_itm.item_qnty)
        stk_rtn_items = ReturnItems.query.filter(ReturnItems.item_product == prd.id).all()
        for stk_itm in stk_rtn_items:
            stk_rtn = stk_rtn + int(stk_itm.item_qnty)
        cl_stk_rtn_items = ClientReturnItems.query.filter(ClientReturnItems.item_product == prd.id).all()
        for cl_stk_itm in cl_stk_rtn_items:
            cl_stk_rtn = cl_stk_rtn + int(cl_stk_itm.item_qnty)
        total_out = inv_qty + stk_rtn
        total_in = ord_qty + cl_stk_rtn
        stk_out = total_out
        big_qty = int(prd.product_stock) +  total_out
        prd_data.append({"id":prd.id,"prd_Name":prd.product_name ,"beg_Qty":big_qty,"in_qty":prd.product_stock,"pur_Amt":prd.product_whole_price,"out_qty":stk_out,"sale_Amt":prd.product_rental,"cls_qty":prd.product_stock})
    return jsonify(prd_data)

@api25.route('/get_all_party_report_data', methods=['POST']) 
def get_all_party_report_index(): 
    data = request.get_json()
    party_rp_data = []
    userid = int(data['userid'])
    coa_list = ChartOfAccount.query.filter(ChartOfAccount.userid == userid).all()
    for coa in coa_list:
        if(str(coa.account_mode).strip() == "commission"):
            leg_debit_val = 0
            leg_credit_val = 0
            sum_comm_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == coa.id ,Ledger.ledger_type == "commission")).all()
            for comm_leg_result in sum_comm_leg:
                leg_debit_val += int(comm_leg_result.ledger_debit_amount)
                leg_credit_val += int(comm_leg_result.ledger_credit_amount)
            party_rp_data.append({"id":coa.id,"name":coa.accnt_name ,"email":"N/A","phone":"N/A","debitAmt":leg_debit_val,"creditAmt":leg_credit_val,"acc_type":coa.account_mode})
        elif(str(coa.account_mode).strip() == "general"):
            leg_debit_val = 0
            leg_credit_val = 0
            sum_gen_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == coa.id ,Ledger.ledger_type == "general")).all()
            for gen_leg_result in sum_gen_leg:
                leg_debit_val += int(gen_leg_result.ledger_debit_amount)
                leg_credit_val += int(gen_leg_result.ledger_credit_amount)    
            party_rp_data.append({"id":coa.id,"name":coa.accnt_name ,"email":"N/A","phone":"N/A","debitAmt":leg_debit_val,"creditAmt":leg_credit_val,"acc_type":coa.account_mode})
        elif(str(coa.account_mode).strip() == "party"):
            get_party = Party.query.filter(Party.chart_accnt == int(coa.id)).one()
            leg_debit_val = 0
            leg_credit_val = 0
            sum_gen_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == coa.id ,Ledger.ledger_type == "party")).all()
            for gen_leg_result in sum_gen_leg:
                leg_debit_val += int(gen_leg_result.ledger_debit_amount)
                leg_credit_val += int(gen_leg_result.ledger_credit_amount)    
            party_rp_data.append({"id":get_party.id,"name":get_party.english_name ,"email":get_party.contact_person,"phone":get_party.phone_number,"debitAmt":leg_debit_val,"creditAmt":leg_credit_val,"acc_type":coa.account_mode})
        elif(str(coa.account_mode).strip() == "vehicle"):
            get_vehicle = Vehicles.query.filter(Vehicles.chart_accnt == int(coa.id)).one()
            leg_debit_val = 0
            leg_credit_val = 0
            sum_gen_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == coa.id ,Ledger.ledger_type == "vehicle")).all()
            for gen_leg_result in sum_gen_leg:
                leg_debit_val += int(gen_leg_result.ledger_debit_amount)
                leg_credit_val += int(gen_leg_result.ledger_credit_amount)    
            party_rp_data.append({"id":get_vehicle.id,"name":get_vehicle.vehicle_num ,"email":get_vehicle.driver_name,"phone":get_vehicle.phone_number,"debitAmt":leg_debit_val,"creditAmt":leg_credit_val,"acc_type":coa.account_mode})
        elif(str(coa.account_mode).strip() == "client"):
            get_client = Clients.query.filter(Clients.chart_accnt == int(coa.id)).one()
            leg_debit_val = 0
            leg_credit_val = 0
            sum_gen_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == coa.id ,Ledger.ledger_type == "client")).all()
            for gen_leg_result in sum_gen_leg:
                leg_debit_val += int(gen_leg_result.ledger_debit_amount)
                leg_credit_val += int(gen_leg_result.ledger_credit_amount)    
            party_rp_data.append({"id":get_client.id,"name":get_client.client_name ,"email":get_client.client_email,"phone":get_client.client_phone,"debitAmt":leg_debit_val,"creditAmt":leg_credit_val,"acc_type":coa.account_mode})
        elif(str(coa.account_mode).strip() == "supplier"):
            get_supplier = Supplier.query.filter(Supplier.chart_accnt == int(coa.id)).one()
            leg_debit_val = 0
            leg_credit_val = 0
            sum_gen_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == coa.id ,Ledger.ledger_type == "supplier")).all()
            for gen_leg_result in sum_gen_leg:
                leg_debit_val += int(gen_leg_result.ledger_debit_amount)
                leg_credit_val += int(gen_leg_result.ledger_credit_amount)    
            party_rp_data.append({"id":get_supplier.id,"name":get_supplier.suppl_name ,"email":get_supplier.suppl_email,"phone":get_supplier.suppl_phone,"debitAmt":leg_debit_val,"creditAmt":leg_credit_val,"acc_type":coa.account_mode})
    return jsonify(party_rp_data)


@api25.route('/get_goods_oils_data', methods=['POST']) 
def get_goods_oils_report_index(): 
    data = request.get_json()
    userid = int(data['userid'])
    party_rp_data = []
    coa_list = ChartOfAccount.query.filter(ChartOfAccount.userid == userid).all()
    for coa in coa_list:
        if(str(coa.account_mode).strip() == "party"):
            get_party = Party.query.filter(Party.chart_accnt == int(coa.id)).one()
            leg_debit_val = 0
            leg_credit_val = 0
            sum_gen_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == coa.id ,Ledger.ledger_type == "party")).all()
            for gen_leg_result in sum_gen_leg:
                leg_debit_val += int(gen_leg_result.ledger_debit_amount)
                leg_credit_val += int(gen_leg_result.ledger_credit_amount)    
            party_rp_data.append({"id":get_party.id,"name":get_party.english_name ,"email":get_party.contact_person,"phone":get_party.phone_number,"debitAmt":leg_debit_val,"creditAmt":leg_credit_val,"acc_type":coa.account_mode, "manifest_type":get_party.type})
        elif(str(coa.account_mode).strip() == "vehicle"):
            get_vehicle = Vehicles.query.filter(Vehicles.chart_accnt == int(coa.id)).one()
            leg_debit_val = 0
            leg_credit_val = 0
            sum_gen_leg = Ledger.query.filter(and_(Ledger.ledger_account_no == coa.id ,Ledger.ledger_type == "vehicle")).all()
            for gen_leg_result in sum_gen_leg:
                leg_debit_val += int(gen_leg_result.ledger_debit_amount)
                leg_credit_val += int(gen_leg_result.ledger_credit_amount)    
            party_rp_data.append({"id":get_vehicle.id,"name":get_vehicle.vehicle_num ,"email":get_vehicle.driver_name,"phone":get_vehicle.phone_number,"debitAmt":leg_debit_val,"creditAmt":leg_credit_val,"acc_type":coa.account_mode, "manifest_type":get_vehicle.veh_type})
    return jsonify(party_rp_data)
