// CalendarApp.tsx

import React, { useState, useEffect } from "react";
import AddEventModal from "../components/AddEventModal";
import ProfileModal from "../components/ProfileModal";
import EventDetailModal from "../components/EventDetailModal";
import CalendarCell from "../components/CalendarCell";
import {
	fetchMonthlyEvents,
	get_calendar_event_detail,
} from "../services/calendarService";

const CalendarApp: React.FC = () => {
	const [currentDate, setCurrentDate] = useState(new Date());
	const [events, setEvents] = useState({});
	const [selectedEvent, setSelectedEvent] = useState(null);
	const [selectedDate, setSelectedDate] = useState<string>("");
	const [showAddModal, setShowAddModal] = useState(false);
	const [showProfileModal, setShowProfileModal] = useState(false);

	const loadEvents = async () => {
		const year = currentDate.getFullYear();
		const month = currentDate.getMonth() + 1;
		const data = await fetchMonthlyEvents(year, month);
		setEvents(data);
	};

	useEffect(() => {
		loadEvents();
	}, [currentDate]);

	const handleDayClick = async (dateKey: string, eventId?: string) => {
		setSelectedDate(dateKey);
		if (eventId) {
			const detail = await get_calendar_event_detail(eventId);
			setSelectedEvent(detail);
		}
	};

	return (
		<div>
			{/* カレンダー表示省略。日単位セルに CalendarCell を使用 */}

			<AddEventModal
				isOpen={showAddModal}
				onClose={() => setShowAddModal(false)}
				onAdd={(data) => console.log("新しいイベント:", data)}
				selectedDate={selectedDate}
			/>

			<ProfileModal
				isOpen={showProfileModal}
				onClose={() => setShowProfileModal(false)}
				onSubmit={(u, e) => console.log("更新:", u, e)}
				initialUsername="demo"
				initialEmail="demo@example.com"
			/>

			<EventDetailModal
				isOpen={!!selectedEvent}
				onClose={() => setSelectedEvent(null)}
				event={selectedEvent}
			/>
		</div>
	);
};

export default CalendarApp;
