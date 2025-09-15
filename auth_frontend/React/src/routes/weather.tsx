// src/components/WeatherPanel.tsx
import { Box, Heading, Text, Spinner, VStack } from "@chakra-ui/react";
import { useWeather } from "../endpoints/api"; // Adjust the import path as necessary

const WeatherPanel = () => {
	const { data, loading, error } = useWeather();

	return (
		<Box borderWidth="1px" borderRadius="lg" p={4}>
			<Heading as="h3" size="md">
				現在の天気
			</Heading>
			{loading ? (
				<Spinner mt={2} />
			) : error ? (
				<Text color="red.500" mt={2}>
					{error}
				</Text>
			) : data ? (
				<VStack align="start" mt={2}>
					<Text>地域: {data.prefecture}</Text>
					<Text>天気: {data.weather}</Text>
					<Text>気温: {data.temperature}</Text>
				</VStack>
			) : (
				<Text mt={2}>天気情報が取得できませんでした。</Text>
			)}
		</Box>
	);
};

export default WeatherPanel;
