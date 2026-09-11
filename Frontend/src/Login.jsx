import { useState } from "react";
import { login, register } from "./api";

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setError("");
      setLoading(true);

      if (isRegistering) {
        await register(email, password);

        setIsRegistering(false);
        setError("");

        alert("Registration successful. Please login.");
      } else {
        const result = await login(email, password);

        localStorage.setItem(
          "access_token",
          result.access_token
        );

        onLogin(result.access_token);
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      <div className="login-card">

        <h1>
          Invoice OCR
        </h1>

        <p>
          {isRegistering
            ? "Create your account"
            : "Login to your dashboard"}
        </p>


        <form onSubmit={handleSubmit}>

          <label>
            Email
          </label>

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            required
          />


          <label>
            Password
          </label>

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            required
          />


          {error && (
            <p className="error">
              {error}
            </p>
          )}


          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading
              ? "Please wait..."
              : isRegistering
              ? "Register"
              : "Login"}
          </button>

        </form>


        <button
          className="switch-button"
          onClick={() => {
            setIsRegistering(!isRegistering);
            setError("");
          }}
        >
          {isRegistering
            ? "Already have an account? Login"
            : "Don't have an account? Register"}
        </button>

      </div>

    </div>
  );
}

export default Login;