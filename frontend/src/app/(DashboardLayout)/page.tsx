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
} from "@mui/material";
import Chart from "../components/Chart";

interface ApiResponse {
  date: string[];
  return_: number[];
  varHistorical: number;
  varParametric: number;
  analysisText: string;
}

const Page = () => {
  const [stock, setStock] = useState("");
  const [confidence, setConfidence] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<ApiResponse | null>(null);

  const handleGenerate = async () => {
    // if (!stock || !confidence)
    //   return alert("Please select stock and confidence level.");

    setLoading(true);
    setData(null);
    try {
      const res = await axios.get(`/api/returns/${stock}`);
      setData(res.data);
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
            <MenuItem value="TSLA">TSLA</MenuItem>
            <MenuItem value="MSFT">MSFT</MenuItem>
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 180 }}>
          <InputLabel>Confidence Level</InputLabel>
          <Select
            value={confidence}
            label="Confidence Level"
            onChange={(e) => setConfidence(e.target.value)}
          >
            <MenuItem value="90">90%</MenuItem>
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
          <Chart data={data} />

          <Typography variant="h6" sx={{ mt: 3 }}>
            Value at Risk (VaR) Results
          </Typography>
          {/* <ResultsTable
            results={[
              { type: "Historical VaR", value: data.varHistorical },
              { type: "Parametric VaR", value: data.varParametric },
            ]}
          /> */}

          <Typography variant="h6" sx={{ mt: 3 }}>
            Analysis
          </Typography>
          <Typography>{data.analysisText}</Typography>
        </Box>
      )}
    </Container>
  );
};

export default Page;
