"use client";

import { Typography, Grid, Paper } from "@mui/material";
import Layout from "./layout";

const Page = () => {
  return (
    <>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={2} style={{ border: "1px solid red" }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>Chart Area</Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>Recent Activities</Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>Data Table</Paper>
        </Grid>
      </Grid>
    </>
  );
};

export default Page;
