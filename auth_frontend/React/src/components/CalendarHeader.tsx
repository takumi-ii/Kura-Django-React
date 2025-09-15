export default function CalendarHeader({
	currentDate,
	onPrev,
	onNext,
	onProfile,
}) {
	return (
		<div className="calendar-header">
			<button onClick={onPrev}>＜</button>
			<h2>
				{currentDate.toLocaleDateString("ja-JP", {
					year: "numeric",
					month: "long",
				})}
			</h2>
			<button onClick={onNext}>＞</button>
			<button onClick={onProfile}>プロフィール</button>
		</div>
	);
}
