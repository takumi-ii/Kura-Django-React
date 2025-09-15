// components/Modal.tsx
import React from "react";
import { createPortal } from "react-dom";

interface ModalProps {
	isOpen: boolean;
	onClose: () => void;
	children: React.ReactNode;
	title?: string;
	width?: string;
	height?: string;
}

const Modal: React.FC<ModalProps> = ({
	isOpen,
	onClose,
	children,
	title,
	width = "500px",
	height = "auto",
}) => {
	if (!isOpen) return null;

	return createPortal(
		<div
			className="modal-overlay"
			style={{
				position: "fixed",
				top: 0,
				left: 0,
				right: 0,
				bottom: 0,
				backgroundColor: "rgba(0, 0, 0, 0.5)",
				display: "flex",
				alignItems: "center",
				justifyContent: "center",
				zIndex: 1000,
			}}
			onClick={onClose}
		>
			<div
				className="modal-content"
				style={{
					backgroundColor: "white",
					padding: "20px",
					borderRadius: "8px",
					width,
					height,
					position: "relative",
				}}
				onClick={(e) => e.stopPropagation()}
			>
				{title && <h2>{title}</h2>}
				<button
					onClick={onClose}
					style={{
						position: "absolute",
						top: "10px",
						right: "10px",
						border: "none",
						background: "transparent",
						fontSize: "18px",
						cursor: "pointer",
					}}
				>
					&times;
				</button>
				<div className="modal-body">{children}</div>
			</div>
		</div>,
		document.body
	);
};

export default Modal;
