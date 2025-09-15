// components/ProfileModal.tsx

import React, { useState } from "react";
import Modal from "../Modal";

interface Props {
	isOpen: boolean;
	onClose: () => void;
	onSubmit: (username: string, email: string) => void;
	initialUsername: string;
	initialEmail: string;
}

const ProfileModal: React.FC<Props> = ({
	isOpen,
	onClose,
	onSubmit,
	initialUsername,
	initialEmail,
}) => {
	const [username, setUsername] = useState(initialUsername);
	const [email, setEmail] = useState(initialEmail);

	const handleSubmit = () => {
		onSubmit(username, email);
		onClose();
	};

	return (
		<Modal isOpen={isOpen} onClose={onClose} title="プロフィール編集">
			<div className="form-group">
				<label>ユーザー名</label>
				<input
					value={username}
					onChange={(e) => setUsername(e.target.value)}
					className="input"
				/>
			</div>
			<div className="form-group">
				<label>メールアドレス</label>
				<input
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					className="input"
				/>
			</div>
			<button onClick={handleSubmit} className="btn-primary mt-2">
				保存
			</button>
		</Modal>
	);
};

export default ProfileModal;
