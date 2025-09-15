// components/CalendarTable.tsx
import CalendarCell from "./CalendarCell";

export default function CalendarTable({
	currentDate,
	schedule,
	diaries,
	onCellClick,
}) {
	const year = currentDate.getFullYear();
	const month = currentDate.getMonth();
	const firstDay = new Date(year, month, 1);
	const startDay = firstDay.getDay();
	const daysInMonth = new Date(year, month + 1, 0).getDate();

	const rows = [];

	for (let i = 0; i < 6; i++) {
		const cells = [];
		for (let j = 0; j < 7; j++) {
			const date = new Date(year, month, i * 7 + j - startDay + 1);
			const dateKey = date.toISOString().split("T")[0];
			cells.push(
				<CalendarCell
					key={dateKey}
					date={date}
					schedule={schedule[dateKey]}
					diary={diaries[dateKey]}
					onClick={() => onCellClick(date)}
					// isToday, isSelectedなども渡す
				/>
			);
		}
		rows.push(<tr key={i}>{cells}</tr>);
	}

	return (
		<table>
			<tbody>{rows}</tbody>
		</table>
	);
}
