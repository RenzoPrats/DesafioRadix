import { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";
import axios from "axios";
import "./Home.css";
import COLORS from "../../consts/colors";
import Select, { StylesConfig } from "react-select";
import { useAuth } from "../../context/Auth";

// Define a estrutura dos pontos de dados recebidos da API
interface DataPoint {
  equipment_id: string;
  avg_value: number;
}

const BASE_URL = "http://127.0.0.1:8000/aggregated-data?period="; // URL base para buscar dados agregados

function Home() {
  const { logout } = useAuth();
  const chartRef = useRef<HTMLCanvasElement | null>(null);
  const chartInstance = useRef<Chart | null>(null);
  const [period, setPeriod] = useState("24h");

  // Opções para seleção de período
  const periodOptions = [
    { value: "24h", label: "24 horas" },
    { value: "48h", label: "48 horas" },
    { value: "1w", label: "1 semana" },
    { value: "1m", label: "1 mês" },
  ];

  // Estilos personalizados para o componente Select
  const customStyles: StylesConfig = {
    control: (provided, state) => ({
      ...provided,
      borderColor: state.isFocused ? "#4bc0c0" : "#cccccc",
      boxShadow: state.isFocused ? "0 0 0 1px #4bc0c0" : provided.boxShadow,
      "&:hover": {
        borderColor: "#4bc0c0",
      },
    }),
    option: (provided, state) => ({
      ...provided,
      backgroundColor: state.isSelected ? "#4bc0c0" : "white",
      color: state.isSelected ? "white" : "#333",
      "&:hover": {
        backgroundColor: state.isSelected ? "#4bc0c0" : "#e6f7f7",
      },
    }),
  };

  useEffect(() => {
    // Função para buscar dados e atualizar o gráfico
    const fetchData = async () => {
      try {
        // Faz uma requisição para obter dados agregados com base no período selecionado
        const response = await axios.get<DataPoint[]>(`${BASE_URL}${period}`);
        const chartData = response.data;

        if (chartRef.current) {
          if (chartInstance.current) {
            chartInstance.current.destroy(); // Destrói o gráfico anterior, se existir
          }

          const ctx = chartRef.current.getContext("2d");
          if (ctx) {
            // Cria uma nova instância do gráfico
            chartInstance.current = new Chart(ctx, {
              type: "bar",
              data: {
                labels: chartData.map((item) => item.equipment_id),
                datasets: [
                  {
                    label: "Valor Médio",
                    data: chartData.map((item) => item.avg_value),
                    backgroundColor: COLORS,
                  },
                ],
              },
              options: {
                responsive: true,
                plugins: {
                  legend: {
                    position: "top",
                  },
                },
              },
            });
          }
        }
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      }
    };

    fetchData();

    // Função de limpeza para destruir o gráfico ao desmontar o componente
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [period]);

  // Função para lidar com a mudança do período selecionado
  const handlePeriodChange = (selectedOption: any) => {
    setPeriod(selectedOption.value);
  };

  return (
    <div className="div-main">
      <nav className="navbar">
        <div className="navbar-content">
          <h1 className="navbar-title">Valor médio dos sensores</h1>
          <button className="logout-button" onClick={logout}>
            Logout
          </button>
        </div>
      </nav>
      <div className="content">
        <div className="chart-controls">
          <p className="select-text">
            Selecione o período desejado para exibir no gráfico a média de
            valores de cada equipamento.
          </p>
          <Select
            value={periodOptions.find((option) => option.value === period)}
            onChange={handlePeriodChange}
            className="period-select"
            options={periodOptions}
            styles={customStyles}
          ></Select>
        </div>
        <div className="chart">
          <canvas ref={chartRef}></canvas>
        </div>
      </div>
    </div>
  );
}

export default Home;
