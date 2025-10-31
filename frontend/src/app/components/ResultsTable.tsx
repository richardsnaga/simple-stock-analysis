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
      // Convert to percentage string with 2 decimal places
      console.log('valuee',params)
      const value = Number(params) * 100;
      return `${value.toFixed(2)}%`;
    }
  },
        { field: 'historical_var', headerName: 'historical_var', width: 200 },
        { field: 'parametric_var', headerName: 'parametric_var', width: 200 },
        { field: 'price', headerName: 'price', width: 200 },
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
