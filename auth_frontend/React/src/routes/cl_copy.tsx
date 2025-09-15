import React, { useEffect, useState, type JSX } from "react";
import axios from "axios";
import "./calendar.css";
import profilePic from "./prof.png";
import { logout } from "../endpoints/api";
import {
	submit_calendar_event,
	get_calendar_ids,
	get_calendar_event_detail,
} from "../endpoints/api";

interface ScheduleItem {
	title: string;
	time?: string;
	color?: string;
	done?: boolean;
	event_id?: string;
	calendar_id?: string;
}

interface DiaryEntry {
	id: string;
	title: string;
	body: string;
	created_at: string;
	// 他に必要なフィールドがあれば追加
}
type FormDataType = {
	date: string;
	title: string;
	content: string;
	location: string;
	start_time: string;
	end_time: string;
	is_all_day: boolean;
	tags: string[];
	urls: string[];
	checklist: string[];
	share_with: string[];
	is_public: boolean;
	notification_time: string;
};

type Schedule = Record<string, ScheduleItem[]>;
type Diaries = Record<string, DiaryEntry[]>;

// Axios の基本設定
axios.defaults.withCredentials = true;

export default function CalendarApp(): JSX.Element {
	const [currentDate, setCurrentDate] = useState<Date>(new Date());
	const [selectedDate, setSelectedDate] = useState<string | null>(null);

	// APIから取得したスケジュールと日記
	const [schedule, setSchedule] = useState<Schedule>({});
	const [diaries, setDiaries] = useState<Diaries>({});

	// 予定追加用モーダル
	const [showModal, setShowModal] = useState<boolean>(false);

	const [selectedEvent, setSelectedEvent] = useState<any | null>(null);

	// プロファイル関連状態
	const [showProfile, setShowProfile] = useState<boolean>(false);
	const [isEditingProfile, setIsEditingProfile] = useState<boolean>(false);
	const [username, setUsername] = useState<string>("ユーザー名");
	const [email, setEmail] = useState<string>("メールアドレス");
	const [password, setPassword] = useState<string>("");
	const lastLogin = "2023年1月1日";

	// エラーメッセージ状態
	const [errorMessage, setErrorMessage] = useState<string>("");

	// 月切り替え・初回レンダー時にAPI呼び出し
	useEffect(() => {
		const year = currentDate.getFullYear();
		const month = currentDate.getMonth() + 1;

		// スケジュール取得
		axios
			.get(
				`http://localhost:8000/api/calendar/month/?year=${year}&month=${month}`,
				{ withCredentials: true }
			)
			.then((response) => {
				const data: any[] = response.data;
				const byDate: Schedule = {};
				data.forEach((item) => {
					const d = item.date;
					if (!byDate[d]) byDate[d] = [];
					byDate[d].push({
						title: item.title,
						time: item.start_time?.slice(0, 5),
						color: item.is_all_day ? undefined : "red",
						done: item.is_all_day,
						event_id: item.event_id, // 追加
						calendar_id: item.calendar, // 追加
					});
				});
				setSchedule(byDate);
			})
			.catch(console.error);

		// 日記取得
		const startDate = new Date(year, month - 1, 1, 0, 0, 0).toISOString();
		const endDate = new Date(
			year,
			month - 1,
			new Date(year, month, 0).getDate(),
			23,
			59,
			59
		).toISOString();
		axios
			.get(
				`http://localhost:8000/api/diary/entries/?start_date=${startDate}&end_date=${endDate}`,
				{ withCredentials: true }
			)
			.then((response) => {
				const data: DiaryEntry[] = response.data;
				const byDate: Diaries = {};
				data.forEach((entry) => {
					const d = entry.created_at.split("T")[0];
					if (!byDate[d]) byDate[d] = [];
					byDate[d].push(entry);
				});
				setDiaries(byDate);
			})
			.catch(console.error);
	}, [currentDate]);

	// モーダル表示時に選択日を設定
	useEffect(() => {
		setFormData((prev) => ({
			...prev,
			date: selectedDate || new Date().toISOString().split("T")[0],
		}));
	}, [showModal]);

	const year = currentDate.getFullYear();
	const month = currentDate.getMonth();

	const getDateKey = (y: number, m: number, d: number) =>
		`${y}-${String(m + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;

	const renderDays = (): JSX.Element[] => {
		const firstDay = new Date(year, month, 1).getDay();
		const daysInMonth = new Date(year, month + 1, 0).getDate();
		const rows: JSX.Element[] = [];
		let cells: JSX.Element[] = [];

		for (let i = 0; i < firstDay; i++) {
			cells.push(<td key={`empty-${i}`}></td>);
		}
		for (let day = 1; day <= daysInMonth; day++) {
			const dateKey = getDateKey(year, month, day);
			const isToday =
				new Date().toDateString() ===
				new Date(year, month, day).toDateString();
			const isSelected = selectedDate === dateKey;
			const cellClass = `${isToday ? "today" : ""} ${
				isSelected ? "selected-day" : ""
			}`;
			const daySchedule = schedule[dateKey] || [];
			const dayDiaries = diaries[dateKey] || [];
			cells.push(
				<td
					key={day}
					className={cellClass}
					onClick={() => setSelectedDate(dateKey)}
				>
					<div className="day-label">{day}</div>
					{daySchedule.map((ev, i) => (
						<div
							key={`ev-${i}`}
							className={`event ${ev.done ? "event-box" : ""}`}
							style={
								ev.color && !ev.done ? { color: ev.color } : {}
							}
							onClick={async (e) => {
								e.stopPropagation();
								try {
									if (ev.event_id) {
										const detail =
											await get_calendar_event_detail(
												ev.event_id
											);

										setSelectedEvent(detail);
									}
								} catch (err) {
									console.error("詳細の取得に失敗:", err);
									setSelectedEvent(null);
								}
							}}
						>
							{ev.color && !ev.done ? (
								<>
									<span
										className="dot"
										style={{ background: ev.color }}
									/>
									{ev.title} {ev.time}
								</>
							) : ev.done ? (
								`■ ${ev.title}`
							) : (
								ev.title
							)}
						</div>
					))}
					{dayDiaries.map((di, i) => (
						<div key={`di-${i}`} className="diary-entry">
							📝 {di.title}
						</div>
					))}
				</td>
			);
			if ((firstDay + day) % 7 === 0 || day === daysInMonth) {
				rows.push(<tr key={`row-${day}`}>{cells}</tr>);
				cells = [];
			}
		}
		return rows;
	};

	const handlePrevMonth = (): void => {
		const d = new Date(currentDate);
		d.setMonth(month - 1);
		setCurrentDate(d);
		setSelectedDate(null);
	};
	const handleNextMonth = (): void => {
		const d = new Date(currentDate);
		d.setMonth(month + 1);
		setCurrentDate(d);
		setSelectedDate(null);
	};

	const handleLogout = async (e?: React.FormEvent) => {
		if (e) e.preventDefault();
		try {
			const success = await logout();
			if (success) {
				// ログアウト後の処理（例: ログイン画面へ遷移）
				window.location.href = "/login";
			} else {
				setErrorMessage("ログアウトに失敗しました");
			}
		} catch {
			setErrorMessage("ログアウト中にエラーが発生しました");
		}
	};

	// useStateはコンポーネントのトップで宣言
	const [formData, setFormData] = useState<FormDataType>({
		date: "",
		title: "",
		content: "",
		location: "",
		start_time: "",
		end_time: "",
		is_all_day: false,
		tags: [],
		urls: [],
		checklist: [],
		share_with: [],
		is_public: false,
		notification_time: "",
	});

	const buildEventData = (calendarId: string, formData: FormDataType) => {
		const eventData: any = {
			calendar: calendarId,
			date: formData.date,
			title: formData.title,
			is_all_day: formData.is_all_day,
			is_public: formData.is_public,
		};

		if (formData.start_time) eventData.start_time = formData.start_time;
		if (formData.end_time) eventData.end_time = formData.end_time;
		if (formData.content) eventData.content = formData.content;
		if (formData.location) eventData.location = formData.location;
		if (formData.tags && formData.tags.length > 0)
			eventData.tags = formData.tags;
		if (formData.urls && formData.urls.length > 0)
			eventData.urls = formData.urls;
		if (formData.checklist && formData.checklist.length > 0)
			eventData.checklist = formData.checklist;
		if (formData.share_with && formData.share_with.length > 0)
			eventData.share_with = formData.share_with;
		if (formData.notification_time)
			eventData.notification_time = formData.notification_time;

		return eventData;
	};

	const handleSave = async () => {
		if (!formData.date || !formData.title) {
			alert("日付とタイトルは必須です");
			return;
		}
		try {
			const calendars = await get_calendar_ids();
			if (calendars.length === 0) {
				setErrorMessage("カレンダーIDが取得できませんでした");
				return;
			}
			const calendarId = calendars[0].id;

			const eventData = buildEventData(calendarId, formData);

			await submit_calendar_event(eventData);

			setSchedule((prev) => ({
				...prev,
				[formData.date]: [...(prev[formData.date] || []), formData],
			}));
			setShowModal(false);
			setErrorMessage("");
		} catch (err) {
			setErrorMessage("予定の追加に失敗しました");
			console.error(err);
		}
	};

	return (
		<>
			<div className="calendar-container">
				<header className="calendar-header">
					<div className="menu-left">
						<button id="menu-toggle">☰</button>
						<span className="logo">📅 MyCalendar</span>
					</div>
					<h1 id="calendar-title">{`${year}年${month + 1}月`}</h1>
					<button className="bt-month" onClick={handlePrevMonth}>
						&lt; Prev
					</button>
					<button className="bt-month" onClick={handleNextMonth}>
						Next &gt;
					</button>
					<div className="menu-right">
						<button>🔍</button>
						<button onClick={() => setShowModal(true)}>＋</button>
					</div>
					<div className="profile">
						<div
							className="profile-icon"
							onClick={() => setShowProfile(true)}
						></div>
					</div>
				</header>

				<nav className="side-icons">
					<button title="通知">🔔</button>
					<button title="カレンダー">🗓️</button>
					<button title="設定">⚙️</button>
				</nav>

				<table className="calendar-table">
					<thead>
						<tr>
							<th>日</th>
							<th>月</th>
							<th>火</th>
							<th>水</th>
							<th>木</th>
							<th>金</th>
							<th>土</th>
						</tr>
					</thead>
					<tbody>{renderDays()}</tbody>
				</table>
			</div>
			{showModal && (
				<div className="modal">
					<div className="modal-content">
						<h2>予定を追加</h2>
						<label>
							日付:
							<input
								type="date"
								value={formData.date}
								onChange={(e) =>
									setFormData({
										...formData,
										date: e.target.value,
									})
								}
							/>
						</label>
						<label>
							タイトル:
							<input
								type="text"
								value={formData.title}
								onChange={(e) =>
									setFormData({
										...formData,
										title: e.target.value,
									})
								}
							/>
						</label>
						<label>
							内容:
							<input
								type="text"
								value={formData.content || ""}
								onChange={(e) =>
									setFormData({
										...formData,
										content: e.target.value,
									})
								}
							/>
						</label>
						<label>
							場所:
							<input
								type="text"
								value={formData.location || ""}
								onChange={(e) =>
									setFormData({
										...formData,
										location: e.target.value,
									})
								}
							/>
						</label>
						<label>
							開始時間:
							<input
								type="time"
								value={formData.start_time || ""}
								onChange={(e) =>
									setFormData({
										...formData,
										start_time: e.target.value,
									})
								}
							/>
						</label>
						<label>
							終了時間:
							<input
								type="time"
								value={formData.end_time || ""}
								onChange={(e) =>
									setFormData({
										...formData,
										end_time: e.target.value,
									})
								}
							/>
						</label>
						<label>
							終日:
							<input
								type="checkbox"
								checked={formData.is_all_day || false}
								onChange={(e) =>
									setFormData({
										...formData,
										is_all_day: e.target.checked,
									})
								}
							/>
						</label>
						<label>
							タグ（カンマ区切り）:
							<input
								type="text"
								value={
									formData.tags ? formData.tags.join(",") : ""
								}
								onChange={(e) =>
									setFormData({
										...formData,
										tags: e.target.value
											.split(",")
											.map((t) => t.trim()),
									})
								}
							/>
						</label>
						<label>
							URL（カンマ区切り）:
							<input
								type="text"
								value={
									formData.urls ? formData.urls.join(",") : ""
								}
								onChange={(e) =>
									setFormData({
										...formData,
										urls: e.target.value
											.split(",")
											.map((u) => u.trim()),
									})
								}
							/>
						</label>
						<label>
							チェックリスト（カンマ区切り）:
							<input
								type="text"
								value={
									formData.checklist
										? formData.checklist.join(",")
										: ""
								}
								onChange={(e) =>
									setFormData({
										...formData,
										checklist: e.target.value
											.split(",")
											.map((c) => c.trim()),
									})
								}
							/>
						</label>
						<label>
							公開:
							<input
								type="checkbox"
								checked={formData.is_public || false}
								onChange={(e) =>
									setFormData({
										...formData,
										is_public: e.target.checked,
									})
								}
							/>
						</label>
						<label>
							通知日時:
							<input
								type="datetime-local"
								value={formData.notification_time || ""}
								onChange={(e) =>
									setFormData({
										...formData,
										notification_time: e.target.value,
									})
								}
							/>
						</label>
						<div className="modal-actions">
							<button onClick={() => setShowModal(false)}>
								キャンセル
							</button>
							<button onClick={handleSave}>保存</button>
						</div>
					</div>
				</div>
			)}
			{showProfile && (
				<div className="profile-modal">
					<div className="profile-modal-content">
						<div className="profile-modal-inside">
							<div className="profile-header">
								<h2>プロフィール</h2>
								<img
									src={profilePic}
									alt="profile picture"
									className="profile-picture"
								/>
							</div>
							<div className="profile-modal-details">
								{!isEditingProfile && (
									<>
										<p>
											ユーザー名: <span>{username}</span>
										</p>
										<p>
											メール: <span>{email}</span>
										</p>
									</>
								)}
								{isEditingProfile && (
									<>
										<label>
											ユーザー名:
											<input
												value={username}
												onChange={(e) =>
													setUsername(e.target.value)
												}
											/>
										</label>
										<label>
											メール:
											<input
												type="email"
												value={email}
												onChange={(e) =>
													setEmail(e.target.value)
												}
											/>
										</label>
										<label>
											パスワード:
											<input
												type="password"
												value={password}
												onChange={(e) =>
													setPassword(e.target.value)
												}
												placeholder="パスワード"
											/>
										</label>
									</>
								)}
								<p>
									最終ログイン: <span>{lastLogin}</span>
								</p>
							</div>
						</div>
						<div className="profile-modal-actions">
							{isEditingProfile && (
								<button
									onClick={() => setIsEditingProfile(false)}
								>
									save
								</button>
							)}
							<button
								onClick={() =>
									setIsEditingProfile((prev) => !prev)
								}
							>
								{isEditingProfile
									? "キャンセル"
									: "プロフィール編集"}
							</button>
							<button onClick={handleLogout}>Logout</button>
							<button
								onClick={() => {
									setShowProfile(false);
									setIsEditingProfile(false);
								}}
							>
								✖️
							</button>
						</div>
					</div>
				</div>
			)}
			{errorMessage && (
				<div style={{ color: "red", margin: "12px 0" }}>
					{errorMessage}
				</div>
			)}

			{selectedEvent && (
				<div className="modal">
					<div className="modal-content">
						<h2>{selectedEvent.title}</h2>
						<p>
							<strong>日付:</strong> {selectedEvent.date}
						</p>
						{selectedEvent.start_time && (
							<p>
								<strong>開始:</strong>{" "}
								{selectedEvent.start_time}
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
								<strong>タグ:</strong>{" "}
								{selectedEvent.tags.join(", ")}
							</p>
						)}
						{selectedEvent.checklist?.length > 0 && (
							<p>
								<strong>チェックリスト:</strong>{" "}
								{selectedEvent.checklist.join(", ")}
							</p>
						)}
						<div className="modal-actions">
							<button onClick={() => setSelectedEvent(null)}>
								閉じる
							</button>
						</div>
					</div>
				</div>
			)}
		</>
	);
}
