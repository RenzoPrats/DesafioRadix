import { createContext, useState, useContext, useEffect } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

// Cria um contexto de autenticação com valores padrão
const AuthContext = createContext<{
  user: any | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
}>({
  user: null,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
});

const BASE_URL = "http://localhost:8000"; // URL base para as requisições à API

// Hook personalizado para acessar o contexto de autenticação
export function useAuth() {
  return useContext(AuthContext);
}

// Provedor de autenticação que gerencia o estado de autenticação
export const AuthProvider = ({ children }: any) => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verifica se há um usuário armazenado localmente
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const parsedUser = JSON.parse(storedUser);
      if (isTokenValid(parsedUser.token)) {
        setUser(parsedUser); // Define o usuário autenticado
      } else {
        localStorage.removeItem("user"); // Remove o usuário se o token for inválido
      }
    }
    setLoading(false); // Define o carregamento como concluído
  }, []);

  // Função para verificar a validade do token
  const isTokenValid = (token: string): boolean => {
    try {
      const decodedToken = jwtDecode(token);
      const currentTime = Math.floor(Date.now() / 1000); // Obtém o tempo atual em segundos
      return decodedToken && decodedToken.exp
        ? decodedToken.exp > currentTime // Verifica se o token não expirou
        : false;
    } catch (error) {
      console.error("Erro ao decodificar o token:", error);
      return false;
    }
  };

  // Função para realizar o login
  const login = async (username: string, password: string) => {
    const response = await axios.post(`${BASE_URL}/token`, {
      username,
      password,
    });
    const token = response.data.access;
    if (isTokenValid(token)) {
      const userData = { username, token };
      setUser(userData); // Define o usuário autenticado
      localStorage.setItem("user", JSON.stringify(userData)); // Armazena o usuário localmente
    } else {
      throw new Error("Token inválido ou expirado recebido");
    }
    setLoading(false); // Define o carregamento como concluído
  };

  // Função para registrar um novo usuário
  const register = async (username: string, password: string) => {
    try {
      setLoading(true); // Define o carregamento como iniciado
      const response = await axios.post(`${BASE_URL}/register`, {
        username,
        password,
      });
      const token = response.data.access;
      if (token) {
        const userData = { username, token };
        setUser(userData); // Define o usuário autenticado
        localStorage.setItem("user", JSON.stringify(userData)); // Armazena o usuário localmente
      }
      setLoading(false); // Define o carregamento como concluído
    } catch (error) {
      console.error("Falha no registro:", error);
      setLoading(false); // Define o carregamento como concluído, mesmo em caso de erro
      throw error;
    }
  };

  // Função para realizar o logout
  const logout = () => {
    try {
      setUser(null); // Remove o usuário autenticado
      localStorage.removeItem("user"); // Remove o usuário do armazenamento local
      localStorage.removeItem("token"); // Remove o token do armazenamento local
    } catch (error) {
      console.error("Falha no logout:", error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
