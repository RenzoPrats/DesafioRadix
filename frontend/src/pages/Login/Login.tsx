import { useState } from "react";
import { useAuth } from "../../context/Auth";
import { useNavigate, Link } from "react-router-dom";
import "./Login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  // Função responsável por lidar com o processo de login
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate("/");
    } catch (error) {
      console.error(error);
      setError("E-mail ou senha inválidos");
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleLogin}>
        <h2 className="login-title">Login</h2>
        <div className="input-group">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            required
          />
        </div>
        <div className="input-group">
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Senha"
            required
          />
        </div>
        <p className="register-link">
          Ainda não possui cadastro?{" "}
          <Link to="/register">Cadastre-se aqui</Link>
        </p>
        <button className="login-button" type="submit">
          Entrar
        </button>
        {error && <p className="error-message">{error}</p>}
      </form>
    </div>
  );
};

export default Login;
