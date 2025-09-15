// components/CalendarCell.tsx
export default function CalendarCell({ date, schedule, diary, isToday, isSelected, onClick }) {
	return (
		<td
			className={`${isToday ? "today" : ""} ${isSelected ? "selected-day" : ""}`}
			onClick={onClick}
		>
			<div className="day-label">{date.getDate()}</div>
			{/* スケジュールと日記の描画 */}
			{schedule?.map(...)}
			{diary?.map(...)}
		</td>
	);
}
