import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../endpoints/api";

const Login = () => {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [errorMessage, setErrorMessage] = useState("");
	const navigate = useNavigate();

	const handleLogin = async (e: React.FormEvent) => {
		e.preventDefault();
		try {
			const success = await login(username, password);
			if (success) {
				navigate("/");
			} else {
				setErrorMessage("ログインに失敗しました");
			}
		} catch (err) {
			setErrorMessage("ログイン中にエラーが発生しました");
		}
	};

	return (
		<form
			onSubmit={handleLogin}
			style={{ maxWidth: 400, margin: "40px auto" }}
		>
			<div style={{ marginBottom: 16 }}>
				<label htmlFor="username">Username</label>
				<input
					id="username"
					type="text"
					value={username}
					onChange={(e) => setUsername(e.target.value)}
					autoComplete="username"
					style={{
						width: "100%",
						padding: 8,
						boxSizing: "border-box",
					}}
				/>
			</div>
			<div style={{ marginBottom: 16 }}>
				<label htmlFor="password">Password</label>
				<input
					id="password"
					type="password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
					autoComplete="current-password"
					style={{
						width: "100%",
						padding: 8,
						boxSizing: "border-box",
					}}
				/>
			</div>
			<button type="submit" style={{ width: "100%", padding: 10 }}>
				ログイン
			</button>
			{errorMessage && (
				<div style={{ color: "red", marginTop: 12 }}>
					{errorMessage}
				</div>
			)}
		</form>
	);
};
export default Login;
