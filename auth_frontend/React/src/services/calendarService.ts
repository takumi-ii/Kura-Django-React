import axios from "axios";

export const fetchMonthlyEvents = (year: number, month: number) => {
	return axios.get(
		`http://localhost:8000/api/calendar/month/?year=${year}&month=${month}`,
		{ withCredentials: true }
	);
};

export const fetchDiary = (startDate: string, endDate: string) => {
	return axios.get(
		`http://localhost:8000/api/diary/entries/?start_date=${startDate}&end_date=${endDate}`,
		{ withCredentials: true }
	);
};

export const get_calendar_event_detail = (eventId: string) => {
	return axios.get(`http://localhost:8000/api/calendar/${eventId}/`, {
		withCredentials: true,
	});
};
