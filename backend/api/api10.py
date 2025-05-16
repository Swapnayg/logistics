import datetime
from flask import Blueprint
from flask import Flask, render_template, request, Response, send_file , redirect, session, url_for, jsonify
from accountSubTypes import AccountSubTypes
from accountTypes import AccountTypes
from chartofAccount import ChartOfAccount
from citysetup import CitySetup
from inwarehouse import InvWarehouses
from ledger import Ledger
from ledger2 import Ledger2
from modeofpayment import ModeOfPayment
from party import Party
from tblInvoice import TblInvoice
from tblOrder import TblOrder
from units import Units
from users import Users
from extensions import db
from sqlalchemy import and_, extract, insert, text
from api.refreshcoacustomer import RefreshCOA_Customer

api10 = Blueprint('api10', __name__)

def sum_array(arr):
    total = sum(arr)
    return total

def percent_change(old, new):
    ad = abs(new - old )
    avg = (old + new) / 2
    try:
        pro_diff = ad / avg
        per_diff = pro_diff * 100
    except:
        pro_diff = 0
        per_diff = 0
    return round(per_diff,2)

@api10.route('/sales_dashboard_data/<userid>', methods=['GET']) 
def sales_dashboard_index(userid): 
    trans_data = []
    current_month = datetime.datetime.now().month
    now = datetime.datetime.now()
    last_month = now.month-1 if now.month > 1 else 12
    cm_gross_total = 0
    lm_gross_total = 0
    cm_gross_purch_val = 0
    lm_gross_purch_val = 0
    cm_income_gen = 0
    lm_income_gen = 0
    cm_gross_sell = db.session.query(TblInvoice).filter(and_(extract('month', TblInvoice.datetime)==current_month), TblInvoice.userid == userid).all()
    lm_gross_sell = db.session.query(TblInvoice).filter(and_(extract('month', TblInvoice.datetime)==last_month),TblInvoice.userid == userid).all()
    cm_gross_purch = db.session.query(TblOrder).filter(and_(extract('month', TblOrder.datetime)==current_month), TblOrder.userid == userid).all()
    lm_gross_purch = db.session.query(TblOrder).filter(and_(extract('month', TblOrder.datetime)==last_month), TblOrder.userid == userid).all()
    for sell in cm_gross_sell:
        cm_gross_total += float(sell.grand_total)
    for lsell in lm_gross_sell:
        lm_gross_total += float(lsell.grand_total)
    for purch in cm_gross_purch:
        cm_gross_purch_val += float(purch.grand_total)
    for lpurch in lm_gross_purch:
        lm_gross_purch_val += float(lpurch.grand_total)
    cm_income_gen = cm_gross_total - cm_gross_purch_val
    lm_income_gen = lm_gross_total - lm_gross_purch_val
    perc_gross_sale = percent_change(lm_gross_total,cm_gross_total)
    gross_sale_status = ""
    if(int(cm_gross_total) > int(lm_gross_total)):
        gross_sale_status = "high"
    else:
        gross_sale_status = "low"
    perc_gross_purch = percent_change(lm_gross_purch_val,cm_gross_purch_val)
    gross_purch_status = ""
    if(int(cm_gross_purch_val) > int(lm_gross_purch_val)):
        gross_purch_status = "high"
    else:
        gross_purch_status = "low"

    perc_gross_income = percent_change(lm_income_gen,cm_income_gen)
    gross_income_status = ""
    if(int(cm_income_gen) > int(lm_income_gen)):
        gross_income_status = "high"
    else:
        gross_income_status = "low"
    chart_of_suppl_txt = text("SELECT id,accnt_name,networth, MAX(networth) FROM public.chart_of_accounts Where userid = "+str(userid)+" AND account_mode = 'supplier' GROUP BY id limit 10;") 
    chart_of_suppl = db.session.execute(chart_of_suppl_txt)
    chart_suppl_data = []
    for chart_suppl in chart_of_suppl:
        chart_suppl_data.append({"supplId":chart_suppl.id,"supplName":chart_suppl.accnt_name,"supplNetworth":chart_suppl.networth  })
    chart_of_client_txt = text("SELECT id,accnt_name,networth, MAX(networth) FROM public.chart_of_accounts Where userid = "+str(userid)+" AND account_mode = 'client' GROUP BY id limit 10;") 
    chart_of_client = db.session.execute(chart_of_client_txt)
    chart_client_data = []
    for chart_client in chart_of_client:
        chart_client_data.append({"clientId":chart_client.id,"clientName":chart_client.accnt_name,"clientNetworth":chart_client.networth  })
   
    stk_details_txt = text(" SELECT id, product_name,min(product_stock) as min_stk, product_stock FROM tbl_product Where userid = "+str(userid)+" GROUP BY id limit 10;") 
    stk_details = db.session.execute(stk_details_txt)
    stk_details_data = []
    for stk_dtls in stk_details:
        stk_details_data.append({"stkId":stk_dtls.id,"stkName":stk_dtls.product_name,"stkQty":stk_dtls.min_stk  })
    ledger_data_txt = text("SELECT * FROM ledger2 WHERE userid = "+str(userid)+" AND ledger_credit_amount != '0' AND (ledger_bill LIKE 'INV_%' OR ledger_bill LIKE 'ORD_%') limit 10;") 
    ledger_data = db.session.execute(ledger_data_txt)
    for ledg_i in ledger_data:
        total_bal = 0
        if "INV_" in str(ledg_i.ledger_bill).strip():
            try:
                inv_data = TblInvoice.query.filter(TblInvoice.invoice_num == str(ledg_i.ledger_bill).strip()).one()
                total_bal = inv_data.grand_total
            except:  
                print("not found")
        elif "ORD_" in str(ledg_i.ledger_bill).strip():
            try:
                ord_data = TblOrder.query.filter(TblOrder.order_num == str(ledg_i.ledger_bill).strip()).one()
                total_bal = ord_data.grand_total
            except:  
                print("not found")
        trans_data.append({"id":ledg_i.id,"ledg_date":ledg_i.datetime,"ledg_invoice":ledg_i.ledger_bill,"ledg_method":ledg_i.ledger_method,"ledg_paid":ledg_i.ledger_credit_amount,"ledg_balance":ledg_i.ledger_balance, "total_bal":total_bal})
        
    wk_sale_data = []
    invoice_data_txt = text("SELECT datetime,EXTRACT('dow' FROM datetime) as days, sum(CAST(grand_total AS DECIMAL(10,2))) as sum_val FROM tbl_invoice WHERE userid = "+str(userid)+" AND datetime >= current_date - interval '7 days' group by datetime order by days;") 
    invoice_data = db.session.execute(invoice_data_txt)
    order_data_txt = text("SELECT datetime,EXTRACT('dow' FROM datetime) as days, sum(CAST(grand_total AS DECIMAL(10,2))) as sum_val FROM tbl_order WHERE userid = "+str(userid)+" AND datetime >= current_date - interval '7 days' group by datetime order by days;") 
    order_data = db.session.execute(order_data_txt)
    wk_purchase_data = [0] * 7
    wk_sale_data = [0] * 7
    wk_income_data = []
    for ord in order_data:
        wk_purchase_data[int(ord.days)] = round(float(ord.sum_val))
    for inv in invoice_data:
        wk_sale_data[int(inv.days)] = round(float(inv.sum_val))
    for index, sale in enumerate(wk_sale_data):
        income_val = sale - wk_purchase_data[index]
        wk_income_data.append(income_val)
    return jsonify({"ledger_data": trans_data , "chartOfSuppl": chart_suppl_data ,"stk_details_data":stk_details_data,"chartOfClient": chart_client_data, "cm_gross_total":round(cm_gross_total,2),"perc_gross_sale":round(perc_gross_sale,2),"gross_sale_status":gross_sale_status,"cm_gross_purch_val":round(cm_gross_purch_val,2),"perc_gross_purch":round(perc_gross_purch,2),"gross_purch_status":gross_purch_status,"cm_income_gen":round(cm_income_gen,2),"perc_gross_income": round(perc_gross_income,2), "gross_income_status":gross_income_status,"wk_income_data":wk_income_data,"wk_purchase_data":wk_purchase_data, "total_pur":sum_array(wk_purchase_data), "total_sales":sum_array(wk_income_data)})


@api10.route('/add_inwarehouse_values', methods=['POST']) 
def inwarehouse_create(): 
    data = request.get_json()
    userid = int(data['userid'])
    sadd_inware = insert(InvWarehouses).values(ware_name=data['in_ware_name'], ware_code=data['inware_code'], ware_location = data['inware_location'], userid = userid)
    inware_result = db.session.execute(sadd_inware)
    db.session.commit()
    return jsonify({"data":inware_result.inserted_primary_key[0]})

@api10.route('/add_acconttype_values', methods=['POST']) 
def accntType_create(): 
    data = request.get_json()
    userid = int(data['userid'])
    get_user = Users.query.get(int(userid))
    sadd_account_type = insert(AccountTypes).values(type_name=data['a_accnt_name'], type_status=data['a_accnt_status'], userid = userid, username= get_user.user_role)
    accnt_type_result = db.session.execute(sadd_account_type)
    db.session.commit()
    return jsonify({"data":accnt_type_result.inserted_primary_key[0]})

@api10.route('/add_sub_acconttype_values', methods=['POST']) 
def sub_accntType_create(): 
    data = request.get_json()
    userid = int(data['userid'])
    get_user = Users.query.get(int(userid))
    sadd_sub_account_type = insert(AccountSubTypes).values(type_name_id=data['a_accnt_name'],sub_type_name=data['a_sub_accnt_name'], type_status=data['a_accnt_status'], userid = userid, username= get_user.user_role)
    sub_accnt_type_result = db.session.execute(sadd_sub_account_type)
    db.session.commit()
    return jsonify({"data":sub_accnt_type_result.inserted_primary_key[0]})

@api10.route('/add_cashbook_values', methods=['POST']) 
def ledger_cash_add_create(): 
    data = request.get_json()
    userid = int(data['userid'])
    ledger_balance = 0
    get_chart_accnt = ChartOfAccount.query.filter(ChartOfAccount.id == int(str(data['ac_sel_id']))).one()
    if(data['ac_acc_Type'] == "in"):
        ledger_balance = int(get_chart_accnt.networth) + int(str(data['ac_amount']))
    elif(data['ac_acc_Type'] == "out"):
        ledger_balance = int(get_chart_accnt.networth) - int(str(data['ac_amount']))
    if(data['ac_party_type'] == "party" or data['ac_party_type'] == "vehicle" or data['ac_party_type'] == "general" or data['ac_party_type'] == "commission"):
        sadd_ledger_cash = insert(Ledger).values(ledger_account_no=data['ac_sel_id'],ledger_party_name=data['ac_sel_party'], ledger_gen_date=data['ac_cashbookDate'],ledger_debit_amount=data['ac_debit_amt'], ledger_credit_amount=data['ac_credit_amt'], ledger_bill=data['leg_inv_num'],ledger_method=data['ac_acc_Method'], ledger_balance=ledger_balance,ledger_bill_no=data['ac_bill_no'],ledger_type=data['ac_party_type'],ledger_descp=data['ac_description'], userid = userid)
        sub_ledger_cash_result = db.session.execute(sadd_ledger_cash)
        db.session.commit()
    elif(data['ac_party_type'] == "supplier" or data['ac_party_type'] == "client" ):
        sadd_ledger_custom = insert(Ledger2).values(ledger_account_no=data['ac_sel_id'],ledger_party_name=data['ac_sel_party'], ledger_gen_date=data['ac_cashbookDate'],ledger_debit_amount=data['ac_debit_amt'], ledger_credit_amount=data['ac_credit_amt'], ledger_bill=data['leg_inv_num'],ledger_method=data['ac_acc_Method'], ledger_balance=ledger_balance,ledger_bill_no=data['ac_bill_no'],ledger_type=data['ac_party_type'],ledger_descp=data['ac_description'], userid = userid)
        sub_ledger_cash_result = db.session.execute(sadd_ledger_custom)
        db.session.commit()
    if(data['ac_party_type'] == "party"):
        RefreshCOA_Customer.refresh_COA_Party(str(data['ac_sel_id']))
    elif(data['ac_party_type'] == "vehicle"):
        RefreshCOA_Customer.refresh_COA_Vehicle(str(data['ac_sel_id']))
    elif(data['ac_party_type'] == "general"):
        RefreshCOA_Customer.refresh_COA_General(str(data['ac_sel_id']))
    elif(data['ac_party_type'] == "commission"):
        RefreshCOA_Customer.refresh_COA_Comm(userid)
    elif(data['ac_party_type'] == "client"):
        RefreshCOA_Customer.refresh_COA_Customer(str(get_chart_accnt.id))
    elif(data['ac_party_type'] == "supplier"):
        RefreshCOA_Customer.refresh_COA_Supplier(str(get_chart_accnt.id))
    return jsonify({"data":sub_ledger_cash_result.inserted_primary_key[0]})


@api10.route('/add_chart_of_account_values', methods=['POST']) 
def add_chart_of_accnt_create(): 
    data = request.get_json()
    userid = int(data['userid'])
    get_chart_details =  ChartOfAccount.query.filter(and_(ChartOfAccount.accnt_name == str(data['a_acctName']).strip().lower(), ChartOfAccount.accnt_type  == str(data['a_accttype']).strip().lower(), ChartOfAccount.account_mode == 'general',ChartOfAccount.userid == userid )).all()
    if(len(get_chart_details) == 0):
        sadd_chart_of_accnt = insert(ChartOfAccount).values(accnt_name=str(data['a_acctName']).strip().lower(),accnt_code=data['a_acctcode'], accnt_type=str(data['a_accttype']).strip().lower(), accnt_status=data['a_acctstatus'], accnt_description=data['a_acctdescp'], account_mode = 'general', userid = userid)
        sub_chart_of_accnt_result = db.session.execute(sadd_chart_of_accnt)
        db.session.commit()
        return jsonify({"data":sub_chart_of_accnt_result.inserted_primary_key[0]})
    else:
        return jsonify({"data":"exits"})


@api10.route('/update_party', methods=['POST']) 
def party_update(): 
    data = request.get_json()
    userid = int(data['userid'])
    value = Party.query.filter(Party.id == int(data['party_id'])).first()
    get_party_chart = ChartOfAccount.query.filter(ChartOfAccount.id == int(str(value.chart_accnt))).one()
    get_party_chart.accnt_name = str(data['party']).strip().lower()
    value.english_name = str(data['party']).strip().lower()
    value.type = str(data['p_type'])
    value.contact_person = str(data['p_contactPerson'])
    value.phone_number = str(data['p_phoneNo'])
    db.session.flush()
    db.session.commit()
    return jsonify({"data":"updated"})

@api10.route('/update_city_setup', methods=['POST']) 
def city_set_update(): 
    data = request.get_json()
    userid = int(data['userid'])
    city_value = CitySetup.query.filter(CitySetup.id == int(data['city_id'])).first()
    city_value.city_name_e = str(data['city_name'])
    city_value.city_prov = str(data['c_province'])
    db.session.flush()
    db.session.commit()
    return jsonify({"data":"updated"})

@api10.route('/update_mode_of_pay', methods=['POST']) 
def mode_of_pay_update(): 
    data = request.get_json()
    userid = int(data['userid'])
    mode_pay_value = ModeOfPayment.query.filter(ModeOfPayment.id == int(data['mode_id'])).first()
    mode_pay_value.pay_name = str(data['mode_name'])
    mode_pay_value.pay_status = str(data['mode_status'])
    mode_pay_value.exlc_in_cash = str(data['mode_pay_exclude'])
    db.session.flush()
    db.session.commit()
    return jsonify({"data":"updated"})

@api10.route('/update_unit_setup', methods=['POST']) 
def unit_set_update(): 
    data = request.get_json()
    userid = int(data['userid'])
    unit_value = Units.query.filter(Units.id == int(data['u_id'])).first()
    unit_value.units_name = str(data['unit_name'])
    unit_value.units_status = str(data['u_status'])
    db.session.flush()
    db.session.commit()
    return jsonify({"data":"updated"})
