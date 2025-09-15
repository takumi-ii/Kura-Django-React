// src/hooks/useAuthCheck.ts
import { useEffect, useState } from "react";
import axios from "axios";

export function useAuthCheck() {
	const [loading, setLoading] = useState(true);
	const [authenticated, setAuthenticated] = useState(false);

	useEffect(() => {
		const check = async () => {
			try {
				const res = await axios.post(
					"http://localhost:8000/api/authenticated/",
					{}, // POSTデータ（空でOK）
					{ withCredentials: true } // オプション
				);
				setAuthenticated(res.data.authenticated);
			} catch (e) {
				setAuthenticated(false);
			} finally {
				setLoading(false);
			}
		};
		check();
	}, []);

	return { loading, authenticated };
}
