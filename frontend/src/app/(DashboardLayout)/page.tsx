"use client";

import { useState } from "react";
import axios from "axios";
import {
  Box,
  Button,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  CircularProgress,
  Card,
  CardContent,
} from "@mui/material";
import Chart from "../components/Chart";
import ResultsTable from "../components/ResultsTable";

const Page = () => {
  const [stock, setStock] = useState("");
  const [confidence, setConfidence] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [dataVar, setDataVar] = useState([]);
  const [analysis, setAnalysis] = useState("")

  const handleGenerate = async () => {
    // if (!stock || !confidence)
    //   return alert("Please select stock and confidence level.");

    setLoading(true);
    setData(null);
    setAnalysis("");
    setDataVar([]);
    try {
      const res = await axios.get(`/api/returns/${stock}`);
      const resVar = await axios.get(`/api/var/${stock}`, { params: { 'level': confidence}});
      console.log('resvar',resVar)
      setData(res.data);
      setDataVar(resVar.data.data);
      setAnalysis(resVar.data.analysis)
    } catch (err) {
      console.error(err);
      alert("Failed to fetch data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Simple Stock Analysis
      </Typography>

      <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
        <FormControl sx={{ minWidth: 160 }}>
          <InputLabel>Stock</InputLabel>
          <Select
            value={stock}
            label="Stock"
            onChange={(e) => setStock(e.target.value)}
          >
            <MenuItem value="AAPL">AAPL</MenuItem>
            <MenuItem value="GOOGL">GOOGL</MenuItem>
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 180 }}>
          <InputLabel>Confidence Level</InputLabel>
          <Select
            value={confidence}
            label="Confidence Level"
            onChange={(e) => setConfidence(e.target.value)}
          >
            <MenuItem value="95">95%</MenuItem>
            <MenuItem value="99">99%</MenuItem>
          </Select>
        </FormControl>

        <Button variant="contained" onClick={handleGenerate} disabled={loading}>
          {loading ? <CircularProgress size={24} /> : "Generate"}
        </Button>
      </Box>

      {data && (
        <Box sx={{ mt: 4 }}>
          <Chart data={data} stock={stock} />

        <div  style={{marginTop: '30px'}}>
          <ResultsTable
            results={dataVar}
          /></div>

          <Card sx={{ mt: 3, boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Analysis
              </Typography>
              <Typography variant="body1">
                {analysis}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      )}
    </Container>
  );
};

export default Page;
