import { useState } from "react";
import { useAuth } from "../../context/Auth";
import { useNavigate, Link } from "react-router-dom";
import "./Register.css";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [error, setError] = useState("");
  const { register } = useAuth();
  const navigate = useNavigate();

  // Função responsável por lidar com o processo de registro
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== passwordConfirm) {
      setError("As senhas não coincidem");
      return;
    }
    try {
      await register(email, password);
      navigate("/");
    } catch (error) {
      console.error(error);
      setError("Falha ao registrar");
    }
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleRegister}>
        <h2 className="register-title">Registro</h2>
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
            placeholder="Password"
            required
          />
        </div>
        <div className="input-group">
          <input
            type="password"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            placeholder="Confirme a Senha"
            required
          />
        </div>
        <p className="login-link">
          Já possui cadastro? <Link to="/login">Entre aqui</Link>
        </p>
        <button className="register-button" type="submit">
          Registrar
        </button>
        {error && <p className="error-message">{error}</p>}
      </form>
    </div>
  );
};

export default Register;
