"use client";
import React, { useState } from "react";
import { useEffect } from "react";
import Link from "next/link";
import $ from 'jquery'; 
import { Icon } from "@iconify/react/dist/iconify.js";
import { validate } from "uuid";
const loadJQueryAndDataTables = async () => {
  const $ = (await import("jquery")).default;
  await import("datatables.net-dt/js/dataTables.dataTables.js");
  return $;
};


const InwarehouseList = () => {

    const [inware_name, setinware_name] = useState("");
    const [in_ware_id, setId] = useState(0);
    const [in_ware_code, setwarecode] = useState("");
    const [in_ware_loctn, setin_ware_loctn] = useState("");
    const canSubmit = inware_name.length > 0 && in_ware_code.length > 0  && in_ware_loctn.length > 0;

  const handleSubmit = (e) => {
    e.preventDefault();
    if(canSubmit)
    {
      if($("#btcninwaresubmit").text().trim() == "Save")
      {
        fetch('http://35.154.229.254/add_inwarehouse_values', { 
          method: 'POST', 
          headers: {   'Accept': 'application/json',
            'Content-Type': 'application/json'  }, 
            body: JSON.stringify({userid:localStorage.getItem('id'), in_ware_name: inware_name, inware_code: in_ware_code, inware_location: in_ware_loctn})
          }).then(res => {
              return res.json();
          }).then(data => {
          if(parseInt(data) != 0)
          {
              refreshtable();
          }
        });
      }
      else if($("#btcninwaresubmit").text().trim() == "Update")
        {
            fetch('http://35.154.229.254/update_inwarehouse_setup', { 
              method: 'POST', 
              headers:{   'Accept': 'application/json',
                'Content-Type': 'application/json'  },
              body: JSON.stringify({userid:localStorage.getItem('id'),inw_id:in_ware_id,  in_ware_name: inware_name, inware_code: in_ware_code, inware_location: in_ware_loctn})
            }).then(res => {
              return res.json();
            }).then(data => {
              if(data.data == "updated")
              {
                $("#btcninwaresubmit").text("Save");
                refreshtable();
              }
          });
        }
    }
  }

  const handleReset = () => {
    setinware_name("");
    setwarecode("");
    setin_ware_loctn("");
    setId(0);
  };

  function refreshtable()
  {
    handleReset();
    if ( $.fn.DataTable.isDataTable('#inware_table') ) {
      $('#inware_table').DataTable().destroy();
    }
    $('#inware_table tbody').empty();
    fetch('http://35.154.229.254/inwarehouse_data'+'/'+localStorage.getItem('id')).then((res) =>
      res.json().then((jsdata) => {
       for (let i = 0; i < jsdata.length; i++) {
        let row = '<tr>';
        row += '<td>' + (i +1) + '</td>';
        row += '<td style="text-transform:capitalize">' + jsdata[i].ware_name + '</td>';
        row += '<td style="text-transform:capitalize" data-label='+jsdata[i].ware_code+'>' + jsdata[i].ware_code + '</td>';
        row += '<td style="text-transform:capitalize" data-label='+jsdata[i].ware_location+'>' + jsdata[i].ware_location + '</td>';
        row += '<td ><a class="inware_edit w-32-px h-32-px me-8 bg-success-focus text-success-main rounded-circle d-inline-flex align-items-center justify-content-center" data-lable='+jsdata[i].id+'><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--lucide" width="1em" height="1em" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"></path></g></svg></a><a class="inware_delete w-32-px h-32-px me-8 bg-danger-focus text-danger-main rounded-circle d-inline-flex align-items-center justify-content-center" data-lable='+jsdata[i].id+'><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--mingcute" width="1em" height="1em" viewBox="0 0 24 24"><g fill="none"><path d="m12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.018-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"></path><path fill="currentColor" d="M14.28 2a2 2 0 0 1 1.897 1.368L16.72 5H20a1 1 0 1 1 0 2l-.003.071l-.867 12.143A3 3 0 0 1 16.138 22H7.862a3 3 0 0 1-2.992-2.786L4.003 7.07L4 7a1 1 0 0 1 0-2h3.28l.543-1.632A2 2 0 0 1 9.721 2zm3.717 5H6.003l.862 12.071a1 1 0 0 0 .997.929h8.276a1 1 0 0 0 .997-.929zM10 10a1 1 0 0 1 .993.883L11 11v5a1 1 0 0 1-1.993.117L9 16v-5a1 1 0 0 1 1-1m4 0a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0v-5a1 1 0 0 1 1-1m.28-6H9.72l-.333 1h5.226z"></path></g></svg></a></td>';
        row += '</tr>';
        $("#inware_table tbody").append(row);
       }
       $("#inware_table").DataTable();
      }))
    
  }
  
  useEffect(() => {

  var username = localStorage.getItem('username');
  if (username) {
    let table; 
  loadJQueryAndDataTables()
      .then(($) => {
        window.$ = window.jQuery = $;
        fetch('http://35.154.229.254/inwarehouse_data'+'/'+localStorage.getItem('id')).then((res) =>
          res.json().then((jsdata) => {
           for (let i = 0; i < jsdata.length; i++) {
            let row = '<tr>';
            row += '<td>' + (i +1) + '</td>';
            row += '<td style="text-transform:capitalize">' + jsdata[i].ware_name + '</td>';
            row += '<td style="text-transform:capitalize" data-label='+jsdata[i].ware_code+'>' + jsdata[i].ware_code + '</td>';
            row += '<td style="text-transform:capitalize" data-label='+jsdata[i].ware_location+'>' + jsdata[i].ware_location + '</td>';
            row += '<td ><a class="inware_edit w-32-px h-32-px me-8 bg-success-focus text-success-main rounded-circle d-inline-flex align-items-center justify-content-center" data-lable='+jsdata[i].id+'><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--lucide" width="1em" height="1em" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"></path></g></svg></a><a class="inware_delete w-32-px h-32-px me-8 bg-danger-focus text-danger-main rounded-circle d-inline-flex align-items-center justify-content-center" data-lable='+jsdata[i].id+'><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--mingcute" width="1em" height="1em" viewBox="0 0 24 24"><g fill="none"><path d="m12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.018-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"></path><path fill="currentColor" d="M14.28 2a2 2 0 0 1 1.897 1.368L16.72 5H20a1 1 0 1 1 0 2l-.003.071l-.867 12.143A3 3 0 0 1 16.138 22H7.862a3 3 0 0 1-2.992-2.786L4.003 7.07L4 7a1 1 0 0 1 0-2h3.28l.543-1.632A2 2 0 0 1 9.721 2zm3.717 5H6.003l.862 12.071a1 1 0 0 0 .997.929h8.276a1 1 0 0 0 .997-.929zM10 10a1 1 0 0 1 .993.883L11 11v5a1 1 0 0 1-1.993.117L9 16v-5a1 1 0 0 1 1-1m4 0a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0v-5a1 1 0 0 1 1-1m.28-6H9.72l-.333 1h5.226z"></path></g></svg></a></td>';
            row += '</tr>';
            $("#inware_table tbody").append(row);
           }
           $("#inware_table").DataTable();
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
  }, []);

  
  $(document).on("click", '.inware_edit', function(e){
    e.preventDefault();
    var row_id = $(this).attr("data-lable");
    $("#btcninwaresubmit").text("Update");
    var t_row =  $(this).closest('tr').index();
    var inware_name = $("#inware_table tbody tr:eq("+t_row+") td:eq(1)").html();
    var in_ware_code = $("#inware_table tbody tr:eq("+t_row+") td:eq(2)").attr("data-label");
    var in_ware_location = $("#inware_table tbody tr:eq("+t_row+") td:eq(3)").attr("data-label");
    $("#edit_id").val(row_id);
    setId(row_id);
    setinware_name(inware_name.toString().trim());
    setwarecode(in_ware_code.toString().trim());
    setin_ware_loctn(in_ware_location.toString().trim());
  });

  $(document).off('click', '.inware_delete').on("click", '.inware_delete', function(e){
      e.preventDefault();
      var row_id = $(this).attr("data-lable");
    fetch('http://35.154.229.254/inwarehouse_delete/'+row_id+'/'+localStorage.getItem('id'), { 
      method: 'DELETE', 
      headers:{   'Accept': 'application/json',
                'Content-Type': 'application/json'  }, 
      body: JSON.stringify()
    }).then(res => {
      return res.json();
    }).then(data => {
      if(data.data == "deleted")
      {
        refreshtable();
      }
  });
  });
  
  return (
    <div>
    <div className="col-lg-12">
      <div className="card">
        <div className="card-header">
          <h5 className="card-title mb-0">Add In-Warehouse</h5>
        </div>
        <div className="card-body">
          <form className="row gy-3 needs-validation" noValidate onSubmit={e => e.preventDefault()}>
            {/* Party Name */}
            <div className="col-md-3">
              <label className="form-label">Warehouse Name *</label>
              

              <input
                type="text"
                className="form-control"
                value={inware_name}
                onChange={(e) => setinware_name(e.target.value)}
                onKeyPress={(e)=>{e.target.keyCode === 13 && e.preventDefault();}}
                required
              />
            </div>

            {/* province */}
            <div className="col-md-3">
              <label className="form-label">Warehouse Code *</label>
             
              <input
                type="text"
                className="form-control"
                value={in_ware_code}
                onChange={(e) => setwarecode(e.target.value)}
                onKeyPress={(e)=>{e.target.keyCode === 13 && e.preventDefault();}}
                required
              />
            </div>

            <div className="col-md-3">
              <label className="form-label">Warehouse Location *</label>
              

              <input
                type="text"
                className="form-control"
                value={in_ware_loctn}
                onChange={(e) => setin_ware_loctn(e.target.value)}
                onKeyPress={(e)=>{e.target.keyCode === 13 && e.preventDefault();}}
                required
              />
            </div>

            {/* Action Buttons */}
            <div className="col-12 mt-3 d-flex gap-2">
              <button className="btn btn-primary" id="btcninwaresubmit" onClick={handleSubmit} disabled={!canSubmit} >
                <Icon icon="mdi:content-save" className="me-1" /> Save
              </button>
              <button
                className="btn btn-secondary"
                province="button"
                onClick={handleReset}
              >
                <Icon icon="mdi:refresh" className="me-1" /> Reset
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div className="card basic-data-table">
      <div className="card-header">
        <h5 className="card-title mb-0">Warehouses List</h5>
      </div>
      <div className="card-body">
        <table
          className="table bordered-table mb-0"
          id="inware_table"
          data-page-length={10}
        >
          <thead>
            <tr>
              <th scope="col">Sno</th>
              <th scope="col">Warehouse Name</th>
              <th scope="col">Warehouse Code</th>
              <th scope="col">Warehouse Location</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            {/* Sample Data Rows */}

            {/* Add more sample rows as needed */}
          </tbody>
        </table>
      </div>
    </div>
    </div>
  );
};

export default InwarehouseList;