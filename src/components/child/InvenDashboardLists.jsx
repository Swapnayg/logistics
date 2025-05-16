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
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import moment from 'moment';



const InvenDashboardLists = () => {

 
  return (
    <div>

    this is all InvenDashboardLists report page
       
    </div>
  );
};

export default InvenDashboardLists;