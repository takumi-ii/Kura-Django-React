// hooks/useCalendarData.ts
import { useState, useEffect } from "react";
import { fetchSchedule, fetchDiary } from "../services/calendarService";

export const useCalendarData = (currentDate: Date) => {
	const [schedule, setSchedule] = useState({});
	const [diaries, setDiaries] = useState({});

	useEffect(() => {
		const year = currentDate.getFullYear();
		const month = currentDate.getMonth() + 1;
		const startDate = `${year}-${month.toString().padStart(2, "0")}-01`;
		const endDate = `${year}-${month.toString().padStart(2, "0")}-31`;

		fetchSchedule(year, month).then(setSchedule).catch(console.error);
		fetchDiary(startDate, endDate).then(setDiaries).catch(console.error);
	}, [currentDate]);

	return { schedule, diaries };
};
