import React from "react";

interface Props {
	selectedEvent: any;
	onClose: () => void;
}

export default function EventDetailModal({ selectedEvent, onClose }: Props) {
	if (!selectedEvent) return null;

	return (
		<div className="modal">
			<div className="modal-content">
				<h2>{selectedEvent.title}</h2>
				<p>
					<strong>日付:</strong> {selectedEvent.date}
				</p>
				{selectedEvent.start_time && (
					<p>
						<strong>開始:</strong> {selectedEvent.start_time}
					</p>
				)}
				{selectedEvent.end_time && (
					<p>
						<strong>終了:</strong> {selectedEvent.end_time}
					</p>
				)}
				<p>
					<strong>終日:</strong>{" "}
					{selectedEvent.is_all_day ? "はい" : "いいえ"}
				</p>
				{selectedEvent.location && (
					<p>
						<strong>場所:</strong> {selectedEvent.location}
					</p>
				)}
				{selectedEvent.content && (
					<p>
						<strong>内容:</strong> {selectedEvent.content}
					</p>
				)}
				{selectedEvent.tags?.length > 0 && (
					<p>
						<strong>タグ:</strong> {selectedEvent.tags.join(", ")}
					</p>
				)}
				{selectedEvent.checklist?.length > 0 && (
					<p>
						<strong>チェックリスト:</strong>{" "}
						{selectedEvent.checklist.join(", ")}
					</p>
				)}
				<div className="modal-actions">
					<button onClick={onClose}>閉じる</button>
				</div>
			</div>
		</div>
	);
}
