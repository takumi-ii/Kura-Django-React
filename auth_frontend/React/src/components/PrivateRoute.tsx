// // src/components/PrivateRoute.tsx
// import { Navigate } from "react-router-dom";
// import { ReactNode } from "react";
// import { isAuthenticated } from "../auth";

// interface PrivateRouteProps {
// 	children: ReactNode;
// }

// const PrivateRoute = ({ children }: PrivateRouteProps) => {
// 	return isAuthenticated() ? children : <Navigate to="/login" replace />;
// };

// export default PrivateRoute;

// src/components/PrivateRoute.tsx
import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";
import { useAuthCheck } from "../hooks/useAuthCheck";

interface PrivateRouteProps {
	children: ReactNode;
}

const PrivateRoute = ({ children }: PrivateRouteProps) => {
	const { loading, authenticated } = useAuthCheck();

	if (loading) {
		// ローディング中の表示（スピナーなどに変更可）
		return <div>Loading...</div>;
	}

	if (!authenticated) {
		// 未認証 → ログインページにリダイレクト
		return <Navigate to="/login" replace />;
	}

	// 認証済み
	return children;
};

export default PrivateRoute;
