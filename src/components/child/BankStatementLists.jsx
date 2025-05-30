"use client";
import React, { useState } from "react";
import { useEffect } from "react";
import Link from "next/link";
import $ from 'jquery'; 
import { Icon } from "@iconify/react/dist/iconify.js";
import { validate } from "uuid";
import moment from 'moment';
const loadJQueryAndDataTables = async () => {
  const $ = (await import("jquery")).default;
  await import("datatables.net-dt/js/dataTables.dataTables.js");
  return $;
};
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const BankStatementLists = () => {

  var date = new Date();
  const [taxPayable, settaxPayable] = useState(0);
  const [taxReceivable, settaxReceivable] = useState(0);
  const [totalNetProfit, settotalNetProfit] = useState(0);
  const [startDate, setStartDate] = useState(new Date(date.getFullYear(), date.getMonth(), 1));
  const [endDate, setEndDate] = useState(new Date(date.getFullYear(), date.getMonth() + 1, 0));
  const [totalBalance, settotalBalance] = useState(0);

  function handleStDateChange(date)
  {
    setStartDate(date);
    refreshtable(date,endDate);
  }

  function handleEndDateChange(date)
  {
    setEndDate(date);
    refreshtable(startDate,date);
  }

  const handlePrint = (e) => {
    const st_Date = new Date(startDate);
    const en_Date = new Date(endDate);
    var cust_Name = "Bank Statement Report";
    var f_st_date = moment(startDate).format("D MMMM YYYY");
    var f_en_date = moment(endDate).format("D MMMM YYYY");
    fetch('http://35.154.229.254/generateBankStaReport_pdf', { 
      method: 'POST', 
      headers: {   'Accept': 'application/json',
        'Content-Type': 'application/json'  }, 
        body: JSON.stringify({userid:localStorage.getItem('id'), startDate: addDays(st_Date, 1), endDate: addDays(en_Date, 1), f_st_date:f_st_date, f_en_date:f_en_date,cust_Name:cust_Name})
      })
    .then(resp => resp.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'Bank_Statement_Report.pdf';
      document.body.appendChild(a);
      a.click();
    })
    .catch(() => 
    console.log("error"));
  };

  const handleExport = (e) => {
    e.preventDefault();  
    let data = "";
    const tableData = [];
    const rows = document.querySelectorAll("#bank_div table tr");
    for (const row of rows) {
      const rowData = [];
      for (const [index, column] of row.querySelectorAll("th, td").entries()) {
            // To retain the commas in the "Description" column, we can enclose those fields in quotation marks.
        if ((index + 1) % 3 === 0) {
          rowData.push('"' + column.innerText + '"');
        } else {
          rowData.push(column.innerText);
      }
    }
    tableData.push(rowData.join(","));
    }
    data += tableData.join("\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([data], { type: "text/csv" }));
    a.setAttribute("download", "Bank_Statement_Report.csv");
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  function addDays(date, days) {
    const dateCopy = new Date(date);
    dateCopy.setDate(date.getDate() + days);
    return dateCopy;
  }  

  function refreshtable(st_date,en_date)
  {
    const st_Date = new Date(st_date);
    const en_Date = new Date(en_date);

    if ( $.fn.DataTable.isDataTable('#tbl_sale_rpt') ) {
      $('#tbl_sale_rpt').DataTable().destroy();
    }
    $('#tbl_sale_rpt tbody').empty();
    fetch("http://35.154.229.254/get_bank_stat_report_data", { 
      method: 'POST', 
      headers: {   'Accept': 'application/json',
        'Content-Type': 'application/json'  }, 
        body: JSON.stringify({ userid:localStorage.getItem('id'), t_date_from: addDays(st_Date, 1), t_date_to: addDays(en_Date, 1)})
      }).then((res)  =>
      res.json().then((jsdata) => {
        let bal_amount = 0;
           for (let i = 0; i < jsdata.length; i++) {
            let row = '<tr>';
            row += '<td>' + (i +1) + '</td>';
            row += '<td style="text-transform:capitalize">' + moment(jsdata[i].date).format("DD/MM/YYYY")+ '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].accntName + '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].description + '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].debitAmt+ '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].creditAmt + '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].balAmt + '</td>';
            row += '</tr>';
            $("#tbl_sale_rpt tbody").append(row);
            bal_amount +=  parseFloat(jsdata[i].balAmt);
           }
           $("#tbl_sale_rpt").DataTable();
           settotalBalance("Rs. " + bal_amount);
    }));
  }

  useEffect(()=>{
  var username = localStorage.getItem('username');
  if (username) {
    let table;
    loadJQueryAndDataTables()
      .then(($) => {
        window.$ = window.jQuery = $;
        const st_Date = new Date(startDate);
        const en_Date = new Date(endDate);
        fetch("http://35.154.229.254/get_bank_stat_report_data", { 
          method: 'POST', 
          headers: {   'Accept': 'application/json',
            'Content-Type': 'application/json'  }, 
            body: JSON.stringify({ userid:localStorage.getItem('id'), t_date_from: addDays(st_Date, 1), t_date_to: addDays(en_Date, 1)})
          }).then((res)  =>
          res.json().then((jsdata) => {
            let bal_amount = 0;
           for (let i = 0; i < jsdata.length; i++) {
            let row = '<tr>';
            row += '<td>' + (i +1) + '</td>';
            row += '<td style="text-transform:capitalize">' + moment(jsdata[i].date).format("DD/MM/YYYY")+ '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].accntName + '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].description + '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].debitAmt+ '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].creditAmt + '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].balAmt + '</td>';
            row += '</tr>';
            bal_amount +=  parseFloat(jsdata[i].balAmt);
            $("#tbl_sale_rpt tbody").append(row);
           }
           $("#tbl_sale_rpt").DataTable();
           settotalBalance("Rs. " + bal_amount);
          }))
       
      })
      .catch((error) => {
        console.error("Error loading jQuery or DataTables:", error);
      });

    return () => {
      if (table) table.destroy(true);
    };
  }
  else
  {
    window.location.href = '/login';
  } 
},[]);

  
  return (
    <div className="col-lg-12">
      <div className="card">
        <div className="card-header">
          <h5 className="card-title mb-0">Bank Statement</h5>
        </div>
        <div className="card-body">
           <table className="table table-nowrap align-middle table-hover table-centered mb-0">
            <thead className="table-light">
              <tr>
                <td>From :</td>
                <td>
                  <DatePicker selected={startDate} onChange={handleStDateChange} placeholderText="Start Date"/>
                </td>
                  <td>To :</td>
                    <td>      
                    <DatePicker selected={endDate} onChange={handleEndDateChange} placeholderText="End Date"/>
                </td>
                <td> 
                
                </td>
                <th style={{textAlign:"right"}}>
                <button className="btn btn-outline-secondary btn-sm me-2" onClick={handlePrint}>
                <Icon icon="mdi:printer" className="me-1" /> Print
              </button>
                <button className="btn btn-outline-primary btn-sm" onClick={handleExport}>
                <Icon icon="mdi:download" className="me-1" /> Export
              </button>
                </th>
              </tr>
            </thead>
          </table>
        <div className="profit_loss_side sidebar-menu-area" id="bank_div">
        <table
          className="table bordered-table mb-0"
          id="tbl_sale_rpt"
          data-page-length={10}
        >
          <thead>
            <tr>
              <th scope="col">Sno</th>
              <th scope="col">Date</th>
              <th scope="col">Name</th>
              <th scope="col">Description</th>
              <th scope="col">Withdrawal Amount</th>
              <th scope="col">Deposit Amount</th>
              <th scope="col">Balance</th>
            </tr>
          </thead>
          <tbody>
            {/* Sample Data Rows */}

            {/* Add more sample rows as needed */}
          </tbody>
        </table>
        <table className="table table-nowrap align-middle table-hover table-centered mb-0 mt-5" style={{tableLayout:"fixed", textAlign:"right"}}>
            <thead className="table-light">
            <tr>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>Balance :</td>
                <td>{totalBalance}</td>
              </tr>
            </thead>
          </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BankStatementLists;