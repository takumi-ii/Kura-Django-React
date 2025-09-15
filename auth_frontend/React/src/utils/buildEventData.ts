// utils/buildEventData.ts

export interface EventFormData {
	title: string;
	content: string;
	location: string;
	date: string; // YYYY-MM-DD
	start_time?: string; // HH:MM
	end_time?: string; // HH:MM
	is_all_day: boolean;
	tags: string[];
	checklist: string[];
	is_public: boolean;
}

export function buildEventData(form: EventFormData) {
	const data: any = {
		title: form.title,
		content: form.content,
		location: form.location,
		date: form.date,
		is_all_day: form.is_all_day,
		tags: form.tags,
		checklist: form.checklist,
		is_public: form.is_public,
	};

	if (!form.is_all_day) {
		data.start_time = form.start_time || null;
		data.end_time = form.end_time || null;
	} else {
		data.start_time = null;
		data.end_time = null;
	}

	return data;
}
