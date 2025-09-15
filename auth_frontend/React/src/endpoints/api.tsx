import axios from "axios";
import { useEffect, useState } from "react";

const BASE_URL = "http://localhost:8000/api";
const LOGIN_URL = `${BASE_URL}/token/`;
const LOGOUT_URL = `${BASE_URL}/logout/`;
const REGISTER_URL = `${BASE_URL}/register/`;
const IS_AUTHENTICATED_URL = `${BASE_URL}/authenticated/`;
const REFRESH_TOKEN_URL = `${BASE_URL}/token/refresh/`;
const NOTES_URL = `${BASE_URL}/notes/`;
const WEATHER_URL = `${BASE_URL}/weather/`;
const CALENDAR_CREATE_URL = `${BASE_URL}/calendar/create/`;
const USER_PROFILE_URL = `${BASE_URL}/user/profile/`;
const CALENDAR_EVENT_URL = `${BASE_URL}/calendar/`;

export const login = async (username: string, password: string) => {
	try {
		const response = await axios.post(
			LOGIN_URL,
			{
				username,
				password,
			},
			{ withCredentials: true } // Include credentials for CORS
		);
		// console.log("response.data:", response.data);
		return Boolean(response.data?.success);
	} catch (error) {
		return false;
	}
};

export const logout = async () => {
	try {
		await axios.post(LOGOUT_URL, {}, { withCredentials: true }); // Include credentials for CORS
		return true;
	} catch (error) {
		return false;
	}
};

export const refresh_token = async () => {
	try {
		await axios.post(
			REFRESH_TOKEN_URL,
			{},
			{ withCredentials: true } // Include credentials for CORS
		);
		return true;
	} catch (error) {
		return false;
	}
};

const call_refresh = async (error: any, func: () => Promise<any>) => {
	if (error.response && error.response.status === 401) {
		const tokenRefreshed = await refresh_token();
		if (tokenRefreshed) {
			const retryResponse = await func();
			return retryResponse.data;
		}
	}
	return false;
};

type Note = {
	id: number;
	description: string;
	owner: number;
};

export const get_notes = async (): Promise<Note[]> => {
	try {
		const response = await axios.get(NOTES_URL, { withCredentials: true });
		// 直接 Note[] を返す構造ならそのまま返す
		return response.data;
	} catch (error) {
		// リフレッシュ後も同様に Note[] を返すように
		return await call_refresh(error, () =>
			axios
				.get(NOTES_URL, { withCredentials: true })
				.then((res) => res.data)
		);
	}
};

export type WeatherInfo = {
	prefecture: string;
	weather: string;
	temperature: string;
};

export const useWeather = () => {
	const [data, setData] = useState<WeatherInfo | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const fetchWeather = async (lat: number, lng: number) => {
			try {
				const response = await axios.get(WEATHER_URL, {
					params: {
						latlng: `${lat},${lng}`,
					},
					withCredentials: true,
				});
				setData(response.data);
			} catch (err: any) {
				setError("天気情報の取得に失敗しました。");
			} finally {
				setLoading(false);
			}
		};

		// ブラウザから緯度経度を取得
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				(position) => {
					const { latitude, longitude } = position.coords;
					fetchWeather(latitude, longitude);
				},
				() => {
					setError("位置情報の取得に失敗しました。");
					setLoading(false);
				}
			);
		} else {
			setError("このブラウザでは位置情報が取得できません。");
			setLoading(false);
		}
	}, []);

	return { data, loading, error };
};

// カレンダーID取得
export const get_calendar_ids = async () => {
	try {
		const response = await axios.get(USER_PROFILE_URL, {
			withCredentials: true,
		});
		// calendar_idsは配列で返る
		return response.data.calendar_ids as { id: string; name: string }[];
	} catch (error) {
		return [];
	}
};

// カレンダーイベント登録
export const submit_calendar_event = async (eventData: {
	calendar: string;
	date: string;
	start_time: string;
	end_time: string;
	is_all_day: boolean;
	title: string;
	content: string;
	location: string;
	tags: string[];
	urls: string[];
	checklist: string[];
	share_with: string[];
	is_public: boolean;
	notification_time: string;
}) => {
	try {
		const response = await axios.post(CALENDAR_CREATE_URL, eventData, {
			withCredentials: true,
		});
		return response.data;
	} catch (error) {
		throw error;
	}
};

export const get_calendar_event_detail = async (eventId: string) => {
	const url = `${CALENDAR_EVENT_URL}${eventId}/`;

	try {
		const response = await axios.get(url, {
			withCredentials: true,
		});
		//console.log("APIレスポンス:", response);
		return response.data;
	} catch (error) {
		throw error;
	}
};
