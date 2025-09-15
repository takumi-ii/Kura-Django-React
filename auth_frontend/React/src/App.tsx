import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./routes/login";
import Calendar from "./routes/calendar";
import WeatherPanel from "./routes/weather";
import PrivateRoute from "./components/PrivateRoute";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/login" element={<Login />} />
				<Route
					path="/"
					element={
						<PrivateRoute>
							<Calendar />
						</PrivateRoute>
					}
				/>
				<Route
					path="/weather"
					element={
						<PrivateRoute>
							<WeatherPanel />
						</PrivateRoute>
					}
				/>
			</Routes>
		</Router>
	);
}

export default App;
