// components/AddEventModal.tsx

import React, { useState } from "react";
import Modal from "./Modal";
import { buildEventData, EventFormData } from "../utils/buildEventData";

interface Props {
	isOpen: boolean;
	onClose: () => void;
	onAdd: (eventData: any) => void;
	selectedDate: string;
}

const AddEventModal: React.FC<Props> = ({
	isOpen,
	onClose,
	onAdd,
	selectedDate,
}) => {
	const [form, setForm] = useState<EventFormData>({
		title: "",
		content: "",
		location: "",
		date: selectedDate,
		start_time: "",
		end_time: "",
		is_all_day: false,
		tags: [],
		checklist: [],
		is_public: false,
	});

	const handleChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
	) => {
		setForm({ ...form, [e.target.name]: e.target.value });
	};

	const handleSubmit = () => {
		const data = buildEventData(form);
		onAdd(data);
		onClose();
	};

	return (
		<Modal isOpen={isOpen} onClose={onClose} title="予定を追加">
			<input
				name="title"
				value={form.title}
				onChange={handleChange}
				placeholder="タイトル"
				className="input"
			/>
			<textarea
				name="content"
				value={form.content}
				onChange={handleChange}
				placeholder="内容"
				className="input mt-1"
			/>
			<input
				name="location"
				value={form.location}
				onChange={handleChange}
				placeholder="場所"
				className="input mt-1"
			/>
			{/* 他にもタグやチェックリストなどの入力フィールドを追加可能 */}
			<button onClick={handleSubmit} className="btn-primary mt-2">
				追加
			</button>
		</Modal>
	);
};

export default AddEventModal;
