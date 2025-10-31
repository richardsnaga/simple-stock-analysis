"use client";

import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, Card, CardHeader, CardContent } from "@mui/material";
import { GridColDef } from "@mui/x-data-grid";
import { DataGrid } from "@mui/x-data-grid";
import React from "react";

interface ResultsTableProps {
  results: any[];
}

const ResultsTable = ({ results }: ResultsTableProps) => {
    console.log("results >>",results)
    const rowsWithId = results.map((row, index) => ({ id: index, ...row }));
    const columns: GridColDef[] = [
        { field: 'date', headerName: 'Date', width: 200 },
        { 
            field: 'daily_return', 
            headerName: 'Daily Return', 
            width: 200,
            valueFormatter: (params:any) => {
            const value = Number(params) * 100;
            return `${value.toFixed(2)}%`;
            }
        },
        { 
            field: 'historical_var', 
            headerName: 'Historical Var', 
            width: 200,
            valueFormatter: (params:any) => {
            const value = Number(params) * 100;
            return `${value.toFixed(2)}%`;
            }
        },
        { 
            field: 'parametric_var', 
            headerName: 'Parametic Var', 
            width: 200,
            valueFormatter: (params:any) => {
            const value = Number(params) * 100;
            return `${value.toFixed(2)}%`;
            }
        },
        { 
            field: 'price', 
            headerName: 'Price (USD)', 
            width: 200,
            valueFormatter: (params) => {
            if (params == null) return '-';
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2, // tampilkan 2 angka desimal
            }).format(Number(params));
            }
        },
    ];
  
  return (
    <>
    <Card>
       <CardHeader title={"Value at Risk (VaR) Results"} />
        <CardContent>
     <Box sx={{ height: 400, width: 1 }}>
      <DataGrid
        rows={rowsWithId}
        disableColumnFilter
        disableColumnSelector
        disableDensitySelector
        columns={columns}
        showToolbar
      />
    </Box>
    </CardContent>
    </Card>
    </>
  );
};

export default ResultsTable;
