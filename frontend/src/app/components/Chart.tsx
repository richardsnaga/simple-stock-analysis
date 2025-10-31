"use client";

import { Card, CardContent, CardHeader } from "@mui/material";
import dynamic from "next/dynamic";
import React from "react";
const ReactApexChart = dynamic(() => import("react-apexcharts"), {
  ssr: false,
});

interface ChartProps {
  // dates: string[];
  // returns: number[];
  data: any;
}

const Chart: React.FC<ChartProps> = ({ data }) => {
  const dataChart = data.data;
  console.log(
    "data >>",
    dataChart.map((item: any) => item["date"])
  );

  const options: ApexCharts.ApexOptions = {
    chart: {
      type: "line",
      toolbar: {
        autoSelected: "zoom",
      },
      zoom: {
        type: "x",
        enabled: true,
        autoScaleYaxis: true,
      },
    },
    xaxis: {
      categories: dataChart.map((item: any) => item["date"]),
      title: { text: "Date" },
      type: "datetime",
    },
    yaxis: {
      title: { text: "Return (%)" },
      labels: {
        formatter: function (val) {
          return val + "%";
        },
      },
    },
  };

  const series = [
    {
      name: "Daily Return",
      data: dataChart.map((item: any) => +(item["return_"] * 100).toFixed(2)),
    },
  ];

  return (
    <>
      <Card>
        <CardHeader title="Historical Return" />
        <CardContent>
          <ReactApexChart
            options={options}
            series={series}
            type="line"
            height={350}
          />
        </CardContent>
      </Card>
    </>
  );
};

export default Chart;
